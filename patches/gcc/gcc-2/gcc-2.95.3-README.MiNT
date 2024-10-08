Please read the following important information!

As of version 0.54.99 the MiNTLib requires at least gcc 2.95.2 (the
final version, not a alpha or beta version you eventually got).  This
is MANDATORY!

The main story behind that is that there were certain historical problems
in the combination MiNTLib/gcc that could only be fixed by making a
cut.  The advantage of this is that development under MiNT is now
almost 99 % standard (i. e. the same as you are familiar with on
other Unix platforms).

If you use a binary distribution of the MiNTLib it is also mandatory
to use at least the GNU binutils >= version 2.9.1.  Older linkers
(ld) and archivers (ar/ranlib) will not recognize the libraries
in this distribution.  If you build the library from the sources
you may get along with an older linker, but you will probably run
into problems and it is impossible to keep the namespace of the
MiNTLib clean.  Please update instead.

Even if you have installed the required tools you may run into 
problems.  You should therefore do a little test after installation.
I assume here that you have installed the MiNTLib in "/usr".  If
you have installed in "/usr/local" you have to replace "/usr" with
"/usr/local" in the following.

OK, our test, start a shell and run the command:

	$ gcc --print-file-name=libc.a

It should output "/usr/lib/libc.a".  If not, you either have to 
always give gcc the extra option "-L/path/to/your/lib" whenever
you run it, or copy resp. link your libc.a to the location where
gcc expects it.  In any case, make sure that gcc really links against
the library that you want.

Now test the multilib features of your gcc:

	$ gcc -m68020-60 -m68881 --print-file-name=libc.a
	/usr/lib/m68020-60/libc.a
	$ gcc -mshort --print-file-name=libc.a
	/usr/lib/mshort/libc.a
	$ gcc -m68020-60 -m68881 -mshort --print-file-name=libc.a
	/usr/lib/m68020-60/mshort/libc.a
	$ gcc --print-file-name crt0.o
	/usr/lib/crt0.o

These should be exactly the files that have been installed with the
MiNTLib.  If not, remember to give gcc the correct "-L" options or
copy resp. link.

Finally do a complete test.  Create a source file "hello.c":

	#include <stdio.h>
	
	int
	main (int argc, char* argv[])
	{
		printf ("Hello world!\n");
		return 0;
	}
	
Compile it with the "-H" switch:

	$ gcc -H -c hello.c
	/usr/include/stdio.h
	 /usr/include/compiler.h
	  /usr/include/features.h
	   /usr/include/linker.h
	    /usr/include/libc-symbols.h
	     ...

The "-H" switch instructs gcc to print the name of every header file used
when compiling a program.  All these header files should be the ones
you installed with the MiNTLib.  If not, copy or link, or give gcc
the option "-I /path/to/your/include" so that it searches first in
the correct directory for header files.

	Note: Don't get confused if in the above list you find
	header files from directories like
	
		/usr/lib/gcc-lib/m68k-atari-mint/2.95.2/include
		
	These are compiler headers (stddef.h, float.h, stdarg.h,
	varargs.h, limits.h) and they are not part of the MiNTLib.

If you have installed your MiNTLib in /usr/local you cannot use
the trick with "--print-prog-name" because gcc ignores the -L switch
for "--print-prog-name".  Instead create link the little test program
"hello.o" with the option "-v":

	$ gcc -v -o hello hello.o

This will output a lot of information, including all search-paths for
include files and the exact command lines that are passed to the 
preprocessor, the assembler and the linker.  Make sure that the preprocessor
(cpp) gets the correct -I options so that it searches first in your
MiNTLib directory, and that the linker (ld or collect2, they are the
same) gets the correct -L options to search your MiNTLib first for
directories.  Don't forget to check that the crt0.o that gcc passes
to ld resp. collect2 is the one from your current MiNTLib.

This boils down to: If the compiler uses the wrong header files, invoke
gcc with the option "-I <correct directory", if it uses the wrong
libaries or wrong startup modules (crt0.o) give gcc the option
"-L <correct directory>".

For the common case that you have installed the MiNTLib in "/usr/local"
but your gcc version resides in "/usr/bin", instead of always giving
-L and -O options you should rather set the following environment 
variables in your shell's startup files:

	C_INCLUDE_PATH=/usr/local/include
	LIBRARY_PATH=/usr/local/lib
	export C_INCLUDE_PATH LIBRARY_PATH

Troubleshooting
===============

If the above information is not enough you may also find a solution
for your current problem here.

Problem:  When compiling programs I get a message "program ld got fatal 
          signal 10".
Solution: This is a bug in the GNU linker 2.9.1 when it is fed with a 
	  library in the old format.  Read the above information again
	  and check thoroughly that the linker always sees the correct
	  libraries.  If you are not sure whether a particular library
	  is in the old or in the new format, type
	  "mintbin /usr/lib/libfoobar.a" to get the information.  If
	  it says something about "old format" you cannot use
	  the library.  Either get an update for it or convert it to
	  the new format with "arconv <oldlib> -o <newlib>".

Problem:  The compiler complains about zillions of syntax errors and
	  missing prototypes.
Solution: Your include path is wrong and you include old (or wrong)
	  header files.  Recompile the problematic file with the
	  gcc option "-H".  This will output a list of the headers
	  that are actually read.  Check if they are the ones that
	  you want.

Problem:  The compiler can't find the header files <stddef.h>, 
	  <float.h>, <stdarg.h>, <varargs.h>.  Yep, they are 
	  really missing.
Solution: They are missing on purpose because they belong to gcc,
	  not to the MiNTLib.  They usually reside in
	  
	  	/usr/lib/gcc-lib/m68k-atari-mint/<gcc-version>/include
	  
	  If not, you have to update your compiler.

Problem:  The compiler complains that INT_MAX, CHAR_MAX, LONG_MAX or 
	  the like are not defined although I have included <limits.h>
Solution: See the previous solution.  The header <limits.h> is shared
	  between the libc and the compiler, i. e. some macros are
	  provided by the compiler, some by the libc.  If you have
	  installed everything correctly, both the libc <limits.h>
	  and the gcc <limits.h> will get included whenever you
	  "#include <limits.h>".  If not, verify your installation.

Problem:  I have seen a prototype in a header file but gcc still
	  complains about that prototype missing.
Solution: Read the file NOTES in this directory.  The MiNTLib is
	  a multi-feature library and you have to activate these
	  features explicitely.  Otherwise certain extension definitions
	  will not be visible.

Problem:  A prototype definition in a header file is protected
	  by something like "#ifdef __USE_GNU" (or __USE_POSIX,
	  __USE_BSD, __USE_XOPEN_EXTENDED, ...).  I #define this
	  macro but the prototype is still not visible.
Solution: See above, read the file NOTES.  It is wrong to
	  "#define __USE_GNU" or "#define __USE_BSD".  Instead
	  "#define _GNU_SOURCE" or "#define _BSD_SOURCE" like
	  described in NOTES.

Hope this helps.

Guido Flohr <guido@freemint.de>
