extern __attribute__((fastcall)) void test(void);

/* this function needs to preserve d2, because it calls a fastcall function */
__attribute__((cdecl)) void test2(void)
{
	test();
}
