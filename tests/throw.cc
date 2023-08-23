#include <stdio.h>
#include <exception>


void func_exception(void)
{
	printf("in %s\n", __func__);
	throw std::exception();
}

int main(void)
{
	printf("Hello, C++\n");
	try {
		func_exception();
	} catch (const std::exception &e)
	{
		printf("got exception %s\n", e.what());
	}
	return 0;
}
