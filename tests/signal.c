#include <stdio.h>
#include <mint/osbind.h>
#include <mint/mintbind.h>
#include <signal.h>


struct kernel_sigcontext
{
	unsigned long	sc_pc;
	unsigned long	sc_usp;
	unsigned short	sc_sr;
};


static void __CDECL catchit(long sig, long code, long context)
{
	struct kernel_sigcontext *ctxt = (struct kernel_sigcontext *)context;
	fprintf(stderr, "sig=%ld code=%ld context=%08lx %08lx %08lx %04x\n", sig, code, context, ctxt->sc_pc, ctxt->sc_usp, ctxt->sc_sr);
}


int main(void)
{
	int i;
	int pid;
	
	for (i = 1; i < __NSIG; i++)
		if (i != SIGKILL) 
			Psignal(i, catchit);
	pid = Pgetpid();
	for (i = 1; i < __NSIG; i++)
		if (i != SIGKILL && i != SIGSTOP)
			Pkill(pid, i);
	return 0;
}
