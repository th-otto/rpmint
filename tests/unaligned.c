union unal
{
    long val;
} __attribute__ ((packed));

union unal g;

void f(void)
{
    g.val = 0x12345678;
}
