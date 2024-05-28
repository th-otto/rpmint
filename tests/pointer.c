#ifdef __FASTCALL__
#define __CDECL __attribute__((__cdecl__))
#else
#define __CDECL
#endif

typedef void __CDECL (*__sighandler_t)(int signum);

__sighandler_t p;

void handler(int sig)
{
	(void)sig;
}

void test(void)
{
	p = handler;
}
