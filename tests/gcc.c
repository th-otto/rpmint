/* generates calls to memset */

void d2a( int i, char e[] )
{
	if (i >= 0)
		while( i >= 0 )
			e[i--] = ' ';
}

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

char last9[10];

/* generates calls to memmove if count > 2 */
void test2(void)
{
	char *c0 = last9;
	char *c1 = &last9[1];
	int j;

	for (j = 0; j < 4; j++)
		*c0++ = *c1++;
}
