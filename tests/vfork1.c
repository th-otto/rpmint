#include <unistd.h>
#include <stdio.h>

static long trap_1_w_noclobber(int n)
{
	register long __retvalue __asm__("d0");

	__asm__ volatile(
		"movw	%1,%%sp@-\n\t"
		"trap	#1\n\t"
		"addql	#2,%%sp\n\t"
	: "=r"(__retvalue)			/* outputs */
	: "g"(n)				/* inputs  */
	: __CLOBBER_RETURN("d0") "cc"    /* clobbered regs */
	  AND_MEMORY
	);
	return __retvalue;
}


static long getsp(void)
{
	long __retvalue;

	__asm__ volatile(
		"movl	%%sp,%0\n\t"
	: "=r"(__retvalue)			/* outputs */
	:
	: "cc"    /* clobbered regs */
	);
	return __retvalue;
}


#define Pvfork() trap_1_w_noclobber(0x113)

int main(void)
{
	int i;
	pid_t p;
	long sp;
	
	p = Pvfork();
	if (p == 0)
	{
		sp = getsp();
		printf("child sp: %lx ret=%lx\n", sp, (long)__builtin_return_address(0));
		for (i = 0; i < 10; i++)
		{
			printf("%d: in child\n", i);
			usleep(500000);
		}
		_exit(0);
	} else if (p < 0)
	{
		printf("cannot fork\n");
	} else
	{
		sp = getsp();
		printf("parent sp: %lx ret=%lx\n", sp, (long)__builtin_return_address(0));
		for (i = 0; i < 10; i++)
		{
			printf("%d: in parent\n", i);
			usleep(500000);
		}
	}
	return 0;
}
