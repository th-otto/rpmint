TARGET=m68k-atari-mintelf

CROSS_PREFIX=$(TARGET)-

#CC := ${PWD}/../gcc-build/gcc/xgcc -B ${PWD}/../gcc-build/gcc
CC := $(CROSS_PREFIX)gcc
CXX := $(CROSS_PREFIX)g++ -fno-rtti

CFLAGS = -O2 -fomit-frame-pointer
ASFLAGS = $(CFLAGS)
LDFLAGS = $(CFLAGS)

PROGRAMS = multest memtest ctorc ctorcc throw thread curses

all: $(PROGRAMS) compile-tests

multest: multest.o mulfast.o

memtest: memtest.o memfast.o memcpyf.o

ctorc: ctorc.o
	$(CC) -o $@ $^

curses: curses.c
	$(CC) -o $@ $^ -lncurses
	$(CC) -o $@ $^ -lncursesw

ctorcc: ctorcc.o
	$(CXX) -o $@ $^

throw: throw.cc
	$(CXX) -o $@ $^

compile-tests::
	$(CC) -S -O2 -o - structpad.c | grep '\.long' | grep -q 10
	$(CXX) -S -O2 -o - structpad.cc | grep '\.long' | grep -q 10
	if $(CC) -S -O2 -o - structret.c | grep -q 'a1'; then false; fi
.PHONY: compile-tests

clean::
	$(RM) *.o $(PROGRAMS) a.out core
