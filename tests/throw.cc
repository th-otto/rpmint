#include <stdio.h>


void test()
{
	throw 100;
}

int main(void)
{
	try
	{
		test();
	} catch (int e)
	{
		fprintf(stderr, "Got exception %d\n", e);
	}
	return 0;
}
