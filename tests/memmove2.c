char last9[10];

/* generates calls to memmove if count > 2 */
void test(void)
{
	char *c0 = last9;
	char *c1 = &last9[1];
	int j;

	for (j = 0; j < 4; j++)
		*c0++ = *c1++;
}
