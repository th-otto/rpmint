/*
 * Copyright (c) 1982, 1986, 1993
 *	The Regents of the University of California.  All rights reserved.
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
 *
 *	@(#)ip.h	8.1 (Berkeley) 6/10/93
 *	@(#)ip_icmp.h	8.1 (Berkeley) 6/10/93
 */

/*
 * Cut down version of both netinet/ip.h and netinet/ip_icmp.h
 * modified for use in ping.
 *
 * This is so ping works with both libc5 and libc6.
 */

/*
 * Structure of an internet header, naked of options.
 */
struct ip {
#if BYTE_ORDER == LITTLE_ENDIAN
	u_int8_t  ip_hl:4;			/* header length */
	u_int8_t  ip_v:4;			/* version */
#elif BYTE_ORDER == BIG_ENDIAN
	u_int8_t  ip_v:4;			/* version */
	u_int8_t  ip_hl:4;			/* header length */
#else
#error "Don't know your byte order - please fix pingpack.h to get it"
#endif
	u_int8_t  ip_tos;			/* type of service */
	u_int16_t ip_len;			/* total length */
	u_int16_t ip_id;			/* identification */
	u_int16_t ip_off;			/* fragment offset field */
	u_int8_t  ip_ttl;			/* time to live */
	u_int8_t  ip_p;				/* protocol */
	u_int16_t ip_sum;			/* checksum */
	struct in_addr ip_src, ip_dst;		/* source and dest address */
};


struct icmp {
	u_int8_t  icmp_type;	/* type of message, see below */
	u_int8_t  icmp_code;	/* type sub code */
	u_int16_t icmp_cksum;	/* ones complement checksum of struct */
	union {
		struct in_addr ih_gwaddr;	/* gateway address */
		struct ih_idseq {		/* echo datagram */
			u_int16_t icd_id;
			u_int16_t icd_seq;
		} ih_idseq;
	} icmp_hun;
#define	icmp_gwaddr	icmp_hun.ih_gwaddr
#define	icmp_id		icmp_hun.ih_idseq.icd_id
#define	icmp_seq	icmp_hun.ih_idseq.icd_seq

	u_int8_t    icmp_data[1];
};
