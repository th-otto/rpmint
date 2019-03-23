/*
 * Copyright (c) 1989 The Regents of the University of California.
 * All rights reserved.
 *
 * This code is derived from software contributed to Berkeley by
 * Mike Muuss.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. All advertising materials mentioning features or use of this software
 *    must display the following acknowledgement:
 *	This product includes software developed by the University of
 *	California, Berkeley and its contributors.
 * 4. Neither the name of the University nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

char copyright[] =
  "@(#) Copyright (c) 1989 The Regents of the University of California.\n"
  "All rights reserved.\n";
/*
 * From: @(#)ping.c	5.9 (Berkeley) 5/12/91
 */
char rcsid[] = "$Id: ping.c,v 1.39 2000/07/23 04:16:21 dholland Exp $";
#include "../version.h"

/*
 *			P I N G . C
 *
 * Using the InterNet Control Message Protocol (ICMP) "ECHO" facility,
 * measure round-trip-delays and packet loss across network paths.
 *
 * Author -
 *	Mike Muuss
 *	U. S. Army Ballistic Research Laboratory
 *	December, 1983
 *
 * Status -
 *	Public Domain.  Distribution Unlimited.
 * Bugs -
 *	More statistics could always be gathered.
 *	This program has to run SUID to ROOT to access the ICMP socket.
 */

#include <sys/param.h>
#include <sys/socket.h>
#include <sys/file.h>
#include <sys/time.h>
#include <sys/signal.h>

#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <errno.h>

/*
 * Note: on some systems dropping root makes the process dumpable or
 * traceable. In that case if you enable dropping root and someone
 * traces ping, they get control of a raw socket and can start
 * spoofing whatever packets they like. SO BE CAREFUL.
 */
#ifdef __linux__
#define SAFE_TO_DROP_ROOT
#endif

/********************* Garble for libc5 ********************/

#if !defined(__GLIBC__) || (__GLIBC__ < 2)
#ifdef __linux__

/*
 * The Linux kernel definitions of icmp and ip header structures are
 * different from traditional BSD. Linux libcs prior to libc6 don't 
 * provide the BSD versions. Get them from the included file.
 */

#include "pingpack.h"

#endif /* __linux__ */
#endif /* __GLIBC__ */

/********************* Defs. *********************/

/* default data length: 64 byte icmp packet */
#define	DEFDATALEN	(64 - ICMP_MINLEN)

/* maximum length of IP header (including options) */
#define	MAXIPLEN	60

/* max packet contents size */
#define	MAXPAYLOAD	(IP_MAXPACKET - MAXIPLEN - ICMP_MINLEN)

/* max seconds to wait for response */
#define	MAXWAIT		10

/* number of record route slots */
#define	NROUTES		9


/* various options */
static int options;
#define	F_FLOOD		0x001
#define	F_INTERVAL	0x002
#define	F_NUMERIC	0x004
#define	F_PINGFILLED	0x008
#define	F_QUIET		0x010
#define	F_RROUTE	0x020
#define	F_SO_DEBUG	0x040
#define	F_SO_DONTROUTE	0x080
#define	F_VERBOSE	0x100

/* multicast options */
static int moptions;
#define MULTICAST_NOLOOP	0x001
#define MULTICAST_TTL		0x002
#define MULTICAST_IF		0x004

/*
 * bitarray for remembering duplicates
 *
 * MAX_DUP_CHK is the number of bits in received table, i.e. the maximum
 * number of received sequence numbers we can keep track of.  Change 128
 * to 8192 for complete accuracy...
 */
#define	MAX_DUP_CHK	(8 * 128)
static int mx_dup_ck = MAX_DUP_CHK;
static char rcvd_tbl[MAX_DUP_CHK / 8];

#define	A(bit)		rcvd_tbl[(bit)>>3]	/* identify byte in array */
#define	B(bit)		(1 << ((bit) & 0x07))	/* identify bit in byte */
#define	SET(bit)	(A(bit) |= B(bit))
#define	CLR(bit)	(A(bit) &= (~B(bit)))
#define	TST(bit)	(A(bit) & B(bit))


/* characters written for flood */
static const char BSPACE = '\b';
static const char DOT = '.';

/* transmission */
static int sock;		/* socket file descriptor */
static int ident;		/* process id to identify our packets */

/* destination */
static struct sockaddr_in whereto;	/* who to ping */
static const char *hostname;

/*
 * input buffer
 *
 * inpack contains:
 *         ip header    (20 octets)
 *         ip options   (0-40 octets (ipoptlen))
 *         icmp header  (8 octets)
 *         timeval      (8 or 12 octets, only if timing==1)
 *         other data
 */
static u_int8_t inpack[IP_MAXPACKET];
static int ipoptlen;

#define INPACK_IP       ((struct ip *)inpack)
#define INPACK_OPTS     (inpack+sizeof(struct ip))
#define INPACK_ICMP     ((struct icmp *)(inpack+sizeof(struct ip)+ipoptlen))
#define INPACK_PAYLOAD  (INPACK_ICMP->icmp_data)
#define INPACK_TIME     ((struct timeval *)INPACK_PAYLOAD)
#define INPACK_DATA     (INPACK_PAYLOAD+(timing ? sizeof(struct timeval) : 0))


/* 
 * output buffer
 *
 * outpack contains:
 *         icmp header  (8 octets)
 *         timeval      (8 or 12 octets, only if timing==1)
 *         other data
 *
 * datalen is the length of the other data plus the timeval.
 * note: due to alignment problems don't assign to OUTPACK_TIME, use memcpy.
 */
static u_int8_t outpack[IP_MAXPACKET];
static int datalen = DEFDATALEN;

#define OUTPACK_ICMP    ((struct icmp *)outpack)
#define OUTPACK_PAYLOAD (OUTPACK_ICMP->icmp_data)
#define OUTPACK_TIME    ((struct timeval *)OUTPACK_PAYLOAD)
#define OUTPACK_DATA    (OUTPACK_PAYLOAD+(timing ? sizeof(struct timeval) : 0))


/* counters */
static long npackets;		/* max packets to transmit */
static long nreceived;		/* # of packets we got back */
static long nrepeats;		/* number of duplicates */
static long ntransmitted;	/* sequence # for outbound packets = #sent */
static int intervalsecs = 1;	/* interval between packets (seconds) */

/* timing */
static int timing;		/* flag to do timing */
static long tmin = LONG_MAX;	/* minimum round trip time */
static long tmax = 0;		/* maximum round trip time */
static u_long tsum;		/* sum of all times, for doing average */

/********************* utility code ********************/

/*
 * in_cksum
 *
 * Checksum routine for Internet Protocol family headers (C version)
 */
static 
u_int16_t
in_cksum(u_int16_t *addr, int len)
{
	int nleft = len;
	u_int16_t *w = addr;
	u_int32_t sum = 0;
	u_int16_t answer = 0;

	/*
	 * Our algorithm is simple, using a 32 bit accumulator (sum), we add
	 * sequential 16 bit words to it, and at the end, fold back all the
	 * carry bits from the top 16 bits into the lower 16 bits.
	 */
	while (nleft > 1)  {
		sum += *w++;
		nleft -= 2;
	}

	/* mop up an odd byte, if necessary */
	if (nleft == 1) {
		answer=0;
		*(u_char *)(&answer) = *(u_char *)w ;
		sum += answer;
	}

	/* add back carry outs from top 16 bits to low 16 bits */
	sum = (sum >> 16) + (sum & 0xffff);	/* add hi 16 to low 16 */
	sum += (sum >> 16);			/* add carry */
	answer = ~sum;				/* truncate to 16 bits */
	return(answer);
}

/*
 * tvsub
 *
 * Subtract 2 timeval structs:  out = out - in.  
 */
static
void
tvsub(struct timeval *out, const struct timeval *in)
{
	if ((out->tv_usec -= in->tv_usec) < 0) {
		out->tv_sec--;
		out->tv_usec += 1000000;
	}
	out->tv_sec -= in->tv_sec;

	/*
	 * Just in case, clamp to 0.
	 */
	if (out->tv_sec<0) {
		out->tv_sec = 0;
		out->tv_usec = 0;
	}
}

/*
 * tvadd
 *
 * Add 2 timeval structs:  out = out + in.  
 */
static
void
tvadd(struct timeval *out, const struct timeval *in)
{
	if ((out->tv_usec += in->tv_usec) >= 1000000) {
		out->tv_sec++;
		out->tv_usec -= 1000000;
	}
	out->tv_sec += in->tv_sec;
}

/********************* printing code ********************/

/*
 * pr_addr --
 *	Return an ascii host address as a dotted quad and optionally with
 * a hostname.
 */
static 
const char *
pr_addr(u_int32_t l)
{
	struct hostent *hp;
	static char buf[256];
	struct in_addr addr;

	if (l==0) {
		return "0.0.0.0";
	}

	addr.s_addr = l;
	if ((options & F_NUMERIC)==0) {
		hp = gethostbyaddr((char *)&l, 4, AF_INET);
		if (hp) {
			snprintf(buf, sizeof(buf), "%s (%s)", hp->h_name,
				 inet_ntoa(addr));
			return buf;
		}
	}

	return inet_ntoa(addr);
}

/*
 * pr_iph --
 *	Print an IP header with options.
 */
static
void
pr_iph(struct ip *ip)
{
	u_int hlen;
	u_char *cp;

	hlen = ip->ip_hl << 2;
	cp = ((u_char *)ip) + sizeof(struct ip);	/* point to options */

	printf("Vr HL TOS  Len   ID Flg  off TTL Pro  cks      "
	       "Src      Dst Data\n");
	printf(" %1x  %1x  %02x %04x %04x",
	       ip->ip_v, ip->ip_hl, ip->ip_tos, ip->ip_len, ip->ip_id);
	printf("   %1x %04x", ((ip->ip_off) & 0xe000) >> 13,
	       (ip->ip_off) & 0x1fff);
	printf("  %02x  %02x %04x", ip->ip_ttl, ip->ip_p, ip->ip_sum);
	printf(" %s ", inet_ntoa(ip->ip_src));
	printf(" %s ", inet_ntoa(ip->ip_dst));
	/* dump any option bytes */
	while (hlen-- > sizeof(struct ip)) {
		printf("%02x", *cp++);
	}
	putchar('\n');
}

/*
 * pr_retip --
 *	Dump some info on a returned (via ICMP) IP packet.
 */
static void
pr_retip(struct ip *ip)
{
	int hlen;
	u_char *cp;

	pr_iph(ip);
	hlen = ip->ip_hl << 2;

	/* 
	 * theoretically, ip->ip_hl is a 4-bit unsigned value, so 
	 * 0 <= hlen < 64 and cp cannot point outside inpack.
	 */
	cp = (u_char *)ip + hlen;

	if (ip->ip_p == 6) {
		printf("TCP: from port %u, to port %u (decimal)\n",
		       (*cp * 256 + *(cp + 1)), (*(cp + 2) * 256 + *(cp + 3)));
	}
	else if (ip->ip_p == 17) {
		printf("UDP: from port %u, to port %u (decimal)\n",
		       (*cp * 256 + *(cp + 1)), (*(cp + 2) * 256 + *(cp + 3)));
	}
}

/*
 * pr_icmph --
 *	Print a descriptive string about an ICMP header.
 */
static 
void
pr_icmph(struct icmp *icp)
{
	switch(icp->icmp_type) {
	case ICMP_ECHOREPLY:
		/* This is not used - we only call this for non-replies. */
		printf("Echo Reply (!?)\n");
		break;
	case ICMP_DEST_UNREACH:
		switch(icp->icmp_code) {
		case ICMP_NET_UNREACH:
			printf("Destination Net Unreachable\n");
			break;
		case ICMP_HOST_UNREACH:
			printf("Destination Host Unreachable\n");
			break;
		case ICMP_PROT_UNREACH:
			printf("Destination Protocol Unreachable\n");
			break;
		case ICMP_PORT_UNREACH:
			printf("Destination Port Unreachable\n");
			break;
		case ICMP_FRAG_NEEDED:
			printf("frag needed and DF set\n");
			break;
		case ICMP_SR_FAILED:
			printf("Source Route Failed\n");
			break;
		case ICMP_NET_UNKNOWN:
			printf("Network Unknown\n");
			break;
		case ICMP_HOST_UNKNOWN:
			printf("Host Unknown\n");
			break;
		case ICMP_HOST_ISOLATED:
			printf("Host Isolated\n");
			break;
		case ICMP_NET_UNR_TOS:
			printf("Destination Network Unreachable at this TOS\n");
			break;
		case ICMP_HOST_UNR_TOS:
			printf("Destination Host Unreachable at this TOS\n");
			break;
#ifdef ICMP_PKT_FILTERED
		case ICMP_PKT_FILTERED:
			printf("Packet Filtered\n");
			break;
#endif
#ifdef ICMP_PREC_VIOLATION
		case ICMP_PREC_VIOLATION:
			printf("Precedence Violation\n");
			break;
#endif
#ifdef ICMP_PREC_CUTOFF
		case ICMP_PREC_CUTOFF:
			printf("Precedence Cutoff\n");
			break;
#endif
		default:
			printf("Dest Unreachable, Unknown Code: %d\n",
			       icp->icmp_code);
			break;
		}
		/* Print returned IP header information */
		pr_retip((struct ip *)icp->icmp_data);
		break;
	case ICMP_SOURCE_QUENCH:
		printf("Source Quench\n");
		pr_retip((struct ip *)icp->icmp_data);
		break;
	case ICMP_REDIRECT:
		switch(icp->icmp_code) {
		case ICMP_REDIR_NET:
			printf("Redirect Network");
			break;
		case ICMP_REDIR_HOST:
			printf("Redirect Host");
			break;
		case ICMP_REDIR_NETTOS:
			printf("Redirect Type of Service and Network");
			break;
		case ICMP_REDIR_HOSTTOS:
			printf("Redirect Type of Service and Host");
			break;
		default:
			printf("Redirect, Bad Code: %d", icp->icmp_code);
			break;
		}
		printf("(New addr: %s)\n", inet_ntoa(icp->icmp_gwaddr));
		pr_retip((struct ip *)icp->icmp_data);
		break;
	case ICMP_ECHO:
		printf("Echo Request\n");
		/* XXX ID + Seq + Data */
		break;
	case ICMP_TIME_EXCEEDED:
		switch(icp->icmp_code) {
		case ICMP_EXC_TTL:
			printf("Time to live exceeded\n");
			break;
		case ICMP_EXC_FRAGTIME:
			printf("Frag reassembly time exceeded\n");
			break;
		default:
			printf("Time exceeded, Bad Code: %d\n",
			    icp->icmp_code);
			break;
		}
		pr_retip((struct ip *)icp->icmp_data);
		break;
	case ICMP_PARAMETERPROB:
		printf("Parameter problem: IP address = %s\n",
		       inet_ntoa(icp->icmp_gwaddr));
		pr_retip((struct ip *)icp->icmp_data);
		break;
	case ICMP_TIMESTAMP:
		printf("Timestamp\n");
		/* XXX ID + Seq + 3 timestamps */
		break;
	case ICMP_TIMESTAMPREPLY:
		printf("Timestamp Reply\n");
		/* XXX ID + Seq + 3 timestamps */
		break;
	case ICMP_INFO_REQUEST:
		printf("Information Request\n");
		/* XXX ID + Seq */
		break;
	case ICMP_INFO_REPLY:
		printf("Information Reply\n");
		/* XXX ID + Seq */
		break;
#ifdef ICMP_MASKREQ
	case ICMP_MASKREQ:
		printf("Address Mask Request\n");
		break;
#endif
#ifdef ICMP_MASKREPLY
	case ICMP_MASKREPLY:
		printf("Address Mask Reply\n");
		break;
#endif
	default:
		printf("Bad ICMP type: %d\n", icp->icmp_type);
	}
}

static
void
pr_opts(void)
{
	static int old_rrlen;
	static char old_rr[MAX_IPOPTLEN];

	int i,j,k;
	u_int32_t addr;
	u_int8_t *cp = INPACK_OPTS;

	for (i=0; i<ipoptlen; i++) {
		switch (cp[i]) {
		case IPOPT_EOL:
			return;
		case IPOPT_LSRR:
			printf("\nLSRR: ");
			j = cp[++i];
			i++; /* ? */
			if (j > IPOPT_MINOFF) {
				while (i<ipoptlen) {
					memcpy(&addr, &cp[i+1], sizeof(addr));
					printf("\t%s", pr_addr(ntohl(addr)));
					i += sizeof(addr);
					j -= sizeof(addr);
					if (j <= IPOPT_MINOFF)
						break;
					putchar('\n');
				}
			}
			break;
		case IPOPT_RR:
			j = cp[++i];		/* get length */
			k = cp[++i];		/* and pointer */
			if (k > j)
				k = j;
			k -= IPOPT_MINOFF;
			if (k <= 0)
				continue;
			if (k == old_rrlen
			    && i==2
			    && !memcmp(cp+i, old_rr, k)
			    && !(options & F_FLOOD)) {
				printf("\t(same route)");
				k = ((k + 3) / 4) * 4;
				i += k;
				break;
			}
			if (k < MAX_IPOPTLEN) {
				old_rrlen = k;
				memcpy(old_rr, cp+i, k);
			} 
			else {
				old_rrlen = 0;
			}
			j=0;
			printf("\nRR: ");
			for (;;) {
				memcpy(&addr, &cp[i+1], sizeof(addr));
				printf("\t%s", pr_addr(ntohl(addr)));
				i += 4;
				j += 4;
				k -= 4;
				if (k <= 0)
					break;
				if (j >= MAX_IPOPTLEN) {
					printf("\t(truncated route)");
					break;
				}
				putchar('\n');
			}
			break;
		case IPOPT_NOP:
			printf("\nNOP");
			break;
		default:
			printf("\nunknown option %x", cp[i]);
			break;
		}
	}
}

static
void
check_packet_data(void)
{
	u_int8_t *cp, *dp;
	int i;
	struct icmp *icp;

	cp = (u_int8_t *)INPACK_PAYLOAD;
	icp = OUTPACK_ICMP;
	dp = (u_int8_t *)icp->icmp_data;

	for (i=0; i<datalen-ICMP_MINLEN; i++) {
		if (cp[i] != dp[i]) {
			printf("\n");
			printf("wrong data byte #%d should be 0x%x "
			       "but was 0x%x",
			       i, dp[i], cp[i]);
			for (i=0; i<datalen-ICMP_MINLEN; i++) {
				if ((i % 32) == 8)
					printf("\n\t");
				printf("%x ", cp[i]);
			}
			return;
		}
	}
}

/*
 * pr_pack
 *
 * Print out the packet, if it came from us.
 * 
 * This check is necessary because ALL readers of the ICMP socket get a 
 * copy of ALL ICMP packets which arrive ('tis only fair).  This permits 
 * multiple copies of this program to be run without having intermingled 
 * output (or statistics!).
 *
 * Returns nonzero if it was one of our echo replies.
 */
static
int
pr_pack(int packlen, struct sockaddr_in *from)
{
	struct ip *ip;
	struct icmp *icp;
	struct timeval now, packettv, *tp;
	long triptime = 0;
	int hlen, dupflag;
	int rv;

	gettimeofday(&now, NULL);

	/* Check the IP header */
	ip = INPACK_IP;
	hlen = ip->ip_hl << 2;
	if (hlen < (int)sizeof(struct ip)) {
		if (options & F_VERBOSE) {
			fprintf(stderr,
				"ping: packet too short (%d octets with "
				"IP header) from %s\n", 
				packlen, inet_ntoa(from->sin_addr));
		}
		return 0;
	}
	if (hlen > packlen) {
		if (options & F_VERBOSE) {
			fprintf(stderr,
				"ping: partial packet (%d octets IP header, "
				"whole packet only %d) from %s\n", 
				hlen, packlen, inet_ntoa(from->sin_addr));
		}
		return 0;
	}
	ipoptlen = hlen - sizeof(struct ip);
	packlen -= hlen;
	icp = INPACK_ICMP;

	/* ICMP_MINLEN is the size of the icmp header (8 octets) */
	if (packlen < ICMP_MINLEN + datalen) {
		if (options & F_VERBOSE) {
			fprintf(stderr,
				"ping: packet too short (%d octets) from %s\n",
				packlen, inet_ntoa(from->sin_addr));
		}
		return 0;
	}


	/* Now the ICMP part */
	if (icp->icmp_type == ICMP_ECHOREPLY) {
		if (icp->icmp_id != ident)
			return 0;		/* 'Twas not our ECHO */
		nreceived++;
		if (timing) {
			tp = (struct timeval *)icp->icmp_data;
			memcpy(&packettv, tp, sizeof(struct timeval));
			tvsub(&now, &packettv);

			/* precision: tenths of milliseconds */
			triptime = now.tv_sec * 10000 + (now.tv_usec / 100);

			tsum += triptime;
			if (triptime < tmin)
				tmin = triptime;
			if (triptime > tmax)
				tmax = triptime;
		}

		if (TST(icp->icmp_seq % mx_dup_ck)) {
			++nrepeats;
			--nreceived;
			dupflag = 1;
		} 
		else {
			SET(icp->icmp_seq % mx_dup_ck);
			dupflag = 0;
		}

		if (options & F_QUIET) {
			return 1;
		}

		rv = 1;

		if (options & F_FLOOD) {
			write(STDOUT_FILENO, &BSPACE, 1);
		}
		else {
			printf("%d octets from %s: icmp_seq=%u", packlen,
			       inet_ntoa(from->sin_addr), icp->icmp_seq);
			printf(" ttl=%d", ip->ip_ttl);
			if (timing) {
				printf(" time=%ld.%ld ms", triptime/10,
				       triptime%10);
			}
			if (dupflag) {
				printf(" (DUP!)");
			}

			/* check the data */
			check_packet_data();
		}
	} 
	else {
		/* We've got something other than an ECHOREPLY */
		if ((options & F_VERBOSE)==0) {
			return 0;
		}
		printf("%d octets from %s: ", packlen,
		       pr_addr(from->sin_addr.s_addr));
		pr_icmph(icp);
		rv = 0;
	}

	/* Display any IP options */
	pr_opts();

	if ((options & F_FLOOD)==0) {
		putchar('\n');
		fflush(stdout);
	}

	return rv;
}

/********************* pinging code ********************/

/*
 * finish --
 *	Print out statistics, and give up.
 */
static
void
finish(int ignore)
{
	(void)ignore;

	signal(SIGINT, SIG_IGN);
	putchar('\n');
	fflush(stdout);
	printf("--- %s ping statistics ---\n", hostname);
	printf("%ld packets transmitted, ", ntransmitted);
	printf("%ld packets received, ", nreceived);
	if (nrepeats) {
		printf("+%ld duplicates, ", nrepeats);
	}
	if (ntransmitted) {
		if (nreceived > ntransmitted)
			printf("-- somebody's printing up packets!");
		else
			printf("%ld%% packet loss",
			       ((ntransmitted - nreceived) * 100) /
				ntransmitted);
	}
	putchar('\n');

	if (nreceived && timing) {
		printf("round-trip min/avg/max = %ld.%ld/%lu.%lu/%ld.%ld ms\n",
			tmin/10, tmin%10,
			(tsum / (nreceived + nrepeats))/10,
			(tsum / (nreceived + nrepeats))%10,
			tmax/10, tmax%10);
	}

	if (nreceived==0) exit(1);
	exit(0);
}

/*
 * pinger
 * 	
 * Compose and transmit an ICMP ECHO REQUEST packet.  The IP header
 * will be added on by the kernel.  The ID field is our UNIX process ID,
 * and the sequence number is an ascending integer.  The first few bytes
 * of the data portion are used to hold a UNIX "timeval" struct, to 
 * compute the round-trip time. 
 */
static
void
pinger(void)
{
	struct icmp *icp;
	size_t packlen;
	int sentlen;

	icp = OUTPACK_ICMP;
	icp->icmp_type = ICMP_ECHO;
	icp->icmp_code = 0;
	icp->icmp_cksum = 0;
	icp->icmp_seq = ntransmitted++;
	icp->icmp_id = ident;

	CLR(icp->icmp_seq % mx_dup_ck);

	if (timing) {
		struct timeval tmptm;
		gettimeofday(&tmptm, NULL);
		memcpy(icp->icmp_data, &tmptm, sizeof(tmptm));
	}

	/* get total length of outpack (datalen is total length of payload) */
	packlen = datalen + ((u_int8_t *)icp->icmp_data - outpack);

	/* compute ICMP checksum here */
	icp->icmp_cksum = in_cksum((u_short *)outpack, packlen);

	sentlen = sendto(sock, outpack, packlen, 0,
			 (struct sockaddr *)&whereto, sizeof(whereto));
	if (sentlen != (int)packlen)  {
		if (sentlen < 0) {
			perror("sendto");
		}
		printf("ping: sent %d octets to %s, ret=%d\n", 
		       (int)packlen, hostname, sentlen);
	}

	if ((options & F_QUIET)==0 && (options & F_FLOOD)) {
		write(STDOUT_FILENO, &DOT, 1);
	}
}

static
int
compute_waittime(void)
{
	int waittime;
	if (nreceived) {
		waittime = 2 * tmax / 1000;
		if (!waittime)
			waittime = 1;
		if (waittime > MAXWAIT)
			waittime = MAXWAIT;
	} 
	else {
		waittime = MAXWAIT;
	}
	return waittime;
}

static
void
doping(void)
{
	struct sockaddr_in from;
	socklen_t fromlen;
	struct timeval interval, next, now, timeout;
	fd_set mask;
	int dosend=1, packlen;

	if (options & F_FLOOD) {
		interval.tv_sec = 0;
		interval.tv_usec = 10000;
	}
	else {
		interval.tv_sec = intervalsecs;
		interval.tv_usec = 0;
	}
	FD_ZERO(&mask);

	/*
	 * Loop forever sending pings. (Well, not quite forever.)
	 */
	while (1) {
		if (dosend) {
			dosend = 0;
			pinger();
			if (npackets && ntransmitted >= npackets) {
				/* 
				 * That was the last one.
				 * Set `interval' to how long to wait for 
				 * any remaining replies to roll in.
				 */
				interval.tv_sec = compute_waittime();
				interval.tv_usec = 0;
			}

			/* set time to next ping: the interval */
			gettimeofday(&next, NULL);
			tvadd(&next, &interval);
			timeout = interval;
		}
		else {
			/* compute time left to next ping */
			gettimeofday(&now, NULL);
			timeout = next;
			tvsub(&timeout, &now);
		}

		FD_SET(sock, &mask);
		if (select(sock+1, &mask, NULL, NULL, &timeout) < 1) {
			/* Timed out - exit if none left to send. */
			if (npackets && ntransmitted >= npackets) {
				break;
			}
			/* Otherwise, send another */
			dosend = 1;
			continue;
		}

		/* A packet's come in, get it */
		fromlen = sizeof(from);
		packlen = recvfrom(sock, inpack, sizeof(inpack), 0,
				   (struct sockaddr *)&from, &fromlen);
		if (packlen < 0) {
			if (errno == EINTR)
				continue;
			perror("recvfrom");
			continue;
		}

		if (pr_pack(packlen, &from)) {
			/*
			 * In flood mode, getting a packet back instantly
			 * triggers the next one.
			 */
			if (options & F_FLOOD) {
				dosend = 1;
			}
		}

		if (npackets && nreceived >= npackets) {
			/*
			 * Got all the replies - stop.
			 */
			break;
		}
	}
}

/********************* setup code ********************/

static
int
dosockopt(int code1, int code2, int val)
{
	return setsockopt(sock, code1, code2, &val, sizeof(val));
}

static
void 
settarget(const char *target)
{
	struct hostent *hp;
	static char namebuf[MAXHOSTNAMELEN];

	memset(&whereto, 0, sizeof(whereto));
	hp = gethostbyname(target);
	if (!hp) {
		fprintf(stderr, "ping: unknown host %s\n", target);
		exit(2);
	}
	whereto.sin_family = hp->h_addrtype;
	if (hp->h_length > (int)sizeof(whereto.sin_addr)) {
		hp->h_length = sizeof(whereto.sin_addr);
	}
	memcpy(&whereto.sin_addr, hp->h_addr, hp->h_length);
	strncpy(namebuf, hp->h_name, sizeof(namebuf) - 1);
	namebuf[sizeof(namebuf)-1] = 0;
	hostname = namebuf;
}

/*
 * Handle -p option.
 */
static
void
fill(const char *patstr)
{
	size_t i;
	int j, patlen;
	int pat[16];

	for (i=0; patstr[i]; i++) {
		if (!isxdigit(patstr[i])) {
			fprintf(stderr, "ping: patterns for -p must be "
				"specified as hex digits.\n");
			exit(2);
		}
	}

	patlen = sscanf(patstr,
	    "%2x%2x%2x%2x%2x%2x%2x%2x%2x%2x%2x%2x%2x%2x%2x%2x",
	    &pat[0], &pat[1], &pat[2], &pat[3], &pat[4], &pat[5], &pat[6],
	    &pat[7], &pat[8], &pat[9], &pat[10], &pat[11], &pat[12],
	    &pat[13], &pat[14], &pat[15]);

	/*
	 * Just fill the whole output packet with the pattern, rather
	 * than just the data section. The part at the beginning will get
	 * overlaid with the icmp header and whatnot.
	 *
	 * This means we don't have to know yet if we're sending the
	 * timeval (which depends on the selected packet size), which 
	 * is good since get called from option processing and the -s
	 * option might not have turned up yet.
	 */
	if (patlen > 0) {
		for (i=0,j=0; i<sizeof(outpack); i++, j=(j+1)%patlen) {
			outpack[i] = pat[j];
		}
	}

	if (!(options & F_QUIET)) {
		printf("PATTERN: 0x");
		for (j=0; j<patlen; j++) {
			printf("%02x", pat[j]&0xFF);
		}
		printf("\n");
	}
}

static
void
usage(void)
{
	fprintf(stderr,
		"usage: ping [-LRdfnqrv] [-c count] [-i wait] [-l preload]\n"
		"\t[-p pattern] [-s packetsize] [-t ttl] "
		"[-I interface address] host\n");
	exit(2);
}

static
int
secure_startup(void)
{
	int am_i_root;
	struct protoent *proto;

	/*
	 * Clear environment.
	 * (This protects against various problems with libc.)
	 */
#if 0
	static char *null = NULL;
	__environ = &null;
#endif

	/*
	 * Certain options require that the man behind the curtain be
	 * root. Since we should be setuid root anyway, check real uid.
	 */
	am_i_root = (getuid()==0);

	/*
	 * Look up ICMP.
	 */
	proto = getprotobyname("icmp");
	if (!proto) {
		fprintf(stderr, "ping: unknown protocol icmp.\n");
		exit(2);
	}

	/*
	 * Open the raw socket.
	 */
	sock = socket(AF_INET, SOCK_RAW, proto->p_proto);
	if (sock < 0) {
		if (errno==EPERM) {
			fprintf(stderr, "ping: ping must run as root\n");
		}
		else {
			perror("ping: socket");
		}
		exit(2);
	}

	/*
	 * If someone's messing with us, bail.
	 * It would be nice to issue an error message, but to where? 
	 */
	if (sock==STDIN_FILENO || sock==STDOUT_FILENO || sock==STDERR_FILENO) {
		exit(255);
	}

	/* 
	 * See discussion at the top of this file.
	 * It's not crucial if this fails.
	 */
#ifdef SAFE_TO_DROP_ROOT
	setuid(getuid());
#endif

	return am_i_root;
}


int
main(int argc, char *argv[])
{
	struct in_addr ifaddr;
	int i;
	int ch, preload, stoptime=0;
	u_char ttl=0, loop;
	int am_i_root;
	char rspace[3 + 4 * NROUTES + 1];	/* record route space */

	am_i_root = secure_startup();

	preload = 0;
	while ((ch = getopt(argc, argv, "I:LRc:dfh:i:l:np:qrs:t:vw:"))!=EOF) {
		switch(ch) {
		case 'c':
			npackets = atoi(optarg);
			if (npackets <= 0) {
				fprintf(stderr, 
					"ping: bad number of "
					"packets to transmit.\n");
				exit(2);
			}
			break;
		case 'd':
			options |= F_SO_DEBUG;
			break;
		case 'f':
			if (!am_i_root) {
				fprintf(stderr, "ping: %s\n", strerror(EPERM));
				exit(2);
			}
			options |= F_FLOOD;
			setbuf(stdout, NULL);
			break;
		case 'i':		/* wait between sending packets */
			intervalsecs = atoi(optarg);
			if (intervalsecs <= 0) {
				fprintf(stderr,"ping: bad timing interval.\n");
				exit(2);
			}
			options |= F_INTERVAL;
			break;
		case 'l':
			if (!am_i_root) {
				fprintf(stderr, "ping: %s\n", strerror(EPERM));
				exit(2);
			}
			preload = atoi(optarg);
			if (preload < 0) {
				fprintf(stderr, "ping: bad preload count.\n");
				exit(2);
			}
			break;
		case 'n':
			options |= F_NUMERIC;
			break;
		case 'p':		/* fill buffer with user pattern */
			options |= F_PINGFILLED;
			fill(optarg);
			break;
		case 'q':
			options |= F_QUIET;
			break;
		case 'R':
			options |= F_RROUTE;
			break;
		case 'r':
			options |= F_SO_DONTROUTE;
			break;
		case 's':		/* size of packet to send */
			if (!am_i_root) {
				fprintf(stderr, "ping: %s\n", strerror(EPERM));
				exit(2);
			}
			datalen = atoi(optarg);
			if (datalen > MAXPAYLOAD) {
				fprintf(stderr, 
					"ping: packet size too large.\n");
				exit(2);
			}
			if (datalen <= 0) {
				fprintf(stderr,"ping: illegal packet size.\n");
				exit(2);
			}
			break;
		case 'v':
			options |= F_VERBOSE;
			break;
		case 'w':
			stoptime = atoi(optarg);
			if (stoptime <= 0) {
				fprintf(stderr,"ping: illegal timeout.\n");
				exit(2);
			}
			break;
		case 'L':
			moptions |= MULTICAST_NOLOOP;
			loop = 0;
			(void) loop;
			break;
		case 't':
			moptions |= MULTICAST_TTL;
			i = atoi(optarg);
			if (i < 0 || i > 255) {
				fprintf(stderr, 
					"ping: ttl %d out of range\n", i);
				exit(2);
			}
			ttl = i;
			break;
		case 'I':
			moptions |= MULTICAST_IF;
			if (!inet_aton(optarg, &ifaddr)) {
				fprintf(stderr, 
					"ping: bad interface address '%s'\n",
					optarg);
				exit(2);
			}
			break;
		default:
			usage();
		}
	}
	if (options & F_FLOOD && options & F_INTERVAL) {
		fprintf(stderr, "ping: -f and -i: Incompatible options.\n");
		exit(2);
	}

	argc -= optind;
	argv += optind;
	
	if (argc != 1) {
		usage();
	}

	settarget(argv[0]);

	/* if there's space for the time, we can time the transfer */
	if (datalen >= (int)sizeof(struct timeval)) {
		timing = 1;
	}

	/* If an explicit pattern wasn't set, use a default fill. */
	if ((options & F_PINGFILLED)==0) {
		int i;
		struct icmp *icp = OUTPACK_ICMP;
		u_int8_t *ptr = (u_int8_t *)icp->icmp_data;
		for (i = 0; i < datalen; i++) {
			ptr[i] = i;
		}
	}

	/* Use this code to identify this ping process */
	ident = getpid() & 0xFFFF;

	if (options & F_SO_DEBUG) {
		dosockopt(SOL_SOCKET, SO_DEBUG, 1);
	}
	if (options & F_SO_DONTROUTE) {
		dosockopt(SOL_SOCKET, SO_DONTROUTE, 1);
	}
	/* this is necessary for broadcast pings to work */
	dosockopt(SOL_SOCKET, SO_BROADCAST, 1);

	/* record route option */
	if (options & F_RROUTE) {
	        memset(rspace, 0, sizeof(rspace));
		rspace[IPOPT_OPTVAL] = IPOPT_RR;
		rspace[IPOPT_OLEN] = sizeof(rspace)-1;
		rspace[IPOPT_OFFSET] = IPOPT_MINOFF;
		if (setsockopt(sock, IPPROTO_IP, IP_OPTIONS, rspace,
		    sizeof(rspace)) < 0) {
			perror("ping: record route");
			exit(2);
		}
	}

	/*
	 * When pinging the broadcast address, you can get a lot of answers.
	 * Doing something so evil is useful if you are trying to stress the
	 * ethernet, or just want to fill the arp cache to get some stuff for
	 * /etc/ethers.
	 */
	dosockopt(SOL_SOCKET, SO_RCVBUF, 64*1024);

	if (moptions & MULTICAST_NOLOOP) {
		if (dosockopt(IPPROTO_IP, IP_MULTICAST_LOOP, 0)) {
			perror("can't disable multicast loopback");
			exit(92);
		}
	}

	if (moptions & MULTICAST_TTL) {
		if (dosockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl)) {
			perror("can't set multicast time-to-live");
			exit(93);
		}
	}

	if (moptions & MULTICAST_IF) {
		if (setsockopt(sock, IPPROTO_IP, IP_MULTICAST_IF,
			       &ifaddr, sizeof(ifaddr))) {
			perror("can't set multicast source interface");
			exit(94);
		}
	}

	if (whereto.sin_family == AF_INET) {
		printf("PING %s (%s): %d octets data\n", 
		       hostname, inet_ntoa(whereto.sin_addr), datalen);
	}
	else {
		printf("PING %s: %d octets data\n", hostname, datalen);
	}

	signal(SIGINT, finish);

	if (stoptime) {
		signal(SIGALRM, finish);
		alarm(stoptime);
	}

	while (preload--) {
		/* fire off them quickies */
		pinger();
	}

	doping();

	finish(0);
	/* NOTREACHED */
	return 0;
}
