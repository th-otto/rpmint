#include <stdio.h>
#include <readline/readline.h>


int main(void)
{
	int rows, cols;
	
	printf("calling rl_reset_terminal\n");
	rl_reset_terminal (NULL);
	printf("calling rl_get_screen_size\n");
	rl_get_screen_size (&rows, &cols);
	printf("rows=%d cols=%d\n", rows, cols);

	return 0;
}
