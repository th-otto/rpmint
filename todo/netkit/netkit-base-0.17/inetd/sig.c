#include <signal.h>
#include <string.h>
#include <syslog.h>
#include "sig.h"

static sigset_t blockmask, emptymask;
static int blocked=0;

char sig_rcsid[] = 
  "$Id: sig.c,v 1.2 2000/07/22 20:13:07 dholland Exp $";

void
sig_init(void)
{
	struct sigaction sa;

	sigemptyset(&emptymask);
	sigemptyset(&blockmask);
	sigaddset(&blockmask, SIGCHLD);
	sigaddset(&blockmask, SIGHUP);
	sigaddset(&blockmask, SIGALRM);

	memset(&sa, 0, sizeof(sa));
	sa.sa_mask = blockmask;
	sa.sa_handler = retry;
	sigaction(SIGALRM, &sa, NULL);
	sa.sa_handler = config;
	sigaction(SIGHUP, &sa, NULL);
	sa.sa_handler = reapchild;
	sigaction(SIGCHLD, &sa, NULL);
	sa.sa_handler = goaway;
	sigaction(SIGTERM, &sa, NULL);
	sa.sa_handler = goaway;
	sigaction(SIGINT, &sa,  NULL);
	sa.sa_handler = SIG_IGN;
	sigaction(SIGPIPE, &sa, NULL);
}

void
sig_block(void) {
	sigprocmask(SIG_BLOCK, &blockmask, NULL);
	if (blocked) {
	    syslog(LOG_ERR, "internal error - signals already blocked\n");
	    syslog(LOG_ERR, "please report to netbug@ftp.uk.linux.org\n");
	}
	blocked = 1;
}

void
sig_unblock(void) {
	sigprocmask(SIG_SETMASK, &emptymask, NULL);
	blocked = 0;
}

void
sig_wait(void) {
	sigsuspend(&emptymask);
}

void
sig_preexec(void)
{
	struct sigaction sa;
	memset(&sa, 0, sizeof(sa));
	sa.sa_handler = SIG_DFL;
	sigaction(SIGPIPE, &sa, NULL);

	sig_unblock();
}
