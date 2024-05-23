int test1(int, int, int);

int x;

int test2(int a, int b, int c)
{
	x = a * a;
	return test1(a, b, c);
}
