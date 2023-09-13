template<typename T>
struct A
{
  A()
  { }

  char buf[4];
};

template<typename T>
struct B : public A<T>
{
  B()
  { }
};

template<typename T>
struct C : public B<T>
{
  C() throw()
  { }
};

void f()
{
  C<char> tmp;
}

