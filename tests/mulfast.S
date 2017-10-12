#include "symbols.h"

	.text
	FUNC(__mulsi3_fast)
	.globl	SYM (__mulsi3_fast)
SYM (__mulsi3_fast):
	move.l  d2,-(a7)
	movel   d0, a0          | d0a0 = x0:x1
	movel   d1, a1		| d1a1 = y0:y1
	swap	d0              | d0   = x1:x0 
	muluw   d1, d0          | d0 = y1*x0 
	swap	d1		| d1 = y1:y0
	movel   a0, d2		| d2 = x0:x1
	muluw   d2, d1          | d1 = x1*y0	
#ifndef __mcoldfire__
	addw	d1, d0
#else
	addl	d1, d0
#endif
	swap	d0
	clrw	d0
	movel	a1,d1		| d1 = y0:y1
	muluw	d2, d1		| d1 = x1*y1

	move.l  (a7)+,d2
	addl	d1, d0

	rts


	.text
	FUNC(__udivsi3_fast)
	.globl	SYM (__udivsi3_fast)
SYM (__udivsi3_fast):
#ifndef __mcoldfire__
	move.l  d2,-(a7)
	movel	d0, a0

	cmpl	IMM (0x10000), d1 /* divisor >= 2 ^ 16 ?   */
	jcc	udivsi3_fast_L3		/* then try next algorithm */
	movel	d0, d2
	clrw	d2
	swap	d2
	divu	d1, d2          /* high quotient in lower word */
	movew	d2, d0		/* save high quotient */
	swap	d0
	movew	a0, d2		/* get low dividend + high rest */
	divu	d1, d2		/* low quotient */
	movew	d2, d0
	jra	udivsi3_fast_L6

udivsi3_fast_L3:	movel	d1, d2		/* use d2 as divisor backup */
udivsi3_fast_L4:	lsrl	IMM (1), d1	/* shift divisor */
	lsrl	IMM (1), d0	/* shift dividend */
	cmpl	IMM (0x10000), d1 /* still divisor >= 2 ^ 16 ?  */
	jcc	udivsi3_fast_L4
	divu	d1, d0		/* now we have 16-bit divisor */
	andl	IMM (0xffff), d0 /* mask out divisor, ignore remainder */

/* Multiply the 16-bit tentative quotient with the 32-bit divisor.  Because of
   the operand ranges, this might give a 33-bit product.  If this product is
   greater than the dividend, the tentative quotient was too large. */
	movel	d2, d1
	mulu	d0, d1		/* low part, 32 bits */
	swap	d2
	mulu	d0, d2		/* high part, at most 17 bits */
	swap	d2		/* align high part with low part */
	tstw	d2		/* high part 17 bits? */
	jne	udivsi3_fast_L5		/* if 17 bits, quotient was too large */
	addl	d2, d1		/* add parts */
	jcs	udivsi3_fast_L5		/* if sum is 33 bits, quotient was too large */
	cmpl	a0, d1		/* compare the sum with the dividend */
	jls	udivsi3_fast_L6		/* if sum > dividend, quotient was too large */
udivsi3_fast_L5:	subql	IMM (1), d0	/* adjust quotient */

udivsi3_fast_L6:
	move.l  (a7)+,d2
	rts

#else /* __mcoldfire__ */

/* ColdFire implementation of non-restoring division algorithm from
   Hennessy & Patterson, Appendix A. */
	moveml	d2-d4,sp@
	clrl	d2		| clear p
	moveq	IMM (31),d4
udivsi3_fast_L1:	addl	d0,d0		| shift reg pair (p,a) one bit left
	addxl	d2,d2
	movl	d2,d3		| subtract b from p, store in tmp.
	subl	d1,d3
	jcs	udivsi3_fast_L2		| if no carry,
	bset	IMM (0),d0	| set the low order bit of a to 1,
	movl	d3,d2		| and store tmp in p.
udivsi3_fast_L2:	subql	IMM (1),d4
	jcc	udivsi3_fast_L1
	moveml	sp@,d2-d4	| restore data registers
	rts
#endif /* __mcoldfire__ */



	.text
	FUNC(__divsi3_fast)
	.globl	SYM (__divsi3_fast)
SYM (__divsi3_fast):
	move.l  d2,-(a7)
	moveq	IMM (1), d2	/* sign of result stored in d2 (=1 or =-1) */
	tstl	d1
	jpl	divsi3_fast_L1
	negl	d1
#ifndef __mcoldfire__
	negw	d2		/* change sign because divisor <0  */
#else
	negl	d2		/* change sign because divisor <0  */
#endif
divsi3_fast_L1:	tstl	d0		/* d0 = dividend */
	jpl	divsi3_fast_L2
	negl	d0
#ifndef __mcoldfire__
	negw	d2
#else
	negl	d2
#endif

divsi3_fast_L2:	movew	d2,a1		/* Called function MUST NOT clobber a1 */
	jbsr	SYM (__udivsi3_fast)	/* divide abs(dividend) by abs(divisor) */

	movew	a1,d2
	jpl	divsi3_fast_L3
	negl	d0

divsi3_fast_L3:
	move.l  (a7)+,d2
	rts




	.text
	FUNC(__umodsi3_fast)
	.globl	SYM (__umodsi3_fast)
SYM (__umodsi3_fast):
	move.l  d2,-(a7)
	movel	d0, d2
	movel	d1, a1		/* a1 MUST NOT be clobbered by calls*/
	jbsr	SYM (__udivsi3_fast)
	movel	a1, d1		/* d1 = divisor */
#ifndef __mcoldfire__
	jbsr SYM (__mulsi3_fast)	/* d0 = (a/b)*b */
#else
	mulsl	d1,d0
#endif
	movel	d2, d1		/* d1 = dividend */
	subl	d0, d1		/* d1 = a - (a/b)*b */
	movel	d1, d0
	move.l  (a7)+,d2
	rts

	FUNC(__modsi3_fast)
	.globl	SYM (__modsi3_fast)
SYM (__modsi3_fast):
	move.l  d2,-(a7)
	movel	d0, sp@-
	movel	d1, sp@-
	jbsr	SYM (__divsi3_fast)
	movel	sp@+, d1	/* d1 = divisor */
#ifndef __mcoldfire__
	jbsr	SYM (__mulsi3_fast)	/* d0 = (a/b)*b */
#else
	mulsl	d1,d0
#endif
	movel	sp@+, d1	/* d1 = dividend */
	subl	d0, d1		/* d1 = a - (a/b)*b */
	movel	d1, d0
	move.l  (a7)+,d2
	rts
