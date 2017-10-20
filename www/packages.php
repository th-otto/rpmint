<?php

$basepackages = array(
	'binutils' => array(
		'name' => 'binutils',
		'upstream' => 'http://www.gnu.org/software/binutils/',
		'version' => '2.29.1',
		'date' => '20171011',
		'repo' => 'https://github.com/th-otto/binutils',
		'branch' => 'binutils-2_29-mint',
		'source' => 'https://ftp.gnu.org/gnu/binutils/binutils-2.29.1.tar.xz',
		'patch' => 1,
		'script' => 1,
		'doc' => 1,
		'elf' => 1,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 0,
		'comment' => '
The binutils are a collection of low-level language tools.<br />
The full documentation can be found
<a href="https://sourceware.org/binutils/docs-2.29/" ' . $target . '>here</a>.<br />
		'
	),
	'gcc464' => array(
		'name' => 'gcc',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '4.6.4',
		'date' => '20170518',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'gcc-4_6-mint',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-4.6.4/gcc-4.6.4.tar.bz2',
		'patch' => 1,
		'patchcomment' => 'This archive also contains an (experimental) patch for -mfastcall support.',
		'script' => 1,
		'doc' => 1,
		'elf' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'comment' => '
<code>m68k-atari-mint-gcc</code> is the C compiler.<br />
<code>m68k-atari-mint-g++</code> is the C++ compiler.<br />
They just work. I only tested the C and C++ languages, but other languages may work, too.<br />
If you want to generate DRI symbols in the final executable, append the option
<code>-Wl,--traditional-format</code> to inform the linker.<br />
I configured this version to generate 68000 code by default, and I enabled multilib.
By default, <code>sizeof(int) == 4</code>, but if you compile with <code>-mshort</code>
then <code>sizeof(int) == 2</code> (unsupported by the current MiNTLib). Every object file and every library must be compiled
with the same option! You can also generate code for the 68020 and higher and for the FPU
by using the <code>-m68020-60</code> option. And you can generate code for ColdFire V4e processors
by using the <code>-mcpu=5475</code> option.<br />
The full documentation can be found
<a href="http://gcc.gnu.org/onlinedocs/gcc-4.6.4/gcc/" ' . $target . '>here</a>.<br />
GCC contains everything to compile C programs, except a standard library and a math library.
'
	),
	'gcc720' => array(
		'name' => 'gcc',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '7.2.0',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'gcc-7-mint',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-7.2.0/gcc-7.2.0.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain.',
		'script' => 1,
		'doc' => 1,
		'elf' => 1,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 0,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'comment' => '
This is the currently most recent official version GCC. It comes in two
flavours: one for a.out toolchain (as the previously used version
4.6.4), and one for an elf toolchain. Elf toolchain here means that it
will still produce the same executable format, but works with elf object
files. To support this better, all libraries offered here were also recompiled
using this format (although it is theoretically should be possible to mix them).
'
	),
	'mintbin' => array(
		'name' => 'mintbin',
		'title' => 'MiNTBin',
		'upstream' => 'https://github.com/freemint/mintbin',
		'version' => '0.3',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/mintbin',
		'source' => $download_dir . 'mintbin-0.3.tar.xz',
		'patch' => 0,
		'script' => 1,
		'doc' => 0,
		'elf' => 1,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'comment' => '
MiNTBin has been written by Guido Flohr. It is a set of tools for manipulating
the MiNT executables generated by <code>ld</code>. They are a complement to
the binutils. The main tools are <code>stack</code> for setting the stack size
of an executable, and <code>flags</code> for setting the header flags.
'
	),
);

$libpackages = array(
	'mintlib' => array(
		'name' => 'mintlib',
		'title' => 'MiNTLib',
		'upstream' => 'https://github.com/freemint/mintlib',
		'version' => '0.60.1',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/mintlib',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'comment' => '
MiNTLib is a standard C library. It allows to build software which runs on MiNT and TOS
operating systems. Unlike other packages, I used the latest sources from the CVS repository
instead of the latest official release.
'
	),
	'pml' => array(
		'name' => 'pml',
		'title' => 'PML',
		'upstream' => 'http://ftp.funet.fi/pub/atari/programming/',
		'version' => '2.03',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/pml',
		'branch' => 'master',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
PML stands for Portable Math Library.<br />
It works, but of course it is really slow on a 68000 without FPU.'
	),
	'gemlib' => array(
		'name' => 'gemlib',
		'title' => 'GEMlib',
		'upstream' => 'https://github.com/freemint/lib',
		'version' => '0.44.0',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/lib',
		'branch' => 'master/gemlib',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'comment' => '
The GEMlib allows to write graphical programs using GEM.<br />
It is maintained by Arnaud Bercegeay, the official releases are available
on the <a href="http://arnaud.bercegeay.free.fr/gemlib/"' . $target . '>GEMlib&apos;s homepage</a>.
However, the latest sources are available
on the <a href="https://github.com/freemint/lib"' . $target . '>FreeMiNT&apos;s GitHub repository</a>.
'
	),
	'cflib' => array(
		'name' => 'cflib',
		'title' => 'CFLIB',
		'upstream' => 'https://github.com/freemint/lib',
		'version' => '21',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/lib',
		'branch' => 'master/cflib',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'comment' => '
CFLIB is Christian Felsch&apos;s GEM utility library. It provide advanced controls,
such as check boxes, radio buttons, combo boxes... It also allows windowed
dialogs.<br />
BUG: On plain TOS, the CFLIB makes intensive usage of the GEM USERDEF feature.
Due to bad GEM design, USERDEF callbacks are called in supervisor mode using
the very small internal AES stack. Unfortunately, some GemLib functions such
as v_gtext() needs an insane amout of stack (more than 2 KB). So some USERDEF
callbacks quickly produces an AES internal stack overflow, and crashes all the
system.<br />
Concretely, due to this issue, programs using the CFLIB work fine on XaAES
and TOS 4.04, but crashes on TOS 1.62 and EmuTOS.
'
	),
	'gemma' => array(
		'name' => 'gemma',
		'upstream' => 'https://github.com/freemint/lib',
		'version' => 'git',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/lib',
		'branch' => 'master/gemma',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'comment' => '
Gemma is a support library for GEM application programs.
'
	),
	'zlib' => array(
		'name' => 'zlib',
		'upstream' => 'http://www.zlib.net/',
		'source' => 'http://www.zlib.net/zlib-1.2.11.tar.xz',
		'version' => '1.2.11',
		'date' => '20171006',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
zlib is a compression library implementing the Deflate algorithm, used by gzip and PKZIP.
'
	),
	'libpng' => array(
		'name' => 'libpng',
		'upstream' => 'http://www.libpng.org/pub/png/libpng.html',
		'source' => 'https://ftp-osl.osuosl.org/pub/libpng/src/libpng16/libpng-1.6.34.tar.xz',
		'version' => '1.6.34',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
Portable Network Graphics
<br />
An Open, Extensible Image Format with Lossless Compression 
'
	),
	'bzip2' => array(
		'name' => 'bzip2',
		'upstream' => 'http://www.bzip.org/',
		'source' => 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz',
		'version' => '1.0.6',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
bzip2 is a freely available, patent free (see below), high-quality data
compressor. It typically compresses files to within 10% to 15% of the
best available techniques (the PPM family of statistical compressors),
whilst being around twice as fast at compression and six times faster
at decompression.
'
	),
	'ldg' => array(
		'name' => 'ldg',
		'title' => 'LDG',
		'upstream' => 'http://ldg.sourceforge.net/',
		'version' => 'svn-20171014',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
LDG stands for Gem Dynamical Libraries (actually Librairies Dynamiques
GEM in french). It&apos;s a system allowing GEM applications to load and to
share externals modules. 
<br />
Only the libraries are compiled. To use modules, you also have to
install the auto folder programs from <a href="http://ldg.sourceforge.net/#download">http://ldg.sourceforge.net/</a>. 
'
	),
	'windom' => array(
		'name' => 'windom',
		'title' => 'WinDom',
		'upstream' => 'http://windom.sourceforge.net/',
		'version' => '2.0.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
Windom is a C library to make GEM programming very easy. With the help
of windom, you can focus on programming the real job of your
application, and let windom handle complex and "automatic" GEM stuff
(toolbar, forms, menu in windows...). 
'
	),
	'sdl' => array(
		'name' => 'SDL',
		'upstream' => 'https://www.libsdl.org/',
		'version' => '1.2.15-hg',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
SDL is the Simple DirectMedia Layer library. It is a low-level and cross-platform
library for building games or similar programs.<br />
Thanks to Patrice Mandin, SDL is available on Atari platforms. SDL programs can
run either in full screen or in a GEM window, depending on the SDL_VIDEODRIVER
environment variable.
'
	),
	'ncurses6' => array(
		'name' => 'ncurses',
		'upstream' => 'http://invisible-island.net/ncurses/ncurses.html',
		'source' => 'ftp://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.0.tar.gz',
		'version' => '6.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
Ncurses is a library which allows building full-screen text mode programs,
such as <code>vim</code>, <code>less</code>, or the GDB text UI.
'
	),
	'readline' => array(
		'name' => 'readline',
		'upstream' => 'https://cnswww.cns.cwru.edu/php/chet/readline/rltop.html',
		'source' => 'ftp://ftp.gnu.org/gnu/readline/readline-7.0.tar.gz',
		'version' => '7.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
The GNU Readline library provides a set of functions for use by
applications that allow users to edit command lines as they are typed
in. Both Emacs and vi editing modes are available. The Readline library
includes additional functions to maintain a list of previously-entered
command lines, to recall and perhaps reedit those lines, and perform
csh-like history expansion on previous commands.
'
	),
	'openssl' => array(
		'name' => 'openssl',
		'title' => 'OpenSSL',
		'upstream' => 'https://www.openssl.org/',
		'source' => 'https://www.openssl.org/source/openssl-1.0.2l.tar.gz',
		'version' => '1.0.2l',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
OpenSSL is a robust, commercial-grade, and full-featured toolkit for
the Transport Layer Security (TLS) and Secure Sockets Layer (SSL)
protocols. It is also a general-purpose cryptography library. 
'
	),
	'arc' => array(
		'name' => 'arc',
		'upstream' => 'http://arc.sourceforge.net/',
		'source' => $download_dir . 'arc-5.21p.tar.gz',
		'version' => '5.21p',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
ARC is used to create and maintain file archives. An archive is a group
of files collected together into one file in such a way that the
individual files may be recovered intact.
'
	),
	'arj' => array(
		'name' => 'arj',
		'upstream' => 'http://arj.sourceforge.net/',
		'source' => $download_dir . 'arj-3.10.22.tar.gz',
		'version' => '3.10.22',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
A portable version of the ARJ archiver, available for a growing number
of DOS-like and UNIX-like platforms on a variety of architectures.
'
	),
	'lha' => array(
		'name' => 'lha',
		'upstream' => 'http://lha.sourceforge.jp/',
		'source' => $download_dir . 'lha-1.14i-ac20050924p1.tar.gz',
		'version' => '1.14i-ac20050924p1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
LHa for UNIX - Note: This software is licensed under the ORIGINAL
LICENSE. It is written in man/lha.n in Japanese 
'
	),
/*
	'unrar' => array(
		'name' => 'unrar',
		'title' => 'UnRAR',
		'upstream' => 'http://www.rarlab.com/',
		'source' => 'https://www.rarlab.com/rar/unrarsrc-5.5.8.tar.gz',
		'version' => '5.5.8',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
Unarchiver for .rar files (non-free version)
Unrar can extract files from .rar archives. If you want to create .rar
archives, install package rar.
'
	),
*/
	'xz' => array(
		'name' => 'xz',
		'upstream' => 'http://tukaani.org/xz/',
		'version' => '5.2.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
XZ Utils is free general-purpose data compression software with a high
compression ratio. XZ Utils were written for POSIX-like systems, but
also work on some not-so-POSIX systems. XZ Utils are the successor to
LZMA Utils. 
'
	),
	'zip' => array(
		'name' => 'zip',
		'upstream' => 'http://www.info-zip.org/Zip.html',
		'source' => 'ftp://ftp.info-zip.org/pub/infozip/src/zip30.tgz',
		'version' => '3.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
Zip is a compression and file packaging utility. It is compatible with
PKZIP(tm) 2.04g (Phil Katz ZIP) for MS-DOS systems.
'
	),
	'unzip' => array(
		'name' => 'unzip',
		'upstream' => 'http://www.info-zip.org/UnZip.html',
		'source' => 'ftp://ftp.info-zip.org/pub/infozip/src/unzip60.tgz',
		'version' => '6.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
UnZip is an extraction utility for archives compressed in .zip format
(known as &quot;zip files&quot;).  Although highly compatible both with PKWARE&apos;s
PKZIP(tm) and PKUNZIP utilities for MS-DOS and with Info-ZIP&apos;s own Zip
program, our primary objectives have been portability and non-MS-DOS
functionality. This version can also extract encrypted archives.
'
	),
	'zoo' => array(
		'name' => 'zoo',
		'upstream' => 'http://ftp.math.utah.edu/pub/zoo/',
		'source' => 'http://ftp.math.utah.edu/pub/zoo/zoo-2-10-1.tar.bz2',
		'version' => '2-10-1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
Zoo is a packer based on the Lempel-Ziv algorithm. Lots of files on
DOS/AmigaDOS and TOS systems used this packer for their archives. The
compression rate of gzip is not reached, and thus zoo should only be used
for decompressing old archives.
'
	),
	'gmp' => array(
		'name' => 'gmp',
		'upstream' => 'https://gmplib.org/',
		'source' => 'https://gmplib.org/download/gmp/gmp-6.1.2.tar.xz',
		'version' => '6.1.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
A library for calculating huge numbers (integer and floating point).
'
	),
	'mpfr' => array(
		'name' => 'mpfr',
		'upstream' => 'http://www.mpfr.org/',
		'source' => 'http://www.mpfr.org/mpfr-current/mpfr-3.1.6.tar.xz',
		'version' => '3.1.6',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
The MPFR library is a C library for multiple-precision floating-point
computations with exact rounding (also called correct rounding). It is
based on the GMP multiple-precision library.
'
	),
	'mpc' => array(
		'name' => 'mpc',
		'upstream' => 'http://www.multiprecision.org/mpc/',
		'source' => 'ftp://ftp.gnu.org/gnu/mpc/mpc-1.0.3.tar.gz',
		'version' => '1.0.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as MPFR.
'
	),
	'tar' => array(
		'name' => 'tar',
		'upstream' => 'http://www.gnu.org/software/tar/',
		'source' => 'https://ftp.gnu.org/gnu/tar/tar-1.29.tar.xz',
		'version' => '1.29',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
GNU Tar is an archiver program. It is used to create and manipulate files
that are actually collections of many other files; the program provides
users with an organized and systematic method of controlling a large amount
of data. Despite its name, that is an acronym of "tape archiver", GNU Tar
is able to direct its output to any available devices, files or other programs,
it may as well access remote devices or files.
'
	),
	'libiconv' => array(
		'name' => 'libiconv',
		'upstream' => 'http://www.gnu.org/software/libiconv',
		'source' => 'http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.15.tar.gz',
		'version' => '1.15',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
libiconv library provides an iconv() implementation, for use on
systems which don&apos;t have one, or whose implementation cannot convert
from/to Unicode.
'
	),
	'm4' => array(
		'name' => 'm4',
		'title' => 'M4',
		'upstream' => 'https://www.gnu.org/software/m4/m4.html',
		'source' => 'ftp://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.xz',
		'version' => '1.4.18',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
GNU m4 is an implementation of the traditional Unix macro processor.
'
	),
	'flex' => array(
		'name' => 'flex',
		'upstream' => 'https://github.com/westes/flex',
		'source' => 'https://github.com/westes/flex/releases/download/v2.6.4/flex-2.6.4.tar.gz',
		'version' => '2.6.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
FLEX is a tool for generating scanners: programs that recognize lexical
patterns in text.
'
	),
	'bison' => array(
		'name' => 'bison',
		'upstream' => 'http://www.gnu.org/software/bison/bison.html',
		'source' => 'http://ftp.gnu.org/gnu/bison/bison-3.0.4.tar.xz',
		'version' => '3.0.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
Bison is a general-purpose parser generator that converts an annotated
context-free grammar into a deterministic LR or generalized LR (GLR)
parser employing LALR(1) parser tables. As an experimental feature,
Bison can also generate IELR(1) or canonical LR(1) parser tables. Once
you are proficient with Bison, you can use it to develop a wide range
of language parsers, from those used in simple desk calculators to
complex programming languages. 
'
	),
	'expat' => array(
		'name' => 'expat',
		'upstream' => 'https://libexpat.github.io/',
		'source' => 'http://downloads.sourceforge.net/project/expat/expat/2.2.4/expat-2.2.4.tar.bz2',
		'version' => '2.2.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
Expat is an XML parser library written in C. It is a stream-oriented
parser in which an application registers handlers for things the
parser might find in the XML document (like start tags).
'
	),
	'libidn2' => array(
		'name' => 'libidn2',
		'upstream' => 'https://www.gnu.org/software/libidn/#libidn2',
		'source' => 'ftp://ftp.gnu.org/gnu/libidn/libidn2-2.0.4.tar.lz',
		'version' => '2.0.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
Libidn2 is an implementation of the IDNA2008 + TR46 specifications (RFC
5890, RFC 5891, RFC 5892, RFC 5893, TR 46). Libidn2 is a standalone
library, without any dependency on Libidn. Libidn2 is believed to be a
complete IDNA2008 / TR46 implementation, but has yet to be as
extensively used as the original Libidn library.
'
	),
/*
	'krb5' => array(
		'name' => 'krb5',
		'upstream' => 'https://web.mit.edu/kerberos/www/',
		'source' => 'http://web.mit.edu/kerberos/dist/krb5/1.15/krb5-1.15.2.tar.gz',
		'version' => '1.15.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
Kerberos V5 is a trusted-third-party network authentication system,
which can improve network security by eliminating the insecure
practice of clear text passwords.
'
	),
*/
	'libssh2' => array(
		'name' => 'libssh2',
		'upstream' => 'http://www.libssh2.org/',
		'source' => 'https://www.libssh2.org/download/libssh2-1.8.0.tar.gz',
		'version' => '1.8.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS, SECSH-USERAUTH, SECSH-CONNECTION,
SECSH-ARCH, SECSH-FILEXFER, SECSH-DHGEX, SECSH-NUMBERS, and
SECSH-PUBLICKEY.
'
	),
	'nghttp2' => array(
		'name' => 'nghttp2',
		'upstream' => 'https://nghttp2.org/',
		'source' => 'https://github.com/nghttp2/nghttp2/releases/download/v1.26.0/nghttp2-1.26.0.tar.xz',
		'version' => '1.26.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
nghttp2 is an implementation of HTTP/2 and its header compression algorithm HPACK in C.
'
	),
	'libxml2' => array(
		'name' => 'libxml2',
		'upstream' => 'http://xmlsoft.org',
		'source' => 'ftp://xmlsoft.org/libxml2/libxml2-2.9.6.tar.gz',
		'version' => '2.9.6',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
The XML C library was initially developed for the GNOME project. It is
now used by many programs to load and save extensible data structures
or manipulate any kind of XML files.
'
	),
	'libmetalink' => array(
		'name' => 'libmetalink',
		'upstream' => 'https://launchpad.net/libmetalink',
		'source' => 'https://github.com/metalink-dev/libmetalink/releases/download/release-0.1.3/libmetalink-0.1.3.tar.xz',
		'version' => '0.1.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
Libmetalink is a Metalink library written in C language. It is intended to
provide the programs written in C to add Metalink functionality such as parsing
Metalink XML files.
'
	),
	'libunistring' => array(
		'name' => 'libunistring',
		'upstream' => 'http://www.gnu.org/software/libunistring/',
		'source' => 'http://ftp.gnu.org/gnu/libunistring/libunistring-0.9.7.tar.xz',
		'version' => '0.9.7',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).
'
	),
	'libpsl' => array(
		'name' => 'libpsl',
		'upstream' => 'https://rockdaboot.github.io/libpsl',
		'source' => 'https://github.com/rockdaboot/libpsl/releases/download/libpsl-0.18.0/libpsl-0.18.0.tar.gz',
		'version' => '0.18.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
libpsl is a C library to handle the Public Suffix List. A "public suffix" is a
domain name under which Internet users can directly register own names.

HTTP user agents can use it to avoid privacy-leaking "supercookies" and "super
domain" certificates. It is also use do highlight domain parts in a user interface
and sorting domain lists by site.
'
	),
	'curl' => array(
		'name' => 'curl',
		'upstream' => 'https://curl.haxx.se/',
		'source' => 'https://curl.haxx.se/download/curl-7.56.0.tar.xz',
		'version' => '7.56.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
Curl is a client to get documents and files from or send documents to a
server using any of the supported protocols (HTTP, HTTPS, FTP, FTPS,
TFTP, DICT, TELNET, LDAP, or FILE). The command is designed to work
without user interaction or any kind of interactivity.
'
	),
	'freetype2' => array(
		'name' => 'freetype2',
		'upstream' => 'http://www.freetype.org',
		'source' => 'http://download.savannah.gnu.org/releases/freetype/freetype-2.8.1.tar.bz2',
		'version' => '2.8.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
This library features TrueType fonts for open source projects. This
version also contains an autohinter for producing improved output.
'
	),
	'c-ares' => array(
		'name' => 'c-ares',
		'upstream' => 'http://daniel.haxx.se/projects/c-ares/',
		'source' => $download_dir . 'c-ares-1.7.5.tar.gz',
		'version' => '1.7.5',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
c-ares is a C library that performs DNS requests and name resolves 
asynchronously. c-ares is a fork of the library named &apos;ares&apos;, written 
by Greg Hudson at MIT.
'
	),
	'jpeg' => array(
		'name' => 'jpeg',
		'upstream' => 'http://www.ijg.org/',
		'source' => 'http://www.ijg.org/files/jpegsrc.v8d.tar.gz',
		'version' => '8d',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
This package is a library of functions that manipulate jpeg images, along
with simple clients for manipulating jpeg images.
'
	),
	'hermes' => array(
		'name' => 'Hermes',
		'upstream' => 'http://web.archive.org/web/20040202225109/http://www.clanlib.org/hermes/',
		'source' => $download_dir . 'Hermes-1.3.3.tar.bz2',
		'version' => '1.3.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
HERMES is a library designed to convert a source buffer with a specified pixel
format to a destination buffer with possibly a different format at the maximum
possible speed.

On x86 and MMX architectures, handwritten assembler routines are taking over
the job and doing it lightning fast.

On top of that, HERMES provides fast surface clearing, stretching and some
dithering. Supported platforms are basically all that have an ANSI C compiler
as there is no platform specific code but those are supported: DOS, Win32
(Visual C), Linux, FreeBSD (IRIX, Solaris are on hold at the moment), some BeOS
support.
'
	),
);

?>
