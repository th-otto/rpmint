long add_hwi_a;
void add_hwi(long long b, int *overflow) {
  long long result;
  *overflow = __builtin_add_overflow(add_hwi_a, b, &result);
}
long long mul_hwi_b;
long long mul_hwi(long long a, int *overflow) {
  long long result;
  *overflow = __builtin_mul_overflow(a, mul_hwi_b, &result);
  return result;
}
int sdiv_floor(void(), long &);
long long **lambda_matrix_row_add_mat;
int lambda_matrix_row_add_r1;
int lambda_matrix_row_add_ovf;
static int lambda_matrix_row_add(int n) {
  int i;
  for (; i < n; i++) {
    long long tem =
        mul_hwi(lambda_matrix_row_add_mat[lambda_matrix_row_add_r1][i],
                &lambda_matrix_row_add_ovf);
    if (lambda_matrix_row_add_ovf)
      return 0;
    add_hwi(tem, &lambda_matrix_row_add_ovf);
    if (lambda_matrix_row_add_ovf)
      return 0;
  }
  return 1;
}
static int lambda_matrix_right_hermite(int m) {
  for (;;)
    if (!lambda_matrix_row_add(m))
      return 0;
}
void analyze_subscript_affine_affine_j0() {
  unsigned nb_vars_a, nb_vars_b, dim = nb_vars_a + nb_vars_b;
  lambda_matrix_right_hermite(dim);
  long j1(sdiv_floor(analyze_subscript_affine_affine_j0, j1));
}
