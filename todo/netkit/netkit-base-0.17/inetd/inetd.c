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

char copyright[] =
  "@(#) Copyright (c) 1983 Regents of the University of California.\n"
  "All rights reserved.\n";

/*
 * From: @(#)inetd.c	5.30 (Berkeley) 6/3/91
 */
char rcsid[] = 
  "$Id: inetd.c,v 1.38 2000/07/24 23:48:34 dholland Exp $";

#include "../version.h"

/*
 * Inetd - Internet super-server
 *
 * This program invokes all internet services as needed.
 * connection-oriented services are invoked each time a
 * connection is made, by creating a process.  This process
 * is passed the connection as file descriptor 0 and is
 * expected to do a getpeername to find out the source host
 * and port.
 *
 * Datagram oriented services are invoked when a datagram
 * arrives; a process is created and passed a pending message
 * on file descriptor 0.  Datagram servers may either connect
 * to their peer, freeing up the original socket for inetd
 * to receive further messages on, or ``take over the socket'',
 * processing all arriving datagrams and, eventually, timing
 * out.	 The first type of server is said to be ``multi-threaded'';
 * the second type of server ``single-threaded''. 
 *
 * Inetd uses a configuration file which is read at startup
 * and, possibly, at some later time in response to a hangup signal.
 * The configuration file is ``free format'' with fields given in the
 * order shown below.  Continuation lines for an entry must being with
 * a space or tab.  All fields must be present in each entry.
 *
 *	service name			must be in /etc/services
 *	socket type			stream/dgram/raw/rdm/seqpacket
 *	protocol			must be in /etc/protocols
 *	wait/nowait[.max]		single-threaded/multi-threaded, max #
 *	user[.group]			user/group to run daemon as
 *	server program			full path name
 *	server program arguments	maximum of MAXARGS (20)
 *
 * For RPC services
 *      service name/version            must be in /etc/rpc
 *	socket type			stream/dgram/raw/rdm/seqpacket
 *	protocol			must be in /etc/protocols
 *	wait/nowait[.max]		single-threaded/multi-threaded
 *	user[.group]			user to run daemon as
 *	server program			full path name
 *	server program arguments	maximum of MAXARGS (20)
 *
 * Comment lines are indicated by a `#' in column 1.
 */

/*
 * Here's the scoop concerning the user.group feature:
 *
 * 1) No group listed.
 * 
 * 	a) for root:	NO setuid() or setgid() is done
 * 
 * 	b) nonroot:	setuid()
 * 			setgid(primary group as found in passwd)
 * 			initgroups(name, primary group)
 * 
 * 2) set-group-option on.
 * 
 * 	a) for root:	NO setuid()
 * 			setgid(specified group)
 * 			setgroups(1, specified group)
 * 
 * 	b) nonroot:	setuid()
 * 			setgid(specified group)
 * 			initgroups(name, specified group)
 * 
 * All supplementary groups are discarded at startup in case inetd was
 * run manually.
 */

#include <sys/types.h>
#include <sys/param.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/file.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/un.h>

#include <netinet/in.h>
#include <arpa/inet.h>  /* for inet_ntoa */

#include <errno.h>
#include <netdb.h>
#include <syslog.h>
#include <pwd.h>
#include <grp.h>
#include <stdio.h>
#include <string.h>
#include <getopt.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>

#if !defined(__linux__) && !defined(__MINT__)
#ifndef RLIMIT_NOFILE
#define RLIMIT_NOFILE	RLIMIT_OFILE
#endif
#endif

#include "pathnames.h"
#include "inetd.h"
#include "servtab.h"
#include "sig.h"
#include "daemon.h"
#include "setproctitle.h"
#include "mysleep.h"

#ifdef RPC   /* must come after inetd.h, which defines RPC */
/* work around a compiler warning in rpc.h in libc5 */
#define __wait __wait_foo
#include <rpc/rpc.h>
#include <rpc/pmap_clnt.h>
#undef __wait
#endif
#include <rpc/pmap_clnt.h>

#ifndef MIN
#define MIN(a, b)	((a) < (b) ? (a) : (b))
#endif

#ifdef __MINT__
#define DEFAULT_FILE_LIMIT	32
#else
#define DEFAULT_FILE_LIMIT	1024
#endif

/* Reserve some descriptors, 3 stdio + at least: 1 log, 1 conf. file */
#define FD_MARGIN	(8)


static void logpid(void);
static int bump_nofile(void);

static void attempt_to_restart(void);

struct servtab *servtab;                     /* service table */
const char *configfile = _PATH_INETDCONF;    /* config file path */
int debug = 0;                               /* debug flag */

/* Length of socket listen queue. Should be per-service probably. */
static int 	global_queuelen = 128;

static volatile int	nsock;
static int		maxsock;
static fd_set		allsock;
static int		options;
static int		timingout;

static long rlim_ofile_cur = DEFAULT_FILE_LIMIT;

#ifdef RLIMIT_NOFILE
struct rlimit	rlim_ofile;
#endif




#ifdef sun
/*
 * Sun's RPC library caches the result of `dtablesize()'
 * This is incompatible with our "bumping" of file descriptors "on demand"
 */
int
_rpc_dtablesize()
{
	return rlim_ofile_cur;
}
#endif

/*
 * Remove things from environ[] that might have been inherited from the
 * parent process if we were started by root from a shell without "env -".
 * But, only remove the things that we can be reasonably sure are not 
 * intended to be inherited by inetd's children, because such things might
 * have been deliberately set in /etc/rc.
 *
 * In the long run we need to be able to explicitly specify environment in
 * inetd.conf. Then we can just clear the environment, which is much 
 * simpler.
 */
static
void
discard_stupid_environment(void)
{
	static const char *const junk[] = {
		/* these are prefixes */
		"CVS",
		"DISPLAY=",
		"EDITOR=",
		"GROUP=",
		"HOME=",
		"IFS=",
		"LD_",
		"LOGNAME=",
		"MAIL=",
		"PATH=",
		"PRINTER=",
		"PWD=",
		"SHELL=",
		"SHLVL=",
		"SSH",
		"TERM",
		"TMP",
		"USER=",
		"VISUAL=",
		NULL
	};

	int i,k=0;
	for (i=0; environ[i]; i++) {
		int found=0, j;
		for (j=0; junk[j]; j++) {
			if (!strncmp(environ[i], junk[j], strlen(junk[j]))) {
				found=1;
			}
		}
		if (!found) {
			environ[k++] = environ[i];
		}
	}
	environ[k] = NULL;
}


/*
 * Exec a child, or run a builtin that's meant to be a subprocess.
 * (Not reached in the parent inetd process.)
 */
static
void
exec_child(struct servtab *sep)
{
	struct passwd *pwd;
	struct group *grp = NULL;
	int tmpint;
	uid_t uid;
	gid_t gid;

	/* 
	 * If debugging, we're in someone else's session; make a new one.
	 */
	if (debug) {
		setsid();
	}

	/*
	 * Prepare to exec.
	 */

	pwd = getpwnam(sep->se_user);
	if (pwd == NULL) {
		syslog(LOG_ERR, "getpwnam: %s: No such user", sep->se_user);
		return;
	}

	/*
	 * Use the uid and gid of the user.
	 */
	uid = pwd->pw_uid;
	gid = pwd->pw_gid;

	/*
	 * If a group was specified, use its gid instead of the user's gid.
	 */
	if (sep->se_group) {
		grp = getgrnam(sep->se_group);
		if (grp == NULL) {
			syslog(LOG_ERR, "getgrnam: %s: No such group",
			       sep->se_group);
			return;
		}
		gid = grp->gr_gid;
	}

	/*
	 * If a nonroot user, do initgroups to run with that user's group
	 * list. 
	 *
	 * But if root, do not use root's group list - just use the one gid.
	 *
	 * If no group was specified, keep the group inetd was run under.
	 * This is the traditional behavior, but seems dumb - shouldn't
	 * we use the group from the password file? XXX.
	 */

	if (uid) {
		if (setgid(gid)) {
			syslog(LOG_AUTH|LOG_ERR, "setgid: %m");
			return;
		}
		if (initgroups(pwd->pw_name, gid)) {
			syslog(LOG_AUTH|LOG_ERR, "initgroups: %m");
			return;
		}
		if (setuid(uid)) {
			syslog(LOG_AUTH|LOG_ERR, "setuid: %m");
			return;
		}
		/*
		 * Just a bit of extra paranoia.
		 */
		seteuid(0);
		if (getuid()==0 || geteuid()==0) {
			syslog(LOG_AUTH|LOG_ERR, "Failed to drop root");
			return;
		}
	} 
	else if (grp) {
		if (setgid(gid)) {
			syslog(LOG_AUTH|LOG_ERR, "setgid: %m");
			return;
		}
		if (setgroups(1, &gid)) {
			syslog(LOG_AUTH|LOG_ERR, "setgroups: %m");
			return;
		}
	}

	if (debug) {
		gid_t tmp[NGROUPS_MAX];
		int n, i;
		fprintf(stderr, "pid %d: exec %s\n", getpid(), sep->se_server);
		fprintf(stderr, "uid: %d  gid: %d\n", getuid(), getgid());
		fprintf(stderr, "groups: ");
		n = getgroups(NGROUPS_MAX, tmp);
		for (i=0; i<n; i++) fprintf(stderr, "%d ", tmp[i]);
		fprintf(stderr, "\n");
	}

#ifdef MULOG
	if (sep->se_log) {
		dolog(sep, 0);
	}
#endif

#ifdef RLIMIT_NOFILE
	if (rlim_ofile.rlim_cur != rlim_ofile_cur) {
		if (setrlimit(RLIMIT_NOFILE, &rlim_ofile) < 0) {
			syslog(LOG_ERR,"setrlimit: %m");
		}
	}
#endif

	/* 
	 * Transfer stdout to stderr. This is not with the other dup2's
	 * so debug logging works.
	 */
	dup2(1, 2);
	for (tmpint = rlim_ofile_cur-1; tmpint > 2; tmpint--) {
		close(tmpint);
	}
	
	sig_preexec();

	/*
	 * If a builtin, now run it instead of execing.
	 */
	if (sep->se_bi) {
		(*sep->se_bi->bi_fn)(0, sep);
		exit(0);
	}
	
	execv(sep->se_server, sep->se_argv);
	syslog(LOG_ERR, "execv %s: %m", sep->se_server);
}

static
pid_t
fork_child(struct servtab *sep)
{
	pid_t pid;

	if (sep->se_count++ == 0) {
		gettimeofday(&sep->se_time, NULL);
	}
	else if (sep->se_count >= sep->se_max) {
		struct timeval now;

		gettimeofday(&now, (struct timezone *)0);
		if (now.tv_sec - sep->se_time.tv_sec > CNT_INTVL) {
			sep->se_time = now;
			sep->se_count = 1;
		} 
		else {
			syslog(LOG_ERR, "%s server failing (looping or "
			       "being flooded), service terminated for "
			       "%d min\n",
			       service_name(sep),
			       RETRYTIME/60);

			FD_CLR(sep->se_fd, &allsock);
			close(sep->se_fd);
			sep->se_fd = -1;

			sep->se_count = 0;
			nsock--;
			if (!timingout) {
				timingout = 1;
				alarm(RETRYTIME);
			}
			return -1;
		}
	}
	pid = fork();
	if (pid<0) {
		syslog(LOG_ERR, "fork: %m");
	}
	return pid;
}

static
void
launch(struct servtab *sep)
{
	char buf[50];
	int ctrl, dofork;

	if (debug) {
		fprintf(stderr, "launching: %s\n", sep->se_service);
	}

	if (!sep->se_wait && sep->se_socktype == SOCK_STREAM) {
		/* Do nonblocking accept, just in case */
		fcntl(sep->se_fd, F_SETFL, O_NDELAY);
		ctrl = accept(sep->se_fd, NULL, NULL);
		fcntl(sep->se_fd, F_SETFL, 0);

		if (debug) {
			fprintf(stderr, "accept: new socket %d\n", ctrl);
		}

		if (ctrl < 0) {
			if (errno != EINTR && errno != EWOULDBLOCK) {
				syslog(LOG_WARNING, "accept (for %s): %m",
				       sep->se_service);
			}
			if (errno == EMFILE) {
				syslog(LOG_ALERT, 
				       "Out of files! Attempting restart...");
				attempt_to_restart();
			}
			return;
		}
	} 
	else {
		ctrl = sep->se_fd;
	}

	dofork = (sep->se_bi == NULL || sep->se_bi->bi_fork);
	if (dofork) {
		pid_t pid = fork_child(sep);
		if (pid < 0) {
			if (ctrl != sep->se_fd)
				close(ctrl);
			mysleep(1);
			return;
		}
		if (pid==0) {
			/* child */
			dup2(ctrl, 0);
			close(ctrl);
			dup2(0, 1);
			/* don't do stderr yet */
			exec_child(sep);
			if (sep->se_socktype != SOCK_STREAM)
				recv(0, buf, sizeof (buf), 0);
			_exit(1);
		}
		if (sep->se_wait) {
			sep->se_wait = pid;
			FD_CLR(sep->se_fd, &allsock);
			nsock--;
		}
		if (!sep->se_wait && sep->se_socktype == SOCK_STREAM)
			close(ctrl);
	}
	else {
		sep->se_bi->bi_fn(ctrl, sep);
		if (ctrl != sep->se_fd)
			close(ctrl);
	}
}

static
void
mainloop(void)
{
	struct servtab *sep;

	int n, i;
	fd_set readable;

	sig_block();

	syslog(LOG_INFO, "Online and ready (%d sockets)", nsock);

	for (;;) {
		/*
		 * If there are no live sockets, hold until we have some.
		 * (Is this necessary? Wouldn't the select just wait until
		 * it got signaled?)
		 */
		if (nsock == 0) {
			while (nsock == 0) {
				sig_wait();
			}
		}


		readable = allsock;

		sig_unblock();
		n = select(maxsock + 1, &readable, NULL, NULL, NULL);
		sig_block();

		if (n <= 0) {
			if (n < 0 && errno != EINTR) {
				syslog(LOG_WARNING, "select: %m");
				mysleep(1);
			}
			continue;
		}

		/*
		 * Was:
		 * for (sep = servtab; n && sep; sep = sep->se_next)
		 *   if (sep->se_fd != -1 && FD_ISSET(sep->se_fd, &readable)) {
		 *      n--;
                 *      launch(sep);
		 */

		for (i=3; i<=maxsock; i++) {
			if (FD_ISSET(i, &readable)) {
				sep = find_service_by_fd(i);
				if (sep==NULL || sep->se_fd<0) {
					/* ? */
					syslog(LOG_ERR, 
					       "selected closed socket!?");
					continue;
				}
				launch(sep);
			}
		}
	}
}

/*
 * Saved state so we can try to restart.
 */
static int got_dflag=0, got_iflag=0, got_qflag=0, got_conf=0;

static
void
attempt_to_restart(void)
{
	struct stat statbuf;
	const char *argv[6];
	const char **tmpargv1;
	char **tmpargv2;
	char qbuf[16];
	int i=0;
	snprintf(qbuf, sizeof(qbuf), "-q%d", global_queuelen);
	argv[i++] = "inetd";
	if (got_dflag) argv[i++] = "-d";
	if (got_iflag) argv[i++] = "-i";
	if (got_qflag) argv[i++] = qbuf;
	if (got_conf) argv[i++] = configfile;
	argv[i] = NULL;

	if (stat(_PATH_INETD, &statbuf)!=0 || (statbuf.st_mode & 0111)==0) {
		/*
		 * Cannot restart - inetd is not there or not executable
		 */
		syslog(LOG_ALERT, "Cannot restart.");
		syslog(LOG_ALERT, "Recommend manually restarting inetd ASAP.");
		
		/*
		 * Hopefully this will help the situation and not make too
		 * much a mess of the internal state.
		 */
		for (i=getdtablesize()-1; i>=64; i--) close(i);
		return;
	}

	/*
	 * At this point we're committed to restarting.
	 * Note that we have to close everything before execing the new
	 * inetd, or it won't be able to listen on the ports we've got
	 * bound.
	 */

	for (i=getdtablesize()-1; i>2; i--) {
		shutdown(i,2);
		close(i);
	}

	/* should we try argv[0] first? probably not */
	tmpargv1 = argv;
	/* grr */
	/*tmpargv2 = (char **)tmpargv1;*/
	memcpy(&tmpargv2, &tmpargv1, sizeof(tmpargv1));

	mysleep(10);

	execv(_PATH_INETD, tmpargv2);

	/* Should this be EMERG? */
	closelog();
	openlog("inetd", LOG_PID, LOG_DAEMON);
	syslog(LOG_ALERT, "Restart attempt failed.");
	syslog(LOG_ALERT, "Recommend manually restarting inetd ASAP.");

	/* this may help restore us to a semi-operable state */
	{
		const char *tmp = configfile;
		configfile = "/dev/null";
		config(0);
		configfile = tmp;
		config(0);
	}
}

int
main(int argc, char *argv[], char *envp[])
{
	int ch;
	int nodaemon=0;
	gid_t gid;
	char *progname;

	gid = getgid();
	setgroups(1, &gid);

	/*
	 * Note that Linux, unlike 4.4BSD, needs to clobber the
	 * environment space for setproctitle. If the total size
	 * of the argv and envp strings isn't enough, you won't
	 * see anything. In fact, it may not even show "inetd", only
	 * "ine" or "in". There's nothing that can be done about this,
	 * except run inetd with the full pathname and some long 
	 * environment variables, or hack 4.4BSD-style setproctitle
	 * support into Linux.
	 * 
	 * Note that the setproctitle implementation copies the environment,
	 * so child processes won't be sent trash.
	 *
	 * Also note that we only setproctitle() in child processes, so
	 * our progname pointer and the like remain valid.
	 */

	initsetproctitle(argc, argv, envp);

	/*
	 * This must come _after_ initsetproctitle.
	 */
	discard_stupid_environment();
	
	progname = strrchr(argv[0], '/');
	if (progname == NULL) {
		progname = argv[0];
	}
	else {
		progname++;
	}

	while ((ch = getopt(argc, argv, "diq:")) != EOF)
		switch(ch) {
		case 'd':
			debug = nodaemon = 1;
			options |= SO_DEBUG;
			got_dflag = 1;
			break;
		case 'i':
			nodaemon = 1;
			got_iflag = 1;
			break;
		case 'q':
		        global_queuelen = atoi(optarg);
			if (global_queuelen < 8) global_queuelen=8;
			got_qflag = 1;
			break;
		case '?':
		default:
			fprintf(stderr, "usage: %s [-di] [-q len] [conf]",
				progname);
			exit(1);
		}
	argc -= optind;
	argv += optind;

	if (argc > 0) {
		configfile = argv[0];
		got_conf = 1;
	}

	if (nodaemon == 0) {
		daemon(0, 0);
	}
	else if (debug == 0) {
		/*
		 * If nodaemon mode, but not debug mode, run in our own
		 * session. Init might have done this for us if we're being 
		 * spawned from init... but it might not have.
		 */
		setsid();
	}

	openlog(progname, LOG_PID | LOG_NOWAIT, LOG_DAEMON);
	logpid();

#ifdef RLIMIT_NOFILE
	rlim_ofile_cur = DEFAULT_FILE_LIMIT;
	if (getrlimit(RLIMIT_NOFILE, &rlim_ofile) < 0) {
		syslog(LOG_ERR, "getrlimit: %m");
	} else if (rlim_ofile.rlim_cur != RLIM_INFINITY) {
		rlim_ofile_cur = rlim_ofile.rlim_cur;
	}
#endif

	config(0);

	sig_init();

	mainloop();

	/* Not reachable */
	return 0;
}

void
reapchild(int signum)
{
	int status;
	pid_t pid;
	register struct servtab *sep;
	const char *name;
	char tmp[64];

	(void)signum;

	while ((pid = wait3(&status, WNOHANG, NULL)) > 0) {
		if (debug) {
			fprintf(stderr, "pid %d, exit status %x\n", pid, 
				status);
		}

		sep = find_service_by_pid(pid);
		if (sep==NULL) {
			snprintf(tmp, sizeof(tmp), "pid %d", (int)pid);
			name = tmp;
		}
		else {
			snprintf(tmp, sizeof(tmp), "%s (pid %d)", 
				 sep->se_server, (int)pid);
			name = tmp;
		}

		if (WIFEXITED(status) && WEXITSTATUS(status)) {
			syslog(LOG_WARNING, "%s: exit status %d", name,
			       WEXITSTATUS(status));
		}
		else if (WIFSIGNALED(status)) {
			syslog(LOG_WARNING, "%s: exit signal %d", name,
			       WTERMSIG(status));
		}

		if (sep!=NULL) {
			sep->se_wait = 1;
			FD_SET(sep->se_fd, &allsock);
			nsock++;
			if (debug) {
				fprintf(stderr, "restored %s, fd %d\n",
					sep->se_service, sep->se_fd);
			}
		}
	}
}

void
retry(int signum)
{
	(void)signum;

	timingout = 0;

	restart_services();
}

void
goaway(int signum)
{
	register struct servtab *sep;

	(void)signum;
	for (sep = servtab; sep; sep = sep->se_next) {
		if (sep->se_fd == -1)
			continue;

		switch (sep->se_family) {
		case AF_UNIX:
			(void)unlink(sep->se_service);
			break;
		case AF_INET:
			if (sep->se_wait == 1 && isrpcservice(sep))
				unregister_rpc(sep);
			break;
		}
		(void)close(sep->se_fd);
	}
	(void)unlink(_PATH_INETDPID);
	exit(0);
}

void
closeit(struct servtab *sep)
{
	FD_CLR(sep->se_fd, &allsock);
	nsock--;
	(void) close(sep->se_fd);
	sep->se_fd = -1;
}

void
setup(struct servtab *sep)
{
	int on = 1;

	if ((sep->se_fd = socket(sep->se_family, sep->se_socktype, 0)) < 0) {
		syslog(LOG_ERR, "%s: socket: %m", service_name(sep),
		    sep->se_service, sep->se_proto);

		if (errno == EMFILE) {
			syslog(LOG_ALERT, 
			       "Out of files! Attempting restart...");
			attempt_to_restart();
		}
		return;
	}
#define	turnon(fd, opt) \
setsockopt(fd, SOL_SOCKET, opt, (char *)&on, sizeof (on))
	if (strcmp(sep->se_proto, "tcp") == 0 && (options & SO_DEBUG) &&
	    turnon(sep->se_fd, SO_DEBUG) < 0)
		syslog(LOG_ERR, "setsockopt (SO_DEBUG): %m");
	if (turnon(sep->se_fd, SO_REUSEADDR) < 0)
		syslog(LOG_ERR, "setsockopt (SO_REUSEADDR): %m");
#undef turnon
	if (bind(sep->se_fd, &sep->se_ctrladdr, sep->se_ctrladdr_size) < 0) {
		syslog(LOG_ERR, "%s: bind: %m", service_name(sep),
		    sep->se_service, sep->se_proto);
		(void) close(sep->se_fd);
		sep->se_fd = -1;
		if (!timingout) {
			timingout = 1;
			alarm(RETRYTIME);
		}
		return;
	}
	if (sep->se_socktype == SOCK_STREAM)
		listen(sep->se_fd, global_queuelen);

	if (sep->se_family == AF_UNIX) {
		/* 
		 * Ignore any error, on the grounds that chmod on a socket
		 * might not be possible on some systems.
		 *
		 * XXX in the long run there should be a config option for
		 * the mode. And owner/group, too.
		 */
		chmod(sep->se_ctrladdr_un.sun_path, 0666);
	}

	FD_SET(sep->se_fd, &allsock);
	nsock++;
	if (sep->se_fd > maxsock) {
		maxsock = sep->se_fd;
		if (maxsock > rlim_ofile_cur - FD_MARGIN)
			bump_nofile();
	}
}

void
register_rpc(struct servtab *sep)
{
#ifdef RPC
/*	size_t m; */
	socklen_t m;
	int i;
	struct sockaddr_in sn;
	struct protoent *pp;

	if ((pp = getprotobyname(sep->se_proto+4)) == NULL) {
		syslog(LOG_ERR, "%s: getproto: %m",
		    sep->se_proto);
		return;
	}
	m = sizeof(sn);
	if (getsockname(sep->se_fd, (struct sockaddr *)&sn, &m) < 0) {
		syslog(LOG_ERR, "%s: getsockname: %m", service_name(sep),
		    sep->se_service, sep->se_proto);
		return;
	}

	for (i = sep->se_rpcversl; i <= sep->se_rpcversh; i++) {
		if (debug)
			fprintf(stderr, "pmap_set: %u %u %u %u\n",
				sep->se_rpcprog, i, 
				pp->p_proto, ntohs(sn.sin_port));
		(void)pmap_unset(sep->se_rpcprog, i);
		if (!pmap_set(sep->se_rpcprog, i, pp->p_proto, ntohs(sn.sin_port)))
			syslog(LOG_ERR, "pmap_set: %u %u %u %u: %m",
			       sep->se_rpcprog, i, 
			       pp->p_proto, ntohs(sn.sin_port));
	}
#endif /* RPC */
}

void
unregister_rpc(struct servtab *sep)
{
#ifdef RPC
	int n;

	for (n = sep->se_rpcversl; n <= sep->se_rpcversh; n++) {
		if (debug)
			fprintf(stderr, "pmap_unset(%u, %u)\n",
				sep->se_rpcprog, n);
		if (!pmap_unset(sep->se_rpcprog, n))
			syslog(LOG_ERR, "pmap_unset(%u, %u)\n",
				sep->se_rpcprog, n);
	}
#endif /* RPC */
}


struct servtab *
enter(struct servtab *cp)
{
	register struct servtab *sep;

	sep = domalloc(sizeof(*sep));
	*sep = *cp;
	sep->se_fd = -1;
	sep->se_rpcprog = -1;
	sep->se_next = servtab;
	servtab = sep;
	return (sep);
}

//static char *skip(char **);
//static char *nextline(FILE *);







static void
logpid(void)
{
	FILE *fp;

	if ((fp = fopen(_PATH_INETDPID, "w")) != NULL) {
		fprintf(fp, "%u\n", getpid());
		(void)fclose(fp);
	}
}

static int
bump_nofile(void)
{
#ifdef RLIMIT_NOFILE

#define FD_CHUNK	32

	struct rlimit rl;

	if (getrlimit(RLIMIT_NOFILE, &rl) < 0) {
		syslog(LOG_ERR, "getrlimit: %m");
		return -1;
	}
	rl.rlim_cur = MIN(rl.rlim_max, rl.rlim_cur + FD_CHUNK);
	if (rl.rlim_cur <= rlim_ofile_cur) {
		syslog(LOG_ERR,
			"bump_nofile: cannot extend file limit, max = %d",
			rl.rlim_cur);
		return -1;
	}

	if (setrlimit(RLIMIT_NOFILE, &rl) < 0) {
		syslog(LOG_ERR, "setrlimit: %m");
		return -1;
	}

	rlim_ofile_cur = rl.rlim_cur;
	return 0;

#else
	syslog(LOG_ERR, "bump_nofile: cannot extend file limit");
	return -1;
#endif
}




#ifdef MULOG
dolog(sep, ctrl)
	struct servtab *sep;
	int		ctrl;
{
	struct sockaddr		sa;
	struct sockaddr_in	*sin = (struct sockaddr_in *)&sa;
	int			len = sizeof(sa);
	struct hostent		*hp;
	char			*host, *dp, buf[BUFSIZ], *rfc931_name();
	int			connected = 1;

	if (sep->se_family != AF_INET)
		return;

	if (getpeername(ctrl, &sa, &len) < 0) {
		if (errno != ENOTCONN) {
			syslog(LOG_ERR, "getpeername: %m");
			return;
		}
		if (recvfrom(ctrl, buf, sizeof(buf), MSG_PEEK, &sa, &len) < 0) {
			syslog(LOG_ERR, "recvfrom: %m");
			return;
		}
		connected = 0;
	}
	if (sa.sa_family != AF_INET) {
		syslog(LOG_ERR, "unexpected address family %u", sa.sa_family);
		return;
	}

	hp = gethostbyaddr((char *) &sin->sin_addr.s_addr,
				sizeof (sin->sin_addr.s_addr), AF_INET);

	host = hp?hp->h_name:inet_ntoa(sin->sin_addr);

	switch (sep->se_log & ~MULOG_RFC931) {
	case 0:
		return;
	case 1:
		if (curdom == NULL || *curdom == '\0')
			break;
		dp = host + strlen(host) - strlen(curdom);
		if (dp < host)
			break;
		if (debug)
			fprintf(stderr, "check \"%s\" against curdom \"%s\"\n",
					host, curdom);
		if (strcasecmp(dp, curdom) == 0)
			return;
		break;
	case 2:
	default:
		break;
	}

	openlog("", LOG_NOWAIT, MULOG);

	if (connected && (sep->se_log & MULOG_RFC931))
		syslog(LOG_INFO, "%s@%s wants %s",
				rfc931_name(sin, ctrl), host, sep->se_service);
	else
		syslog(LOG_INFO, "%s wants %s",
				host, sep->se_service);
}
/*
 * From tcp_log by
 *  Wietse Venema, Eindhoven University of Technology, The Netherlands.
 */
#if 0
static char sccsid[] = "@(#) rfc931.c 1.3 92/08/31 22:54:46";
#endif

#include <setjmp.h>

#define	RFC931_PORT	113		/* Semi-well-known port */
#define	TIMEOUT		4
#define	TIMEOUT2	10

static sigjmp_buf timebuf;

/* timeout - handle timeouts */

static void timeout(sig)
int     sig;
{
	siglongjmp(timebuf, sig);
}

/* rfc931_name - return remote user name */

char *
rfc931_name(struct sockaddr_in *there, int ctrl)
{
	/* "there" is remote link information */
	struct sockaddr_in here;	/* local link information */
	struct sockaddr_in sin;		/* for talking to RFC931 daemon */
	int		length;
	int		s;
	unsigned	remote;
	unsigned	local;
	static char	user[256];		/* XXX */
	char		buf[256];
	char		*cp;
	char		*result = "USER_UNKNOWN";
	int		len;

	/* Find out local port number of our stdin. */

	length = sizeof(here);
	if (getsockname(ctrl, (struct sockaddr *) &here, &length) == -1) {
		syslog(LOG_ERR, "getsockname: %m");
		return (result);
	}
	/* Set up timer so we won't get stuck. */

	if ((s = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
		syslog(LOG_ERR, "socket: %m");
		return (result);
	}

	sin = here;
	sin.sin_port = htons(0);
	if (bind(s, (struct sockaddr *) &sin, sizeof(sin)) == -1) {
		syslog(LOG_ERR, "bind: %m");
		close(s);
		return (result);
	}

	signal(SIGALRM, timeout);
	if (sigsetjmp(timebuf)) {
		close(s);			/* not: fclose(fp) */
		return (result);
	}
	alarm(TIMEOUT);

	/* Connect to the RFC931 daemon. */

	sin = *there;
	sin.sin_port = htons(RFC931_PORT);
	if (connect(s, (struct sockaddr *) &sin, sizeof(sin)) == -1) {
		close(s);
		alarm(0);
		return (result);
	}

	/* Query the RFC 931 server. Would 13-byte writes ever be broken up? */
	snprintf(buf, sizeof(buf), "%u,%u\r\n", 
		 ntohs(there->sin_port), ntohs(here.sin_port));


	for (len = 0, cp = buf; len < strlen(buf); ) {
		int	n;
		if ((n = write(s, cp, strlen(buf) - len)) == -1) {
			close(s);
			alarm(0);
			return (result);
		}
		cp += n;
		len += n;
	}

	/* Read response */
	for (cp = buf; cp < buf + sizeof(buf) - 1; ) {
		char	c;
		if (read(s, &c, 1) != 1) {
			close(s);
			alarm(0);
			return (result);
		}
		if (c == '\n')
			break;
		*cp++ = c;
	}
	*cp = '\0';

	if (sscanf(buf, "%u , %u : USERID :%*[^:]:%255s", &remote, &local, user) == 3
		&& ntohs(there->sin_port) == remote
		&& ntohs(here.sin_port) == local) {

		/* Strip trailing carriage return. */
		if (cp = strchr(user, '\r'))
			*cp = 0;
		result = user;
	}

	alarm(0);
	close(s);
	return (result);
}
#endif
