/* m68k-atari-mint-g++ -S -O2 -o - structpad.cc | grep '\.long' */

#include <array>

#define ELEMENTS 9

struct s {
using array_t = std::array<char, ELEMENTS>;
array_t a;
} __attribute__((__packed__));

int a = sizeof(struct s);
