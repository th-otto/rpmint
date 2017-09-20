
CC := ${PWD}/mint-build/gcc/xgcc -B ${PWD}/mint-build/gcc
CFLAGS = -O2 -fomit-frame-pointer
ASFLAGS = $(CFLAGS)
LDFLAGS = $(CFLAGS)

PROGRAMS = multest memtest

all: $(PROGRAMS)

multest: multest.o mulfast.o

memtest: memtest.o memfast.o memcpyf.o

clean::
	$(RM) *.o $(PROGRAMS) a.out core
