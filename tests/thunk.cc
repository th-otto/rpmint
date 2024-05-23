#include <stdio.h>

class Base {
public :
    virtual void f(const char *s) {
        printf("%s: %s\n", __PRETTY_FUNCTION__, s);
    }
private:
    long x;
};

//derived class
class Derived : public virtual Base {
public:
    virtual void f(const char *s) {
        printf("%s: %s\n", __PRETTY_FUNCTION__, s);
    }
private:
    long y;
};

void test(class Base &b)
{
	b.f("Hello");
}

int main(void) {
    Derived d;
    
    test(d);
    return 0;
}
