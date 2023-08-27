#include <math.h>
         volatile double d1, d2;
         volatile int i;
int main (void)
{
i = fpclassify(d1);
         i = isfinite(d1);
         i = isinf(d1);
         i = isnan(d1);
         i = isnormal(d1);
         i = signbit(d1);
         i = isgreater(d1, d2);
         i = isgreaterequal(d1, d2);
         i = isless(d1, d2);
         i = islessequal(d1, d2);
         i = islessgreater(d1, d2);
         i = islessgreater(d1, d2);
         i = isunordered(d1, d2);

  ;
  return 0;
}
