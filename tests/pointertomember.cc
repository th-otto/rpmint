class Foo {
public:
	void Init(const char *, int, int, int);
};

Foo foo;

typedef void (Foo::*callback)(const char *, int, int, int);
callback f;

void test(void)
{
	f = &Foo::Init;
}

void test2(void)
{
	(foo.*f)("hello", 1, 2, 3);
}
