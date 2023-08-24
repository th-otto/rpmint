int somefunc(int (*f)(int));

int f(void) {
int i = 2;
int g(int j) { return i + j; }
return somefunc(g);
}
