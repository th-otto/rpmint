long long mul_hwi_a, mul_hwi_b;
long long mul_hwi_result;
int mul_hwi_ovf;
void mul_hwi(int *overflow) {
  *overflow = __builtin_mul_overflow(mul_hwi_a, mul_hwi_b, &mul_hwi_result);
  mul_hwi(&mul_hwi_ovf);
}
