#include <stdio.h>

class MyException
{

};

int main(int argc, char *argv[])
{
	puts("Start");

	try 
	{
		throw MyException();
	}
	catch (const MyException& e)
	{
		puts("Exception!!");
	}

	puts("End");

	return 0;
}
