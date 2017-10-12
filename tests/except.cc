#include <stdio.h>
#include <exception>

void test()
{
	printf("throwing oops\n");
	throw("oops");
}


int main(void)
{
	try {
		test();
	} catch (const char *s)
	{
		printf("got exception %s\n", s);
	}
	return 0;
}
