#include <stdio.h>
#include <mintbind.h>

void __attribute__((__constructor__)) cons(void)
{
	Cconws("C constructor\r\n");
}


void __attribute__((__destructor__)) dest(void)
{
	Cconws("C destructor\r\n");
}


int main(void)
{
	return 0;
}
