/*
 * checks that jbsr is optimized to a short branch, even if
 * the target label is externally visible.
 * See EXTERN_FORCE_RELOC in te-mint*.h
 */
	.globl hello
	
	.text
	
_start:
	jbsr hello
	nop
	rts

hello:
	nop
	rts
