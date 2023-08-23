struct s {
	char a[4];
};

struct s test(void)
{
	struct s a;
	
	a.a[0] = 0;
	return a;
}
