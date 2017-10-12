#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <osbind.h>
#include <unistd.h>

/*
 * this program is intended to check that functions
 * declared with __attribute__((__fastcall__))
 * work as intended, when compiled in standard mode
 * (without -mfastcall option), hence the test.
 * It must be compiled though with a gcc that supports
 * this option.
 */
#ifdef __FASTCALL__
# error "must not be compiled with -mfastcall"
#endif

#define FASTCALL __attribute__((__fastcall__))

void *FASTCALL memset_fast(void *address, short c, unsigned long size);
void FASTCALL bzero_fast(void *address, unsigned long size);

void *FASTCALL memcpy_fast(void * dst, void * src, size_t length);
void *FASTCALL memmove_fast(void * dst, void * src, size_t length);

int main(void)
{
	int err = 0;
	void *buf1;
	void *buf2;
	long size;
	int pattern = 0x55;
	
#if 1
	for (size = 1; size < 30000000L; size += 800000L + random() % 200000L, pattern++)
	{
		printf("testing memset %ld\n", size);
		buf1 = (void *)Malloc(size);
		buf2 = (void *)Malloc(size);
		if (buf1 == NULL || buf2 == NULL)
		{
			fprintf(stderr, "not enough memory; stopping with err = %d\n", err);
			Mfree(buf2);
			Mfree(buf1);
			break;
		}
		memset(buf1, pattern, size);
		memset_fast(buf2, pattern, size);
		if (memcmp(buf1, buf2, size) != 0)
		{
			err = 1;
			fprintf(stderr, "fail\n");
		}
		Mfree(buf2);
		Mfree(buf1);
	}
#endif
	
	for (size = 20; size < 30000000L; size += 800000L + random() % 200000L, pattern++)
	{
		printf("testing memcpy %ld\n", size);
		buf1 = (void *)Malloc(size);
		buf2 = (void *)Malloc(size);
		if (buf1 == NULL || buf2 == NULL)
		{
			fprintf(stderr, "not enough memory; stopping with err = %d\n", err);
			Mfree(buf2);
			Mfree(buf1);
			break;
		}
		memset(buf1, pattern, size);
		memset_fast(buf2, ~pattern, size);
		memcpy(buf2, buf1, size);
		if (memcmp(buf1, buf2, size) != 0)
		{
			err = 1;
			fprintf(stderr, "fail\n");
		}
		Mfree(buf2);
		Mfree(buf1);
	}
	
	printf("%s\n", err ? "FAIL" : "OK");
	
	return err;
}
