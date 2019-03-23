/* parameters */
#define	TOOMANY		40		/* don't start more than TOOMANY */
#define	CNT_INTVL	60		/*   servers in CNT_INTVL seconds */

#define	RETRYTIME	(60*10)		/* retry time after bind/server fail */

#define RPC                             /* Use SunRPC */


/* globals */
extern const char *configfile;          /* /etc/inetd.conf or alternate */
extern int debug;                       /* debug flag */

/* util functions */
void *domalloc(size_t len);
char *dostrdup(const char *str);
