#include <stdio.h>

#ifdef __FASTCALL__
# error "must not be compiled with -mfastcall"
#endif

#define FASTCALL __attribute__((__fastcall__))

extern long FASTCALL __mulsi3_fast(long a, long b);
extern long FASTCALL __divsi3_fast(long a, long b);
extern unsigned long FASTCALL __udivsi3_fast(unsigned long a, unsigned long b);
extern long FASTCALL __modsi3_fast(long a, long b);
extern unsigned long FASTCALL __umodsi3_fast(unsigned long a, unsigned long b);

int main(void)
{
	int err = 0;
	
	{
		long a, b, c1, c2;
		
		printf("test lmul\n");
		for (a = 0; a < 100000l; a += 100)
		{
			for (b = 0; b < 100000l; b += 100)
			{
				c1 = __mulsi3_fast(a, b);
				c2 = a * b;
				if (c1 != c2)
				{
					err = 1;
					fprintf(stderr, "%ld * %ld: %ld != %ld\n", a, b, c1, c2);
				}
			}
		}
	}
	
	{
		unsigned long a, b, c1, c2;
		
		printf("test ulmul\n");
		for (a = 0; a < 100000l; a += 100)
		{
			for (b = 0; b < 100000l; b += 100)
			{
				c1 = __mulsi3_fast(a, b);
				c2 = a * b;
				if (c1 != c2)
				{
					err = 1;
					fprintf(stderr, "%lu * %lu: %lu != %lu\n", a, b, c1, c2);
				}
			}
		}
	}
	
	{
		long a, b, c1, c2;
		
		printf("test ldiv\n");
		for (a = 0; a < 100000l; a += 100)
		{
			for (b = 1; b < 100000l; b += 100)
			{
				c1 = __divsi3_fast(a, b);
				c2 = a / b;
				if (c1 != c2)
				{
					err = 1;
					fprintf(stderr, "%ld / %ld: %ld != %ld\n", a, b, c1, c2);
				}
			}
		}
	}
	
	{
		unsigned long a, b, c1, c2;
		
		printf("test uldiv\n");
		for (a = 0; a < 100000l; a += 100)
		{
			for (b = 1; b < 100000l; b += 100)
			{
				c1 = __udivsi3_fast(a, b);
				c2 = a / b;
				if (c1 != c2)
				{
					err = 1;
					fprintf(stderr, "%ld / %ld: %ld != %ld\n", a, b, c1, c2);
				}
			}
		}
	}
	
	{
		long a, b, c1, c2;
		
		printf("test lmod\n");
		for (a = 0; a < 100000l; a += 100)
		{
			for (b = 1; b < 100000l; b += 100)
			{
				c1 = __modsi3_fast(a, b);
				c2 = a % b;
				if (c1 != c2)
				{
					err = 1;
					fprintf(stderr, "%ld % %ld: %ld != %ld\n", a, b, c1, c2);
				}
			}
		}
	}
	
	{
		unsigned long a, b, c1, c2;
		
		printf("test ulmod\n");
		for (a = 0; a < 100000l; a += 100)
		{
			for (b = 1; b < 100000l; b += 100)
			{
				c1 = __umodsi3_fast(a, b);
				c2 = a % b;
				if (c1 != c2)
				{
					err = 1;
					fprintf(stderr, "%lu % %lu: %lu != %lu\n", a, b, c1, c2);
				}
			}
		}
	}
	
	printf("%s\n", err ? "FAIL" : "OK");
	
	return err;
}
