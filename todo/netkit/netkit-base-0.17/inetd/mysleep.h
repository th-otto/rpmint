
#if defined __linux__ && (!defined(__GLIBC__) || (__GLIBC__ < 2))
/*
 * Linux libc 5. sleep() is implemented in terms of alarm() and sigpause().
 * This doesn't work, since inetd uses alarm itself.
 */
#define USE_MYSLEEP
#endif /* linux & libc5 */



#ifndef USE_MYSLEEP
#define mysleep(s) sleep(s)
#else
void mysleep(int);
#endif
