extern void __attribute__((fastcall)) test1(int, int, int);


void test(void)
{
	test1(1, 2, 4);
}
