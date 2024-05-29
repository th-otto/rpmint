extern void __attribute__((sysv_abi)) test1(void);


__attribute__((ms_abi)) void test(void)
{
	test1();
}
