/*
 * Internet services provided internally by inetd:
 */

#include <sys/types.h>
#include <sys/time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/un.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "servtab.h"
#include "builtins.h"
#include "setproctitle.h"

#define MINUDPSRCPORT	1024	/* ignore inbound udp on low-number ports */
#define	BUFSIZE	4096

char builtins_rcsid[] = 
  "$Id: builtins.c,v 1.5 2000/07/22 20:13:07 dholland Exp $";

static void
do_setproctitle(char *a, int s)
{
	struct sockaddr_in sn;
	socklen_t size = sizeof(sn);

	if (getpeername(s, (struct sockaddr *)&sn, &size) == 0) {
		setproctitle("-%s [%s]", a, inet_ntoa(sn.sin_addr));
	}
	else {
		setproctitle("-%s", a); 
	}
}



/* Echo service -- echo data back */
/* ARGSUSED */
void
echo_stream(int s, struct servtab *sep)
{
	char buffer[BUFSIZE];
	int i;

	do_setproctitle(sep->se_service, s);
	while ((i = read(s, buffer, sizeof(buffer))) > 0 &&
	    write(s, buffer, i) > 0)
		;
	exit(0);
}

/* ARGSUSED */
/* Echo service -- echo data back */
void
echo_dg(int s, struct servtab *sep)
{
	char buffer[BUFSIZE];
	int i, port;
/* 	size_t size; */
	socklen_t size;
/*	struct sockaddr sa; */
	struct sockaddr_in sa;

	(void)sep;

	size = sizeof(sa);
	i = recvfrom(s, buffer, sizeof(buffer), 0, 
		     (struct sockaddr *)&sa, &size);
	if (i < 0)
		return;
	port = sa.sin_port;
	if (ntohs(port) < MINUDPSRCPORT) 
		return;
	(void) sendto(s, buffer, i, 0, (struct sockaddr *)&sa, sizeof(sa));
}

/* Discard service -- ignore data */
/* ARGSUSED */
void
discard_stream(int s, struct servtab *sep)
{
	char buffer[BUFSIZE];

	do_setproctitle(sep->se_service, s);
	while ((errno = 0, read(s, buffer, sizeof(buffer)) > 0) ||
			errno == EINTR)
		;
	exit(0);
}

/* ARGSUSED */
/* Discard service -- ignore data */
void
discard_dg(int s, struct servtab *sep)
{
	char buffer[BUFSIZE];
	(void)sep;
	read(s, buffer, sizeof(buffer));
}

#include <ctype.h>
#define LINESIZ 72
char ring[128];
char *endring;

static void
initring(void)
{
	register int i;

	endring = ring;

	for (i = 0; i <= 128; ++i)
		if (isprint(i))
			*endring++ = i;
}

/* Character generator */
/* ARGSUSED */
void
chargen_stream(int s, struct servtab *sep)
{
	register char *rs;
	int len;
	char text[LINESIZ+2];

	do_setproctitle(sep->se_service, s);

	if (!endring) {
		initring();
		rs = ring;
	}

	text[LINESIZ] = '\r';
	text[LINESIZ + 1] = '\n';
	for (rs = ring;;) {
		if ((len = endring - rs) >= LINESIZ)
			bcopy(rs, text, LINESIZ);
		else {
			bcopy(rs, text, len);
			bcopy(ring, text + len, LINESIZ - len);
		}
		if (++rs == endring)
			rs = ring;
		if (write(s, text, sizeof(text)) != sizeof(text))
			break;
	}
	exit(0);
}

/* ARGSUSED */
/* Character generator */
void
chargen_dg(int s, struct servtab *sep)
{
/*	struct sockaddr sa; */
	struct sockaddr_in sa;
	static char *rs;
	size_t len;
	socklen_t size;
	char text[LINESIZ+2];
	int port;

	(void)sep;

	if (endring == 0) {
		initring();
		rs = ring;
	}

	size = sizeof(sa);
	if (recvfrom(s, text, sizeof(text), 0, 
		     (struct sockaddr *)&sa, &size) < 0)
		return;

	port = sa.sin_port;
	if (ntohs(port)<MINUDPSRCPORT)
		return;

	if ((len = endring - rs) >= LINESIZ)
		bcopy(rs, text, LINESIZ);
	else {
		bcopy(rs, text, len);
		bcopy(ring, text + len, LINESIZ - len);
	}
	if (++rs == endring)
		rs = ring;
	text[LINESIZ] = '\r';
	text[LINESIZ + 1] = '\n';
	(void) sendto(s, text, sizeof(text), 0, 
		      (struct sockaddr *)&sa, sizeof(sa));
}

/*
 * Return a machine readable date and time, in the form of the
 * number of seconds since midnight, Jan 1, 1900.  Since gettimeofday
 * returns the number of seconds since midnight, Jan 1, 1970,
 * we must add 2208988800 seconds to this figure to make up for
 * some seventy years Bell Labs was asleep.
 *
 * This is already overflowing signed 32-bit long - it will overflow 32-bit 
 * unsigned long in 2036. No clue what to do then; probably nothing, since
 * nobody uses this service.
 */

static 
unsigned long
machtime(void)
{
	struct timeval tv;

	if (gettimeofday(&tv, (struct timezone *)0) < 0) {
		fprintf(stderr, "Unable to get time of day\n");
		return (0L);
	}
	return (htonl((unsigned long)tv.tv_sec + 2208988800UL));
}

void
machtime_stream(int s, struct servtab *sep)
{
	unsigned long result;
	(void)sep;

	result = machtime();
	write(s, (char *) &result, sizeof(result));
}

void
machtime_dg(int s, struct servtab *sep)
{
	unsigned long result;
/*	struct sockaddr sa; */
	struct sockaddr_in sa;
/*	size_t size; */
	socklen_t size;
	int port;
	(void)sep;

	size = sizeof(sa);
	if (recvfrom(s, (char *)&result, sizeof(result), 0, 
		     (struct sockaddr *)&sa, &size) < 0)
		return;
	port = sa.sin_port;
	if (ntohs(port) < MINUDPSRCPORT)
		return;
	result = machtime();
	(void) sendto(s, (char *) &result, sizeof(result), 0, 
		      (struct sockaddr *)&sa, sizeof(sa));
}

/* Return human-readable time of day */
void
daytime_stream(int s, struct servtab *sep)
{
	char buffer[256];
	time_t clocc;

	(void)sep;

	clocc = time(NULL);
	snprintf(buffer, sizeof(buffer), "%.24s\r\n", ctime(&clocc));
	write(s, buffer, strlen(buffer));
}

/* Return human-readable time of day */
void
daytime_dg(int s, struct servtab *sep)
{
	char buffer[256];
	time_t clocc;
	struct sockaddr_in sa;
/*	size_t size; */
	socklen_t size;
	int port;

	(void)sep;

	clocc = time(NULL);
	size = sizeof(sa);
	if (recvfrom(s, buffer, sizeof(buffer), 0, 
		     (struct sockaddr *)&sa, &size) < 0)
		return;
	port = sa.sin_port;
	if (ntohs(port) < MINUDPSRCPORT)
		return;
	snprintf(buffer, sizeof(buffer), "%.24s\r\n", ctime(&clocc));
	sendto(s, buffer, strlen(buffer), 0, 
	       (struct sockaddr *)&sa, sizeof(sa));
}
