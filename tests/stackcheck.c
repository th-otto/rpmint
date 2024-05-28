int test(int n)
{
	if (n > 0)
		return test(n);
	return n;
}

int main(void)
{
	test(1);
	return 0;
}
