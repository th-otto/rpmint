TARGET=m68k-atari-mintelf

CROSS_PREFIX=$(TARGET)-

#CC := ${PWD}/../gcc-build/gcc/xgcc -B ${PWD}/../gcc-build/gcc
CC := $(CROSS_PREFIX)gcc
CXX := $(CROSS_PREFIX)g++ -fno-rtti

CFLAGS = -O2 -fomit-frame-pointer
ASFLAGS = $(CFLAGS)
LDFLAGS = $(CFLAGS)

PROGRAMS = multest memtest ctorc ctorcc

all: $(PROGRAMS)

multest: multest.o mulfast.o

memtest: memtest.o memfast.o memcpyf.o

ctorc: ctorc.o
	$(CC) -o $@ $^

ctorcc: ctorcc.o
	$(CXX) -o $@ $^

clean::
	$(RM) *.o $(PROGRAMS) a.out core
