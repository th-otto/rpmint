/*
 * Copyright (c) 1983, 1991 The Regents of the University of California.
 * All rights reserved.
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

#include <sys/types.h>
#include <sys/time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <rpc/netdb.h>
#include <sys/un.h>
#include <netdb.h>
#include <syslog.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#include "inetd.h"
#include "servtab.h"
#include "builtins.h"
#include "sig.h"
#include "mysleep.h"

char servtab_rcsid[] = 
  "$Id: servtab.c,v 1.6 2000/07/22 20:20:50 dholland Exp $";

static struct biltin biltins[] = {
	/* service	socktype	fork,wait   function */

	/* Echo received data */
	{ "echo",	SOCK_STREAM,	1, 0,	echo_stream, },
	{ "echo",	SOCK_DGRAM,	0, 0,	echo_dg, },

	/* Internet /dev/null */
	{ "discard",	SOCK_STREAM,	1, 0,	discard_stream, },
	{ "discard",	SOCK_DGRAM,	0, 0,	discard_dg, },

	/* Return 32 bit time since 1900 */
	{ "time",	SOCK_STREAM,	0, 0,	machtime_stream, },
	{ "time",	SOCK_DGRAM,	0, 0,	machtime_dg,     },

	/* Return human-readable time */
	{ "daytime",	SOCK_STREAM,	0, 0,	daytime_stream,     },
	{ "daytime",	SOCK_DGRAM,	0, 0,	daytime_dg,     },

	/* Familiar character generator */
	{ "chargen",	SOCK_STREAM,	1, 0,	chargen_stream,     },
	{ "chargen",	SOCK_DGRAM,	0, 0,	chargen_dg,     },

	{ NULL, 	0, 		0, 0, 	NULL }
};

struct servtab *
find_service_by_fd(int fd)
{
	struct servtab *sep;
	for (sep = servtab; sep; sep = sep->se_next) {
		if (sep->se_fd == fd) return sep;
	}
	return NULL;
}

struct servtab *
find_service_by_pid(pid_t pid)
{
	struct servtab *sep;
	for (sep = servtab; sep; sep = sep->se_next) {
		if (sep->se_wait == pid) return sep;
	}
	return NULL;
}

static
struct servtab *
find_same_service(struct servtab *cp)
{
	struct servtab *sep;
	for (sep = servtab; sep; sep = sep->se_next) {
		if (strcmp(sep->se_service, cp->se_service)) continue;
		if (strcmp(sep->se_proto, cp->se_proto)) continue;

		/* 
		 * At this point they're the same up to bind address.
		 * Catch 1: se_address can be null.
		 * Catch 2: two different se_addresses can give the same IP.
		 * Catch 3: contents of se_ctrladdr_in.sin_addr are undefined
		 *          if they're unix sockets. But we do know that this
		 *          isn't the case if se_address isn't null.
		 */

		/* Easy case: both null (cannot point to the same string) */
		if (sep->se_address == cp->se_address) return sep;

		/* Now, if one is null, the other isn't */
		if (sep->se_address==NULL || cp->se_address==NULL) continue;

		/* Don't bother to compare the hostnames, just the IPs */
		if (sep->se_ctrladdr_in.sin_addr.s_addr ==
		    cp->se_ctrladdr_in.sin_addr.s_addr) return sep;
	}
	return NULL;
}

const char *
service_name(struct servtab *sep)
{
	static char rv[256];
	if (sep->se_address) {
		snprintf(rv, sizeof(rv), "%s/%s@%s", sep->se_service, 
			 sep->se_proto, sep->se_address);
	}
	else {
		snprintf(rv, sizeof(rv), "%s/%s", sep->se_service, 
			 sep->se_proto);
	}
	return rv;
}

/********* exit-resistant malloc ************************/

/*
 * On many systems, including presently Linux, this is bloat because
 * malloc never returns null - if the system runs out of swap, it 
 * panics or randomly starts killing processes or does other weird 
 * stuff. However, it doesn't hurt to be prepared. This is the only
 * place inetd can actually exit due to failure, now.
 */

void *
domalloc(size_t len)
{
	static int retries[] = { 2, 10, 60, 600, -1 };
	void *p;
	int try = 0;

	while (retries[try]>0) {
		p = malloc(len);
		if (p != NULL) {
		    	return p;
		}
	
		syslog(LOG_ERR, "Out of memory - retrying in %d seconds.",
		       retries[try]);
		mysleep(retries[try]);
		try++;
	}
	/* Should this be LOG_EMERG? */
	syslog(LOG_ALERT, "Out of memory - GIVING UP!");
	exit(100);
	return NULL;  /* unreachable */
}

char *
dostrdup(const char *cp)
{
	char *x = domalloc(strlen(cp)+1);
	strcpy(x, cp);
	return x;
}


/********* config parser ********************************/

static void loadconfigent(struct servtab *cp);

static FILE *fconfig = NULL;


#if 0 /* old version */
static struct servtab serv;
static char line[256];

static
char *
nextline(FILE *fd)
{
	char *cp;

	if (fgets(line, sizeof (line), fd) == NULL)
		return ((char *)0);
	cp = strchr(line, '\n');
	if (cp)
		*cp = '\0';
	return (line);
}

static 
char *
skip(char **cpp)
{
	register char *cp = *cpp;
	char *start;

	if (*cpp == NULL)
		return ((char *)0);

again:
	while (*cp == ' ' || *cp == '\t')
		cp++;
	if (*cp == '\0') {
		int c;

		c = getc(fconfig);
		(void) ungetc(c, fconfig);
		if (c == ' ' || c == '\t')
			if ((cp = nextline(fconfig))!=NULL)
				goto again;
		*cpp = NULL;
		return NULL;
	}
	start = cp;
	while (*cp && *cp != ' ' && *cp != '\t')
		cp++;
	if (*cp != '\0')
		*cp++ = '\0';
	*cpp = cp;
	return (start);
}

static
struct servtab *
getconfigent(void)
{
	register struct servtab *sep = &serv;
	int argc;
	char *cp, *arg;

more:
	while ((cp = nextline(fconfig)) && *cp == '#')
		;

	if (cp == NULL) {
		return NULL;
	}

	memset(sep, 0, sizeof(*sep));
	sep->se_service = dostrdup(skip(&cp));
	arg = skip(&cp);
	if (arg == NULL)
		goto more;

	if (strcmp(arg, "stream") == 0)
		sep->se_socktype = SOCK_STREAM;
	else if (strcmp(arg, "dgram") == 0)
		sep->se_socktype = SOCK_DGRAM;
	else if (strcmp(arg, "rdm") == 0)
		sep->se_socktype = SOCK_RDM;
	else if (strcmp(arg, "seqpacket") == 0)
		sep->se_socktype = SOCK_SEQPACKET;
	else if (strcmp(arg, "raw") == 0)
		sep->se_socktype = SOCK_RAW;
	else
		sep->se_socktype = -1;

	sep->se_proto = dostrdup(skip(&cp));
	if (strcmp(sep->se_proto, "unix") == 0) {
		sep->se_family = AF_UNIX;
	} else {
		sep->se_family = AF_INET;
		if (strncmp(sep->se_proto, "rpc/", 4) == 0) {
#ifdef RPC
			char *cp1, *ccp;
			cp1 = index(sep->se_service, '/');
			if (cp1 == NULL) {
				syslog(LOG_ERR, "%s: no rpc version",
				    sep->se_service);
				goto more;
			}
			*cp1++ = '\0';
			sep->se_rpcversl =
				sep->se_rpcversh = strtol(cp1, &ccp, 0);
			if (ccp == cp1) {
		badafterall:
				syslog(LOG_ERR, "%s/%s: bad rpc version",
				    sep->se_service, cp1);
				goto more;
			}
			if (*ccp == '-') {
				cp1 = ccp + 1;
				sep->se_rpcversh = strtol(cp1, &ccp, 0); 
				if (ccp == cp1)
					goto badafterall;
			}
#else
			syslog(LOG_ERR, "%s: rpc services not supported",
			    sep->se_service);
			goto more;
#endif /* RPC */
		}
	}
	arg = skip(&cp);
	if (arg == NULL)
		goto more;
	{
		char	*s = index(arg, '.');
		if (s) {
			*s++ = '\0';
			sep->se_max = atoi(s);
		} else
			sep->se_max = TOOMANY;
	}
	sep->se_wait = strcmp(arg, "wait") == 0;
	sep->se_user = dostrdup(skip(&cp));
	sep->se_group = strchr(sep->se_user, '.');
	if (sep->se_group) {
		*sep->se_group++ = '\0';
	}
	sep->se_server = dostrdup(skip(&cp));
	if (strcmp(sep->se_server, "internal") == 0) {
		register struct biltin *bi;

		for (bi = biltins; bi->bi_service; bi++)
			if (bi->bi_socktype == sep->se_socktype &&
			    strcmp(bi->bi_service, sep->se_service) == 0)
				break;
		if (bi->bi_service == 0) {
			syslog(LOG_ERR, "internal service %s unknown\n",
				sep->se_service);
			goto more;
		}
		sep->se_bi = bi;
		sep->se_wait = bi->bi_wait;
	} else
		sep->se_bi = NULL;
	argc = 0;
	for (arg = skip(&cp); cp; arg = skip(&cp)) {
#if MULOG
		char *colon, *rindex();

		if (argc == 0 && (colon = rindex(arg, ':'))) {
			while (arg < colon) {
				int	x;
				char	*ccp;

				switch (*arg++) {
				case 'l':
					x = 1;
					if (isdigit(*arg)) {
						x = strtol(arg, &ccp, 0);
						if (ccp == arg)
							break;
						arg = ccp;
					}
					sep->se_log &= ~MULOG_RFC931;
					sep->se_log |= x;
					break;
				case 'a':
					sep->se_log |= MULOG_RFC931;
					break;
				default:
					break;
				}
			}
			arg = colon + 1;
		}
#endif
		if (argc < MAXARGV)
			sep->se_argv[argc++] = dostrdup(arg);
	}
	while (argc <= MAXARGV)
		sep->se_argv[argc++] = NULL;
	return (sep);
}
#else /* new version begins here */

struct wordmap {
	const char *word;
	int val;
};

static struct wordmap socket_types[] = {
	{ "stream",    SOCK_STREAM    },
	{ "dgram",     SOCK_DGRAM     },
	{ "rdm",       SOCK_RDM       },
	{ "seqpacket", SOCK_SEQPACKET },
	{ "raw",       SOCK_RAW       },
	{ NULL,        -1 }
};

static
int
map_word(struct wordmap *wm, const char *word)
{
	int i;
	for (i=0; wm[i].word!=NULL; i++) {
		if (!strcmp(wm[i].word, word)) return wm[i].val;
	}
	return -1;
}

static
struct biltin *
find_builtin(int socktype, const char *service)
{
	int i;
	for (i=0; biltins[i].bi_service; i++) {
		if (biltins[i].bi_socktype != socktype) continue;
		if (strcmp(biltins[i].bi_service, service)) continue;
		return &biltins[i];
	}
	
	return NULL;
}

static
const char *
assemble_entry(struct servtab *sep, int nfields, char **fields)
{
	struct in_addr service_home;
	struct hostent *hp;
	char *s, *t;
	int i;

	if (nfields < 6) {
		return "Incomplete config entry";
	}

	memset(sep, 0, sizeof(*sep));

	s = strchr(fields[0], '@');
	if (s) {
		*s++ = 0;
		sep->se_address = s;
		hp = gethostbyname(s);
		if (hp==NULL) return "Service hostname/address not found";
		memcpy(&service_home, hp->h_addr, sizeof(service_home));
	}
	else {
		service_home.s_addr = INADDR_ANY;
	}
	sep->se_service = fields[0];
	sep->se_socktype = map_word(socket_types, fields[1]);
	free(fields[1]);

	sep->se_proto = fields[2];
	if (!strcmp(sep->se_proto, "unix")) {
		sep->se_family = AF_UNIX;
		if (sep->se_address!=NULL) {
			return "@host given for unix socket";
		}
	}
	else {
		sep->se_family = AF_INET;
		sep->se_ctrladdr_in.sin_addr = service_home;

		if (!strncmp(sep->se_proto, "rpc/", 4)) {
#ifdef RPC
			s = strchr(sep->se_service, '/');
			if (!s) return "No RPC version";
			*s++ = 0;
			sep->se_rpcversl = strtol(s, &t, 0);
			if (t==s) return "Invalid RPC version";
			if (*t=='-') {
				s = t+1;
				sep->se_rpcversh = strtol(s, &t, 0);
				if (t==s) return "Invalid RPC high version";
			}
			else {
				sep->se_rpcversh = sep->se_rpcversl;
			}
#else
			return "No support for RPC services compiled in";
#endif
		}
	}

	s = strchr(fields[3], '.');
	if (s) {
		*s++ = 0;
		sep->se_max = atoi(s);
	}
	else {
		sep->se_max = TOOMANY;
	}
	sep->se_wait = !strcmp(fields[3], "wait");
	free(fields[3]);

	s = strchr(fields[4], '.');
	if (s) {
		*s++ = 0;
		sep->se_group = s;
	}
	else {
		sep->se_group = NULL;
	}
	sep->se_user = fields[4];

	sep->se_server = fields[5];
	if (!strcmp(fields[5], "internal")) {
		sep->se_bi = find_builtin(sep->se_socktype, sep->se_service);
		if (sep->se_bi==NULL) {
			return "Invalid internal service";
		}
		sep->se_wait = sep->se_bi->bi_wait;
	}
	else {
		sep->se_bi = NULL;
	}

	/* The rest are argv[]. */ 
	for (i=6; i<nfields; i++) {
		sep->se_argv[i-6] = fields[i];
	}

	/* Most programs core if argv[0] is null. */
	if (!sep->se_argv[0]) {
		sep->se_argv[0] = dostrdup(sep->se_server);
	}

	return NULL;
}

static
const char *
nexttoken(void)
{
	static char linebuf[256];
	char *s;

	/*
	 * Hack: linebuf[0-1] is not read into; it is always "Q ". This permits
	 * us to initialize strtok so that it will return the first word on
	 * the line on the _next_ call if we so choose.
	 */
	linebuf[0] = 'Q';
	linebuf[1] = ' ';

	s = strtok(NULL, " \t\n");
	if (s!=NULL) return s;

	do {
		if (fgets(linebuf+2, sizeof(linebuf)-2, fconfig)==NULL) {
			return NULL;
		}
	} while (linebuf[2]=='#');

	if (!strchr(" \t", linebuf[2])) {
		/* Not a continuation line - send back EOL */
		strtok(linebuf, " \t\n");  /* returns Q */
		return "";
	}

	s = strtok(linebuf+2, " \t\n");
	if (!s) return ""; /* empty line -> send EOL */
	return s;
}

static
void
loadconfigfile(void (*sendents)(struct servtab *))
{
	/* 6 fields plus argv, but the last entry of argv[] must remain null */
	char *fields[MAXARGV+6-1];
	int nfields=0;
	int warned=0;
	const char *s;
	int eof=0;
	struct servtab assm; /* assemble entries into here */
	char junk[4];

	/*
	 * Insure strtok() will start at EOL.
	 */
	junk[0] = 'Q' ;
	junk[1] = 0;	
	strtok(junk, " \t\n");
	
	while (!eof) {
		s = nexttoken();
		if (!s&& nfields<1) {
			eof = 1;
		}
		else if (!s || (!*s && nfields>0)) {
			const char *errmsg;
			errmsg = assemble_entry(&assm, nfields, fields);
			if (errmsg) {
				syslog(LOG_WARNING, "Bad config for %s: %s"
				       " (skipped)", fields[0], errmsg);
			}
			else {
				sendents(&assm);
			}
                        if (!s) {
	                	eof = 1;
	                        }
	                else {
				nfields = 0;
			       	warned = 0;
			}
		}
		else if (!*s) {
			/* blank line */
		}
		else if (nfields < MAXARGV+6) {
			fields[nfields++] = dostrdup(s);
		}
		else if (!warned) {
			syslog(LOG_WARNING, "%s: too many arguments, max %d",
			       fields[0], MAXARGV);
			warned = 1;
		}
	}
}

#endif

/********* config loading ****************************************/

static int
setconfig(void)
{

	if (fconfig != NULL) {
		fseek(fconfig, 0L, SEEK_SET);
		return (1);
	}
	fconfig = fopen(configfile, "r");
	return (fconfig != NULL);
}

static void
endconfig(void)
{
	if (fconfig) {
		(void) fclose(fconfig);
		fconfig = NULL;
	}
}

static void
freeconfig(struct servtab *cp)
{
	int i;

	if (cp->se_service)
		free(cp->se_service);
	cp->se_service = NULL;

	cp->se_address = NULL;  /* points into se_service */

	if (cp->se_proto)
		free(cp->se_proto);
	cp->se_proto = NULL;

	if (cp->se_user)
		free(cp->se_user);
	cp->se_user = NULL;

	cp->se_group = NULL;  /* points into se_user */

	if (cp->se_server)
		free(cp->se_server);
	cp->se_server = NULL;

	for (i = 0; i < MAXARGV; i++) {
		if (cp->se_argv[i])
			free(cp->se_argv[i]);
		cp->se_argv[i] = NULL;
	}
}

/*
 * print_service:
 *	Dump relevant information to stderr
 */
static void
print_service(const char *action, struct servtab *sep)
{
	if (isrpcservice(sep))
		fprintf(stderr,
		    "%s: %s rpcprog=%d, rpcvers = %d/%d, proto=%s, wait.max=%d.%d, user.group=%s.%s builtin=%lx server=%s\n",
		    action, sep->se_service,
		    sep->se_rpcprog, sep->se_rpcversh, sep->se_rpcversl, sep->se_proto,
		    sep->se_wait, sep->se_max, sep->se_user, sep->se_group,
		    (unsigned long)sep->se_bi, sep->se_server);
	else
		fprintf(stderr,
		    "%s: %s proto=%s, wait.max=%d.%d, user.group=%s.%s builtin=%lx server=%s\n",
		    action, sep->se_service, sep->se_proto,
		    sep->se_wait, sep->se_max, sep->se_user, sep->se_group,
		    (unsigned long)sep->se_bi, sep->se_server);
}

static
void
loadconfigent(struct servtab *cp)
{
	struct servtab *sep;
	unsigned n;

	/*
	 * dholland 7/14/1997: always use the canonical service 
	 * name to protect against silly configs that list a 
	 * service twice under different aliases. This has been
	 * observed in the wild thanks to Slackware... 
	 * Note: this is a patch, not a fix. The real fix is
	 * to key the table by port and protocol, not service name
	 * and protocol.
	 */
	if (cp->se_family==AF_INET && !isrpcservice(cp)) {
		u_short port = htons(atoi(cp->se_service));
		
		if (!port) {
			struct servent *sp;
			sp = getservbyname(cp->se_service,
					   cp->se_proto);
			if (sp != NULL) { /* bogus services are caught later */
				if (strcmp(cp->se_service, sp->s_name)) {
					/*
					 * Ugh. Since se_address points into
					 * se_service, we need to copy both
					 * together. Ew.
					 */
					char *tmp, *tmp2 = NULL;
					const char *addr = cp->se_address;
					size_t len = strlen(sp->s_name)+1;
					if (addr==NULL) addr = "";
					len += strlen(addr)+1;
					tmp = domalloc(len);
					strcpy(tmp, cp->se_service);
					if (cp->se_address) {
						tmp2 = tmp+strlen(tmp)+1;
						strcpy(tmp2, cp->se_address);
					}
					free(cp->se_service);
					cp->se_service = tmp;
					cp->se_address = tmp2;
				}
			}
		}
	}
	/* End silly patch */

	sep = find_same_service(cp);

	if (sep != NULL) {
		int i;
		
		if (sep->se_checked) {
			syslog(LOG_WARNING, 
			       "extra conf for service %s (skipped)\n",
			       service_name(sep));
			return;
		}
		
#define SWAP(type, a, b) {type c=(type)a; (type)a=(type)b; (type)b=(type)c;}

		/*
		 * sep->se_wait may be holding the pid of a daemon
		 * that we're waiting for.  If so, don't overwrite
		 * it unless the config file explicitly says don't 
		 * wait.
		 */
		if (cp->se_bi == 0 && (sep->se_wait == 1 || cp->se_wait == 0))
			sep->se_wait = cp->se_wait;
		if (cp->se_max != sep->se_max)
			SWAP(int, cp->se_max, sep->se_max);
		if (cp->se_user)
			SWAP(char *, sep->se_user, cp->se_user);
		if (cp->se_group)
			SWAP(char *, sep->se_group, cp->se_group);
		if (cp->se_server)
			SWAP(char *, sep->se_server, cp->se_server);
		if (cp->se_address) {
			/* must swap se_service; se_address points into it */
			SWAP(char *, sep->se_service, cp->se_service);
			SWAP(char *, sep->se_address, cp->se_address);
		}
		for (i = 0; i < MAXARGV; i++)
			SWAP(char *, sep->se_argv[i], cp->se_argv[i]);
#undef SWAP
		if (isrpcservice(sep))
			unregister_rpc(sep);
		sep->se_rpcversl = cp->se_rpcversl;
		sep->se_rpcversh = cp->se_rpcversh;
		freeconfig(cp);
		if (debug) {
			print_service("REDO", sep);
		}
	}
	else {
		sep = enter(cp);
		if (debug)
			print_service("ADD ", sep);
	}
	sep->se_checked = 1;
	
	switch (sep->se_family) {
	case AF_UNIX:
		if (sep->se_fd != -1)
			break;
		(void)unlink(sep->se_service);
		n = strlen(sep->se_service);
		if (n > sizeof(sep->se_ctrladdr_un.sun_path) - 1) 
			n = sizeof(sep->se_ctrladdr_un.sun_path) - 1;
		strncpy(sep->se_ctrladdr_un.sun_path, 
			sep->se_service, n);
		sep->se_ctrladdr_un.sun_path[n] = 0;
		sep->se_ctrladdr_un.sun_family = AF_UNIX;
		sep->se_ctrladdr_size = n +
			sizeof sep->se_ctrladdr_un.sun_family;
		setup(sep);
		break;
	case AF_INET:
		sep->se_ctrladdr_in.sin_family = AF_INET;
		sep->se_ctrladdr_size = sizeof sep->se_ctrladdr_in;
		if (isrpcservice(sep)) {
			struct rpcent *rp;
			
			sep->se_rpcprog = atoi(sep->se_service);
			if (sep->se_rpcprog == 0) {
				rp = getrpcbyname(sep->se_service);
				if (rp == 0) {
					syslog(LOG_ERR,
					       "%s: unknown service",
					       sep->se_service);
					return;
				}
				sep->se_rpcprog = rp->r_number;
			}
			if (sep->se_fd == -1)
				setup(sep);
			if (sep->se_fd != -1)
				register_rpc(sep);
		} 
		else {
			u_short port = htons(atoi(sep->se_service));
			
			if (!port) {
				struct servent *sp;
				sp = getservbyname(sep->se_service,
						   sep->se_proto);
				if (sp == 0) {
					syslog(LOG_ERR,
					       "%s: unknown service",
					       service_name(sep));
					return;
				}
				port = sp->s_port;
			}
			if (port != sep->se_ctrladdr_in.sin_port) {
				sep->se_ctrladdr_in.sin_port = port;
				if (sep->se_fd != -1) {
					closeit(sep);
				}
			}
			if (sep->se_fd == -1)
				setup(sep);
		}
	}
}

void
config(int signum)
{
	register struct servtab *sep, **sepp;

	(void)signum;

	if (!setconfig()) {
		syslog(LOG_ERR, "%s: %m", configfile);
		return;
	}
	for (sep = servtab; sep; sep = sep->se_next)
		sep->se_checked = 0;
#if 0 /* old version */
	while ((cp = getconfigent())!=NULL) {
		loadconfigent(cp);
	}
#else
	loadconfigfile(loadconfigent);
#endif

	endconfig();
	/*
	 * Purge anything not looked at above.
	 */
	sepp = &servtab;
	while ((sep = *sepp) != NULL) {
		if (sep->se_checked) {
			sepp = &sep->se_next;
			continue;
		}
		*sepp = sep->se_next;
		if (sep->se_fd != -1) {
			closeit(sep);
		}
		if (isrpcservice(sep))
			unregister_rpc(sep);
		if (sep->se_family == AF_UNIX)
			(void)unlink(sep->se_service);
		if (debug)
			print_service("FREE", sep);
		freeconfig(sep);
		free((char *)sep);
	}
}

/********* SIGALRM handler ******************************/

void
restart_services(void)
{
	struct servtab *sep;
	for (sep = servtab; sep; sep = sep->se_next) {
		if (sep->se_fd == -1) {
			switch (sep->se_family) {
			case AF_UNIX:
			case AF_INET:
				setup(sep);
				if (sep->se_fd != -1 && isrpcservice(sep))
					register_rpc(sep);
				break;
			}
		}
	}
}



