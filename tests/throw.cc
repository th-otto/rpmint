#include <stdio.h>

  class exception
  {
  public:
    exception() throw() { }
    virtual ~exception() throw();
    virtual const char* what() const throw();
  };

exception::~exception() throw() { }
const char* exception::what() const throw() { return "hello"; }



void func_exception(int i)
{
	printf("in %s\n", __func__);
	if (i == 5)
		throw exception();
}

int main(void)
{
	int i;
	
	printf("Hello, C++\n");
	try {
		for (i = 0; i < 10; i++)
			func_exception(i);
	} catch (const exception &e)
	{
		printf("got exception %d %s\n", i, e.what());
	}
	return 0;
}
