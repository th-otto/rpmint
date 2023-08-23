/* m68k-atari-mint-gcc -S -O2 -o - structpad.c | grep '\.long' */

#define ELEMENTS 9

struct s {
        char a[ELEMENTS];
};

int a = sizeof(struct s);
