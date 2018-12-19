
#include <stdint.h>
#include <stdio.h>

static uint32_t r0 = 1, r1 = 0, r3 = 0;

void calc()
{
	r0 = 0;
	r1 = 1;

	// do {
	// 	r3 = 1;
	// 	do {
	// 		if(r1 * r3 == 10551264)
	// 			r0 = r1 + r0;
	// 		r3 += 1;
	// 	}
	// 	while (r3 <= 10551264);
	// 	r1++;
	// }
	// while (r1 <= 10551264);

	for(r1 = 1; r1 <= 10551264; r1++)
		if (10551264 % r1 == 0)
			r0 += r1;
}

int main()
{
	calc();
	printf("r0 %u\n", r0);
	fflush(stdout);
	return 0;
}

