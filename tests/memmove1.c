/* generates calls to memmove */

struct foo {
	char	*data;
	char	type;
	char	res1;
	char	bdev;
	char	res2;
};

struct foo *p;

void test(int i, int l)
{
	int j;
	
	for (j = l; j > i; j--)
	{
		p[j] = p[j - 1];
	}
}
