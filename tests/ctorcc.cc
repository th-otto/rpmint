#include <mintbind.h>
#include <stddef.h>

void operator delete(void *, size_t)
{
}

class A {
public:
	A();
	virtual ~A();
};

static A a;

A::A()
{
	Cconws("C++ constructor\r\n");
}

A::~A()
{
	Cconws("C++ destructor\r\n");
}

int main(void)
{
	return 0;
}
