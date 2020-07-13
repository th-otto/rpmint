/* generates calls to memset */

void d2a(int i, char *e)
{
	if (i > 0)
		while (i > 0)
			e[--i] = ' ';
}

struct foo {
	char	data[8];
};

struct foo a, b;

void test1(void)
{
	a = b;
}
