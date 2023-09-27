#include <stdio.h>


void func_exception(int i)
{
	printf("in %s\n", __func__);
	if (i == 5)
		throw(i);
}

int main(void)
{
	int i;
	
	setvbuf(stderr, NULL, _IONBF, 0);
	printf("Hello, C++\n");
	try {
		for (i = 0; i < 10; i++)
			func_exception(i);
	} catch (...)
	{
		printf("got exception\n");
	}
	return 0;
}
