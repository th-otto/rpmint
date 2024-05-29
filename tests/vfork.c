#include <unistd.h>
#include <stdio.h>

int main(void)
{
	int i;
	pid_t p;
	
	p = vfork();
	if (p == 0)
	{
		for (i = 0; i < 10; i++)
		{
			printf("%d: in child\n", i);
			usleep(500000);
		}
		_exit(0);
	} else if (p == -1)
	{
		printf("cannot fork\n");
	} else
	{
		for (i = 0; i < 10; i++)
		{
			printf("%d: in parent\n", i);
			usleep(500000);
		}
	}
	return 0;
}
