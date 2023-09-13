#include <stdio.h>

void no_such_function(void) __attribute__ ((weak));

int main(void)
{
	printf("f: %p\n", no_such_function);
	return 0;
}
