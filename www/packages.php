<?php

$basepackages = array(
	'binutils' => array(
		'name' => 'binutils',
		'upstream' => 'http://www.gnu.org/software/binutils/',
		'version' => '2.42',
		'date' => '20240309',
		'repo' => 'https://github.com/th-otto/binutils',
		'branch' => 'binutils-2_42-mint',
		'source' => 'https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'patch' => 1,
		'script' => 1,
		'crossscript' => 1,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 0,
		'D' => 0,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 1,
		'linux32' => 1,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GFDL-1.3-only AND GPL-3.0-or-later',
		'category' => 'Development/Tools/Building',
		'summary' => 'GNU Binutils',
		'comment' => '
The binutils are a collection of low-level language tools.<br />
The full documentation can be found
<a href="https://sourceware.org/binutils/docs-2.42/" ' . $href_target . '>here</a>.<br />
<br />
Note that official support for m68k-aout has been removed since binutils-2.31.<br />
This is a version where that support has been added back in.
<br />
<img src="images/newbutton.png" width="60" height="40" alt="New" />
For the mintelf toolchains, <a href="#gdb" alt="GDB">GDB</a> is now also available.
'
	),
	'binutils230' => array(
		'name' => 'binutils',
		'upstream' => 'http://www.gnu.org/software/binutils/',
		'version' => '2.30',
		'date' => '20180323',
		'repo' => 'https://github.com/th-otto/binutils',
		'branch' => 'binutils-2_30-mint',
		'source' => 'https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'patch' => 1,
		'script' => 1,
		'crossscript' => 0,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 0,
		'D' => 0,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 0,
		'license' => 'GFDL-1.3-only AND GPL-3.0-or-later',
		'category' => 'Development/Tools/Building',
		'summary' => 'GNU Binutils',
		'comment' => '
The binutils are a collection of low-level language tools.<br />
The full documentation can be found
<a href="https://sourceware.org/binutils/docs-2.30/" ' . $href_target . '>here</a>.<br />
<br />
Note that official support for m68k-aout has been removed in binutils-2.31.<br />
This is the last official version with support for it.
'
	),
	'gcc464' => array(
		'name' => 'gcc4',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '4.6.4',
		'date' => '20230719',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'mint/gcc-4.6',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2',
		'patch' => 1,
		'patchcomment' => 'This archive also contains an (experimental) patch for -mfastcall support.',
		'script' => 1,
		'crossscript' => 1,
		'doc' => 1,
		'elf' => 0,
		'fortran' => 0,
		'D' => 0,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 1,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The system GNU C Compiler',
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
<a href="http://gcc.gnu.org/onlinedocs/gcc-4.6.4/gcc/" ' . $href_target . '>here</a>.<br />
GCC contains everything to compile C programs, except a standard library and a math library.
'
	),
	'gcc1410' => array(
		'name' => 'gcc14',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '14.1.0',
		'date' => '20240507',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'mint/gcc-14',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain, and support for -mfastcall',
		'script' => 1,
		'crossscript' => 1,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 1,
		'D' => 1,
		'ada' => 1,
		'm2' => 1,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 1,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The system GNU C Compiler',
		'comment' => '
This is the currently most recent official version of GCC. It comes in two
flavours: one for an a.out toolchain (as with the previously used version
4.6.4), and one for an elf toolchain. Elf toolchain here means that it
will still produce the same executable format, but works with elf object
files. To support this better, all libraries offered here were also recompiled
using this format.<br />
<br />
<span style="color:red">Note:</span> This version now was compiled against fdlibm; it is strongly recommended to
use fdlibm instead of the ancient pml math library.
'
	),
	'gcc1320' => array(
		'name' => 'gcc13',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '13.2.0',
		'date' => '20230801',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'mint/gcc-13',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain, and support for -mfastcall.',
		'script' => 1,
		'crossscript' => 1,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 1,
		'D' => 1,
		'ada' => 1,
		'm2' => 1,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The system GNU C Compiler',
		'comment' => '
Slightly older version of GCC.
'
	),
	'gcc1230' => array(
		'name' => 'gcc12',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '12.3.0',
		'date' => '20230719',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'mint/gcc-12',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain.',
		'script' => 1,
		'crossscript' => 1,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 1,
		'D' => 1,
		'ada' => 1,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The system GNU C Compiler',
		'comment' => '
Slightly older version of GCC.
'
	),
	'gcc1140' => array(
		'name' => 'gcc11',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '11.4.0',
		'date' => '20230719',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'mint/gcc-11',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain.',
		'script' => 1,
		'crossscript' => 1,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 1,
		'D' => 1,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The system GNU C Compiler',
		'comment' => '
Slightly older version of GCC. <br />
'
	),
	'gcc1050' => array(
		'name' => 'gcc10',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '10.5.0',
		'date' => '20230719',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'mint/gcc-10',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain.',
		'script' => 1,
		'crossscript' => 1,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 1,
		'D' => 1,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 1,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The system GNU C Compiler',
		'comment' => '
Slightly older version of GCC.
'
	),
	'gcc950' => array(
		'name' => 'gcc9',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '9.5.0',
		'date' => '20230719',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'mint/gcc-9',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain.',
		'script' => 1,
		'crossscript' => 1,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 1,
		'D' => 0,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 1,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The system GNU C Compiler',
		'comment' => '
Slightly older version of GCC.
'
	),
	'gcc850' => array(
		'name' => 'gcc8',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '8.5.0',
		'date' => '20230719',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'mint/gcc-8',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain.',
		'script' => 1,
		'crossscript' => 1,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 1,
		'D' => 0,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 1,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The system GNU C Compiler',
		'comment' => '
Slightly older version of GCC.
'
	),
	'gcc750' => array(
		'name' => 'gcc7',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '7.5.0',
		'date' => '20230719',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'mint/gcc-7',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain.',
		'script' => 1,
		'crossscript' => 0,
		'doc' => 1,
		'elf' => 1,
		'fortran' => 0,
		'D' => 0,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 1,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The system GNU C Compiler',
		'comment' => '
Slightly older version of GCC.
'
	),
	'mintbin' => array(
		'name' => 'mintbin',
		'title' => 'MiNTBin',
		'upstream' => 'https://github.com/freemint/mintbin',
		'version' => '0.4',
		'date' => '20230911',
		'repo' => 'https://github.com/freemint/mintbin',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'patch' => 0,
		'script' => 1,
		'crossscript' => 0,
		'doc' => 0,
		'elf' => 1,
		'fortran' => 0,
		'D' => 0,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 1,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'atari' => 1,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Development/Tools/Building',
		'summary' => 'Supplementary tools to the GNU binutils for MiNT',
		'comment' => '
MiNTBin has been written by Guido Flohr. It is a set of tools for manipulating
the MiNT executables generated by <code>ld</code>. They are a complement to
the binutils. The main tools are <code>stack</code> for setting the stack size
of an executable, and <code>flags</code> for setting the header flags.
'
	),
	'gdb' => array(
		'name' => 'gdb',
		'title' => 'GDB',
		'upstream' => 'http://www.gnu.org/software/binutils/',
		'version' => '15.0',
		'date' => '20240309',
		'repo' => 'https://github.com/th-otto/binutils',
		'source' => 'https://ftp.gnu.org/gnu/binutils/binutils-2.42.tar.xz',
		'patch' => 0,
		'script' => 0,
		'crossscript' => 0,
		'doc' => 0,
		'elf' => 1,
		'fortran' => 0,
		'D' => 0,
		'ada' => 0,
		'm2' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 0,
		'mingw64' => 0,
		'linux32' => 1,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 0,
		'atari' => 1,
		'license' => 'GPL-3.0-only WITH GCC-exception-3.1 AND GPL-3.0-or-later AND LGPL-2.1-or-later AND LGPL-3.0-or-later',
		'category' => 'Development/Tools/Debuggers',
		'summary' => 'A GNU source-level debugger for C, C++, Fortran and other languages',
		'comment' => '
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.
<br />
Source & patches are part of the binutils package.
'
	),
);

$libpackages = array(
	'mintlib' => array(
		'name' => 'mintlib',
		'title' => 'MiNTLib',
		'upstream' => 'https://github.com/freemint/mintlib',
		'version' => '0.60.1',
		'date' => '20240428',
		'repo' => 'https://github.com/freemint/mintlib',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'System/Libraries',
		'summary' => 'Standard C Libraries for MiNT',
		'comment' => '
MiNTLib is a standard C library. It allows you to build software which runs on MiNT and TOS
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
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Public Domain',
		'category' => 'System/Libraries',
		'summary' => 'Portable Math Library',
		'comment' => '
PML stands for Portable Math Library.<br />
It works, but of course it is really slow on a 68000 without FPU.
<br />
For a comparison to fdlibm, see <a href="math.php">Math libraries for Atari</a>
<br />
<span style="color:red">Warning:</span>This library is deprecated. Use fdlibm instead.
'
	),
	'fdlibm' => array(
		'name' => 'fdlibm',
		'upstream' => 'https://www.netlib.org/fdlibm/',
		'version' => '20240425',
		'repo' => 'https://github.com/freemint/fdlibm/',
		'branch' => 'master',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Public Domain',
		'category' => 'System/Libraries',
		'summary' => 'Freely Distributable C math library',
		'comment' => '
fdlibm is a portable math library that was originally <br />
developed by Sun Microsystems. <br />
You should be able to use it at a replacement for PML,
but note that all packages provided here were compiled using PML.
<br />
For a comparison to PML, see <a href="math.php">Math libraries for Atari</a>
'
	),
	'gemlib' => array(
		'name' => 'gemlib',
		'title' => 'GEMlib',
		'upstream' => 'https://github.com/freemint/gemlib',
		'version' => '0.44.0',
		'date' => '20240425',
		'repo' => 'https://github.com/freemint/gemlib',
		'branch' => 'master',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Public Domain',
		'category' => 'System/Libraries',
		'summary' => 'GEM libraries and header files',
		'comment' => '
GEMlib allows you to write graphical programs using GEM.<br />
It is maintained by Arnaud Bercegeay; the official releases are available
on the <a href="http://arnaud.bercegeay.free.fr/gemlib">GEMlib&apos;s homepage</a>.
However, the latest sources are available
on the <a href="https://github.com/freemint/gemlib">FreeMiNT&apos;s GitHub repository</a>.
'
	),
	'cflib' => array(
		'name' => 'cflib',
		'title' => 'CFLIB',
		'upstream' => 'https://github.com/freemint/cflib',
		'version' => '21',
		'date' => '20240430',
		'repo' => 'https://github.com/freemint/cflib',
		'branch' => 'master',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'System/Libraries',
		'summary' => 'CFLIB is Christian Felsch&apos;s GEM utility library',
		'comment' => '
CFLIB is Christian Felsch&apos;s GEM utility library. It provide advanced controls,
such as check boxes, radio buttons, combo boxes... It also allows windowed
dialogs.<br />
BUG: On plain TOS, CFLIB makes intensive use of the GEM USERDEF feature.
Due to bad GEM design, USERDEF callbacks are called in supervisor mode using
the very small internal AES stack. Unfortunately, some GemLib functions such
as v_gtext() needs an insane amout of stack (more than 2 KB). So some USERDEF
callbacks quickly produces an AES internal stack overflow, and crash the entire
system.<br />
Concretely, due to this issue, programs using CFLIB work fine on XaAES
and TOS 4.04, but crash on TOS 1.62 and early versions of EmuTOS.
'
	),
	'gemma' => array(
		'name' => 'gemma',
		'upstream' => 'https://github.com/freemint/libgemma',
		'version' => 'git',
		'date' => '20181123',
		'repo' => 'https://github.com/freemint/libgemma',
		'branch' => 'master',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'System/Libraries',
		'summary' => 'Support library for GEM application programs',
		'comment' => '
Gemma is a support library for GEM application programs.
'
	),
	'zlib' => array(
		'name' => 'zlib',
		'upstream' => 'http://www.zlib.net/',
		'source' => 'http://www.zlib.net/%{name}-%{version}.tar.xz',
		'version' => '1.3',
		'date' => '20231115',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'Zlib',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Library implementing the DEFLATE compression algorithm',
		'comment' => '
zlib is a general-purpose lossless data-compression library,
implementing an API for the DEFLATE algorithm, the latter of
which is being used by, for example, gzip and the ZIP archive
format.
<br /><br />
This library is also available as a <a href="../sharedlibs.php#zlib">shared library.</a>
'
	),
	'libpng' => array(
		'name' => 'libpng',
		'upstream' => 'http://www.libpng.org/pub/png/libpng.html',
		'source' => 'https://ftp-osl.osuosl.org/pub/%{name}/src/libpng16/%{name}-%{version}.tar.xz',
		'version' => '1.6.39',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'Zlib',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Library for the Portable Network Graphics Format (PNG)',
		'comment' => '
Portable Network Graphics
<br />
An Open, Extensible Image Format with Lossless Compression 
<br /><br />
This library is also available as a <a href="../sharedlibs.php#libpng">shared library.</a>
'
	),
	'bzip2' => array(
		'name' => 'bzip2',
		'upstream' => 'https://www.sourceware.org/bzip2/',
		'source' => 'ftp://sourceware.org/pub/%{name}/%{name}-%{version}.tar.gz',
		'version' => '1.0.8',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 1,
		'rpm' => '1',
		'license' => 'BSD-3-Clause',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'A file compression utility',
		'comment' => '
bzip2 is a freely available, patent free (see below), high-quality data
compressor. It typically compresses files to within 10% to 15% of the
best available techniques (the PPM family of statistical compressors),
whilst being around twice as fast at compression and six times faster
at decompression.
<br /><br />
This library is also available as a <a href="../sharedlibs.php#bzip2">shared library.</a>
'
	),
	'ldg' => array(
		'name' => 'ldg',
		'title' => 'LDG',
		'upstream' => 'http://ldg.sourceforge.net/',
		'version' => '20171014',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'GEM Dynamic Libraries',
		'comment' => '
LDG stands for GEM Dynamic Libraries (actually Librairies Dynamiques
GEM in French). It&apos;s a system allowing GEM applications to load and to
share external modules. 
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
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A high level GEM library for TOS system',
		'comment' => '
Windom is a C library to make GEM programming very easy. With the help
of windom, you can focus on programming the real job of your
application, and let windom handle complex and "automatic" GEM stuff
(toolbar, forms, menu in windows...). <br />
<span style="color:red">Warning:</span> do not run make in the top level directory
after unpacking the source archive; the build system is utterly broken and will
remove your source directory.
'
	),
	'windom1' => array(
		'name' => 'windom1',
		'title' => 'WinDom',
		'upstream' => 'http://windom.sourceforge.net/',
		'version' => '1.21.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A high level GEM library for TOS system',
		'comment' => '
This is the 1.x release of windom.
'
	),
	'sdl' => array(
		'name' => 'SDL',
		'upstream' => 'https://www.libsdl.org/',
		'repo' => 'https://github.com/libsdl-org/SDL-1.2',
		'version' => '1.2.16-git',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/X11',
		'summary' => 'Simple DirectMedia Layer Library',
		'comment' => '
SDL is the Simple DirectMedia Layer library. It is a low-level and cross-platform
library for building games or similar programs.<br />
Thanks to Patrice Mandin, SDL is available on Atari platforms. SDL programs can
run either in full screen or in a GEM window, depending on the SDL_VIDEODRIVER
environment variable.<br />
<br />
Cross compiling hint: in many autoconf/automake based packages, the presence of SDL
is checked for by searching for a sdl-config script. Most likely, the one found will
be the one for your host system. This has the bad effect of adding absolute
search paths like /usr/include/SDL and /usr/lib. If that happens, you have to
manually edit config.status after running configure, and remove those flags.
In some cases, you have to add -I/usr/m68k-atari-mint/sys-root/usr/include/SDL instead.
'
	),
	'ncurses6' => array(
		'name' => 'ncurses',
		'upstream' => 'http://invisible-island.net/ncurses/ncurses.html',
		'source' => 'ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz',
		'version' => '6.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'System/Base',
		'summary' => 'Terminal control library',
		'comment' => '
Ncurses is a library which allows building full-screen text mode programs,
such as <code>vim</code>, <code>less</code>, or the GDB text UI.
'
	),
	'readline' => array(
		'name' => 'readline',
		'upstream' => 'https://cnswww.cns.cwru.edu/php/chet/readline/rltop.html',
		'source' => 'ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz',
		'version' => '7.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'The Readline Library',
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
		'source' => 'https://www.openssl.org/source/%{name}-%{version}.tar.gz',
		'version' => '1.1.1p',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'OpenSSL',
		'category' => 'Productivity/Networking/Security',
		'summary' => 'Secure Sockets and Transport Layer Security',
		'comment' => '
OpenSSL is a robust, commercial-grade, and full-featured toolkit for
the Transport Layer Security (TLS) and Secure Sockets Layer (SSL)
protocols. It is also a general-purpose cryptography library. 
'
	),
	'arc' => array(
		'name' => 'arc',
		'upstream' => 'http://arc.sourceforge.net/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '5.21p',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'Archiving tool for arc achives',
		'comment' => '
ARC is used to create and maintain file archives. An archive is a group
of files collected together into one file in such a way that the
individual files may be recovered intact.
'
	),
	'arj' => array(
		'name' => 'arj',
		'upstream' => 'http://arj.sourceforge.net/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '3.10.22',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'Archiver for .arj files',
		'comment' => '
A portable version of the ARJ archiver, available for a growing number
of DOS-like and UNIX-like platforms on a variety of architectures.
'
	),
	'lha' => array(
		'name' => 'lha',
		'upstream' => 'http://lha.sourceforge.jp/',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '1.14i',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'ISC',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'Archiver for .lzh files',
		'comment' => '
LHA for UNIX - Note: This software is licensed under the ORIGINAL
LICENSE. It is written in man/lha.n in Japanese 
'
	),
/*
	'unrar' => array(
		'name' => 'unrar',
		'title' => 'UnRAR',
		'upstream' => 'http://www.rarlab.com/',
		'source' => 'https://www.rarlab.com/rar/%{name}src-%{version}.tar.gz',
		'version' => '5.5.8',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'NonFree',
		'category' => 'Productivity/Archiving/Compression',
		'summmary' => 'A program to extract, test, and view RAR archives',
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
		'source' => $download_dir . '%{name}-%{version}.tar.zst',
		'version' => '5.4.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later AND GPL-2.0-or-later',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'A Program for Compressing Files with the Lempel&#8211;Ziv&#8211;Markov algorithm',
		'comment' => '
XZ Utils is free general-purpose data compression software with a high
compression ratio. XZ Utils were written for POSIX-like systems, but
also work on some not-so-POSIX systems. XZ Utils are the successor to
LZMA Utils. 
<br /><br />
This library is also available as a <a href="../sharedlibs.php#lzma">shared library.</a>
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
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'File compression program',
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
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'A program to unpack compressed files',
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
		'source' => 'http://ftp.math.utah.edu/pub/%{name}/%{name}-%{version}.tar.bz2',
		'version' => '2.10.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Public Domain',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'Pack Program',
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
		'source' => 'https://gmplib.org/download/%{name}/%{name}-%{version}.tar.xz',
		'version' => '6.2.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later and LGPL-3.0-or-later',
		'category' => 'System/Libraries',
		'summary' => 'The GNU MP Library',
		'comment' => '
A library for calculating huge numbers (integer and floating point).
'
	),
	'mpfr' => array(
		'name' => 'mpfr',
		'upstream' => 'http://www.mpfr.org/',
		'source' => 'http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.xz',
		'version' => '4.0.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-3.0-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'The GNU multiple-precision floating-point library',
		'comment' => '
The MPFR library is a C library for multiple-precision floating-point
computations with exact rounding (also called correct rounding). It is
based on the GMP multiple-precision library.
'
	),
	'mpc' => array(
		'name' => 'mpc',
		'upstream' => 'http://www.multiprecision.org/mpc/',
		'source' => 'ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz',
		'version' => '1.1.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-3.0-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'MPC multiple-precision complex shared library',
		'comment' => '
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as MPFR.
'
	),
	'tar' => array(
		'name' => 'tar',
		'upstream' => 'http://www.gnu.org/software/tar/',
		'source' => 'https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'version' => '1.34',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Productivity/Archiving/Backup',
		'summary' => 'GNU implementation of ((t)ape (ar)chiver)',
		'comment' => '
GNU Tar is an archiver program. It is used to create and manipulate files
that are actually collections of many other files; the program provides
users with an organized and systematic method of controlling a large amount
of data. Despite its name, that is an acronym of "tape archiver", GNU Tar
is able to direct its output to any available devices, files or other programs,
it is also able to access remote devices or files.
'
	),
	'libiconv' => array(
		'name' => 'libiconv',
		'upstream' => 'http://www.gnu.org/software/libiconv',
		'source' => 'http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz',
		'version' => '1.17',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later AND GPL-3.0-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Libiconv is a conversion library',
		'comment' => '
The libiconv library provides an iconv() implementation, for use on
systems which don&apos;t have one, or whose implementation cannot convert
from/to Unicode.<br /><br />
This library is also available as a <a href="../sharedlibs.php#libiconv">shared library.</a>
'
	),
	'm4' => array(
		'name' => 'm4',
		'title' => 'M4',
		'upstream' => 'https://www.gnu.org/software/m4/m4.html',
		'source' => 'ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'version' => '1.4.18',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/Other',
		'summary' => 'GNU m4',
		'comment' => '
GNU m4 is an implementation of the traditional Unix macro processor.
'
	),
	'flex' => array(
		'name' => 'flex',
		'upstream' => 'https://github.com/westes/flex',
		'source' => 'https://github.com/westes/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz',
		'version' => '2.6.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'Fast Lexical Analyzer Generator',
		'comment' => '
FLEX is a tool for generating scanners: programs that recognize lexical
patterns in text.
'
	),
	'bison' => array(
		'name' => 'bison',
		'upstream' => 'http://www.gnu.org/software/bison/bison.html',
		'source' => 'http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'version' => '3.6.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'The GNU Parser Generator',
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
		'source' => 'http://downloads.sourceforge.net/project/%{name}/%{name}/2.2.4/expat-%{version}.tar.bz2',
		'version' => '2.2.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'XML Parser Toolkit',
		'comment' => '
Expat is an XML parser library written in C. It is a stream-oriented
parser in which an application registers handlers for things the
parser might find in the XML document (like start tags).
'
	),
	'libidn2' => array(
		'name' => 'libidn2',
		'upstream' => 'https://www.gnu.org/software/libidn/#libidn2',
		'source' => 'ftp://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.lz',
		'version' => '2.0.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Support for Internationalized Domain Names (IDN) based on IDNA2008',
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
		'source' => 'http://web.mit.edu/kerberos/dist/krb5/1.15/%{name}-%{version}.tar.gz',
		'version' => '1.15.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Productivity/Networking/Security',
		'summary' => 'MIT Kerberos5 implementation',
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
		'source' => 'https://www.libssh2.org/download/%{name}-%{version}.tar.gz',
		'version' => '1.8.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A library implementing the SSH2 protocol',
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
		'source' => 'https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.xz',
		'version' => '1.26.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Implementation of Hypertext Transfer Protocol version 2 in C',
		'comment' => '
nghttp2 is an implementation of HTTP/2 and its header compression algorithm HPACK in C.
'
	),
	'libxml2' => array(
		'name' => 'libxml2',
		'upstream' => 'http://xmlsoft.org',
		'source' => 'ftp://xmlsoft.org/%{name}/%{name}-%{version}.tar.gz',
		'version' => '2.10.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'MIT',
		'category' => 'Development/Libraries',
		'summary' => 'A Library to Manipulate XML Files',
		'comment' => '
The XML C library was initially developed for the GNOME project. It is
now used by many programs to load and save extensible data structures
or manipulate any kind of XML files.
'
	),
	'libmetalink' => array(
		'name' => 'libmetalink',
		'upstream' => 'https://launchpad.net/libmetalink',
		'source' => 'https://github.com/metalink-dev/%{name}/releases/download/release-%{version}/libmetalink-%{version}.tar.xz',
		'version' => '0.1.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'System/Libraries',
		'summary' => 'Metalink Library',
		'comment' => '
Libmetalink is a Metalink library written in C language. It is intended to
provide the programs written in C to add Metalink functionality such as parsing
Metalink XML files.
'
	),
	'libunistring' => array(
		'name' => 'libunistring',
		'upstream' => 'http://www.gnu.org/software/libunistring/',
		'source' => 'http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'version' => '0.9.7',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-3.0-or-later OR GPL-2.0-only',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'GNU Unicode string library',
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
		'source' => 'https://github.com/rockdaboot/libpsl/releases/download/%{name}-%{version}/libpsl-%{version}.tar.lz',
		'version' => '0.21.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT AND MPL-2.0 AND BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'C library for the Publix Suffix List',
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
		'source' => 'https://curl.haxx.se/download/%{name}-%{version}.tar.xz',
		'version' => '7.56.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'curl',
		'category' => 'Productivity/Networking/Web/Utilities',
		'summary' => 'A Tool for Transferring Data from URLs',
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
		'source' => 'http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.bz2',
		'version' => '2.8.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 1,
		'rpm' => '2',
		'license' => 'GPL-2.0-or-later',
		'category' => 'System/Libraries',
		'summary' => 'A TrueType Font Library',
		'comment' => '
This library features TrueType fonts for open source projects. This
version also contains an autohinter for producing improved output.
<br /><br />
This library is also available as a <a href="../sharedlibs.php#freetype">shared library.</a>
'
	),
	'c-ares' => array(
		'name' => 'c-ares',
		'upstream' => 'http://daniel.haxx.se/projects/c-ares/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '1.7.5',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Library for asynchronous name resolves',
		'comment' => '
c-ares is a C library that performs DNS requests and name resolves 
asynchronously. c-ares is a fork of the library named &apos;ares&apos;, written 
by Greg Hudson at MIT.
'
	),
	'jpeg' => array(
		'name' => 'jpeg',
		'upstream' => 'http://www.ijg.org/',
		'source' => 'http://www.ijg.org/files/jpegsrc.v%{version}.tar.gz',
		'version' => '8d',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'rpm' => '3',
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A library for manipulating JPEG image files',
		'comment' => '
This package is a library of functions that manipulate jpeg images, along
with simple clients for manipulating jpeg images.
<br /><br />
This library is also available as a <a href="../sharedlibs.php#jpeg">shared library.</a>
'
	),
	'hermes' => array(
		'name' => 'Hermes',
		'upstream' => 'http://web.archive.org/web/20040202225109/http://www.clanlib.org/hermes/',
		'source' => $download_dir . '%{name}-%{version}.tar.bz2',
		'version' => '1.3.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A library to convert pixel formats',
		'comment' => '
HERMES is a library designed to convert a source buffer with a specified pixel
format to a destination buffer with possibly a different format at the maximum
possible speed.
<br />
On x86 and MMX architectures, handwritten assembler routines are taking over
the job and doing it lightning fast.
<br />
On top of that, HERMES provides fast surface clearing, stretching and some
dithering. Supported platforms are basically all that have an ANSI C compiler
as there is no platform specific code but those are supported: DOS, Win32
(Visual C), Linux, FreeBSD (IRIX, Solaris are on hold at the moment), some BeOS
support.
'
	),
	'gzip' => array(
		'name' => 'gzip',
		'upstream' => 'http://www.gnu.org/software/gzip/',
		'source' => 'http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'version' => '1.9',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'GNU Zip Compression Utilities',
		'comment' => '
Gzip reduces the size of the named files using Lempel-Ziv coding LZ77.
Whenever possible, each file is replaced by one with the extension .gz,
while keeping the same ownership modes and access and modification
times.
'
	),
	'grep' => array(
		'name' => 'grep',
		'upstream' => 'https://www.gnu.org/software/grep/',
		'source' => 'https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'version' => '3.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Productivity/Text/Utilities',
		'summary' => 'Print lines matching a pattern',
		'comment' => '
The grep command searches one or more input files for lines containing a
match to a specified pattern.  By default, grep prints the matching lines.
'
	),
	'ctris' => array(
		'name' => 'ctris',
		'upstream' => 'http://hackl.dhs.org/ctris/',
		'source' => $download_dir . '%{name}-%{version}.tar.bz2',
		'version' => '0.42',
		'patch' => 0,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Amusements/Games/Action/Arcade',
		'summary' => 'ctris is a curses based Tetris game',
		'comment' => '
ctris is a curses based Tetris game.
'
	),
	'dhcp' => array(
		'name' => 'dhcp',
		'upstream' => 'http://www.isc.org/software/dhcp',
		'source' => 'http://ftp.isc.org/isc/dhcp/%{version}/%{name}-%{version}.tar.gz',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '3.1.ESV',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Productivity/Networking/Boot/Servers',
		'summary' => 'Common Files Used by ISC DHCP Software',
		'comment' => '
The Dynamic Host Configuration Protocol (DHCP) is a network protocol
used to assign IP addresses and provide configuration information to
devices such as servers, desktops, or mobile devices, so they can
communicate on a network using the Internet Protocol (IP). ISC DHCP is
a collection of software that implements all aspects of the DHCP
(Dynamic Host Configuration Protocol) suite.
'
	),
	'gawk' => array(
		'name' => 'gawk',
		'upstream' => 'http://www.gnu.org/software/gawk/',
		'source' => 'http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'version' => '4.1.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Productivity/Text/Utilities',
		'summary' => 'GNU awk',
		'comment' => '
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.
'
	),
	'file' => array(
		'name' => 'file',
		'upstream' => 'http://www.darwinsys.com/file/',
		'source' => 'ftp://ftp.astron.com/pub/%{name}/%{name}-%{version}.tar.gz',
		'version' => '5.45',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-2-Clause',
		'category' => 'Productivity/File utilities',
		'summary' => 'A Tool to Determine File Types',
		'comment' => '
With the file command, you can obtain information on the file type of a
specified file. File type recognition is controlled by the file
/etc/magic, which contains the classification criteria. This command is
used by apsfilter to permit automatic printing of different file types.
'
	),
	'diffutils' => array(
		'name' => 'diffutils',
		'upstream' => 'https://www.gnu.org/software/diffutils/',
		'source' => 'https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'version' => '3.6',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GFDL-1.2 and GPL-3.0-or-later',
		'category' => 'Productivity/Text/Utilities',
		'summary' => 'GNU diff Utilities',
		'comment' => '
The GNU diff utilities find differences between files. diff is used to
make source code patches, for instance.
'
	),
	'findutils' => array(
		'name' => 'findutils',
		'upstream' => 'http://www.gnu.org/software/findutils/',
		'source' => 'http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz',
		'version' => '4.7.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Productivity/File utilities',
		'summary' => 'The GNU versions of find utilities (find and xargs)',
		'comment' => '
The findutils package contains programs which will help you locate
files on your system.  The find utility searches through a hierarchy
of directories looking for files which match a certain set of criteria
(such as a file name pattern).  The xargs utility builds and executes
command lines from standard input arguments (usually lists of file
names generated by the find command).
'
	),
	'coreutils' => array(
		'name' => 'coreutils',
		'upstream' => 'http://www.gnu.org/software/coreutils/',
		'source' => 'https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz',
		'version' => '8.32',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'System/Base',
		'summary' => 'GNU Core Utilities',
		'comment' => '
These are the GNU core utilities.  This package is the union of
the GNU fileutils, sh-utils, and textutils packages.
<br />
  [ arch b2sum base32 base64 basename cat chcon chgrp chmod chown chroot cksum
  comm cp csplit cut date dd df dir dircolors dirname du echo env expand expr
  factor false fmt fold groups head hostid id install join
  link ln logname ls md5sum mkdir mkfifo mknod mktemp mv nice nl nohup
  nproc numfmt od paste pathchk pinky pr printenv printf ptx pwd readlink
  realpath rm rmdir runcon seq sha1sum sha224sum sha256sum sha384sum sha512sum
  shred shuf sleep sort split stat stdbuf stty sum sync tac tail tee test
  timeout touch tr true truncate tsort tty uname unexpand uniq unlink
  uptime users vdir wc who whoami yes ]<br />
<br />
This package does not provide man pages, since those are generated automatically
by running the tools and parsing the --help message, which does not work when
cross-compiling. However that also means that those man pages do not
provide any useful information beyond what is available by just running
&lt;tool&gt; --help.
'
	),
	'bash' => array(
		'name' => 'bash',
		'upstream' => 'http://www.gnu.org/software/bash/bash.html',
		'source' => 'ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz',
		'version' => '4.4',
		'patchlevel' => '.23',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'System/Shells',
		'summary' => 'The GNU Bourne-Again Shell',
		'comment' => '
Bash is an sh-compatible command interpreter that executes commands
read from standard input or from a file.  Bash incorporates useful
features from the Korn and C shells (ksh and csh).  Bash is intended to
be a conformant implementation of the IEEE Posix Shell and Tools
specification (IEEE Working Group 1003.2).
<br />
<span style="color:red">Note:</span> /bin/sh is now a bash compiled
with minimal configuration (ie. no line editing features)
'
	),
	'make' => array(
		'name' => 'make',
		'upstream' => 'http://www.gnu.org/software/make/make.html',
		'source' => 'http://ftp.gnu.org/gnu/make/make-%{version}.tar.bz2',
		'version' => '4.2.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Development/Tools/Building',
		'summary' => 'GNU make',
		'comment' => '
The GNU make command with extensive documentation.
'
	),
	'patch' => array(
		'name' => 'patch',
		'upstream' => 'http://ftp.gnu.org/gnu/patch/',
		'source' => 'http://ftp.gnu.org/gnu/patch/%{name}-%{version}.tar.xz',
		'version' => '2.7.5',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Productivity/Text/Utilities',
		'summary' => 'GNU patch',
		'comment' => '
The GNU patch program is used to apply diffs between original and
changed files (generated by the diff command) to the original files.
'
	),
	'groff' => array(
		'name' => 'groff',
		'upstream' => 'http://www.gnu.org/software/groff/groff.html',
		'source' => 'ftp://ftp.gnu.org/gnu/groff/groff-%{version}.tar.gz',
		'version' => '1.22.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Productivity/Publishing/Troff',
		'summary' => 'GNU troff Document Formatting System',
		'comment' => '
Groff is used to "compile" man pages stored in groff or nroff format
for different output devices, for example, displaying to a screen or in
PostScript(tm) format for printing on a PostScript(tm) printer. Most
programs store their man pages in either <code>/usr/share/man/</code> or
<code>/usr/X11R6/man/</code>.
'
	),
	'git' => array(
		'name' => 'git',
		'upstream' => 'https://git-scm.com/',
		'source' => 'https://www.kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz',
		'version' => '2.21.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-only',
		'category' => 'Development/Tools/Version Control',
		'summary' => 'Fast, scalable, distributed revision control system',
		'comment' => '
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations and
full access to internals.
'
	),
	'ca-certificates' => array(
		'name' => 'ca-certificates',
		'upstream' => 'https://github.com/openSUSE/ca-certificates',
		'repo' => 'https://github.com/openSUSE/ca-certificates',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '10b2785',
		'patch' => 0,
		'script' => 1,
		'dev' => 0,
		'bin' => 0,
		'atari' => 0,
		'amiga' => 0,
		'noarch' => 1,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Productivity/Networking/Security',
		'summary' => 'Utilities for system wide CA certificate installation',
		'comment' => '
Update-ca-certificates is intended to keep the certificate stores of
SSL libraries like OpenSSL or GnuTLS in sync with the system&apos;s CA
certificate store that is managed by p11-kit.
'
	),
	/*
	'ca-certificates-mozilla' => array(
		'name' => 'ca-certificates-mozilla',
		'upstream' => 'http://www.mozilla.org',
		'source' => http://hg.mozilla.org/projects/nss/raw-file/default/lib/ckfw/builtins/certdata.txt',
		'version' => '2.22',
		'patch' => 0,
		'script' => 1,
		'dev' => 0,
		'bin' => 0,
		'atari' => 0,
		'amiga' => 0,
		'noarch' => 1,
		'license' => 'MPL-2.0',
		'category' => 'Productivity/Networking/Security',
		'summary' => 'CA certificates for OpenSSL',
		'comment' => '
This package contains some CA root certificates for OpenSSL extracted
from MozillaFirefox
'
	),
	*/
	'gdbm' => array(
		'name' => 'gdbm',
		'upstream' => 'https://www.gnu.org.ua/software/gdbm/',
		'source' => 'https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz',
		'version' => '1.12',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'System/Libraries',
		'summary' => 'GNU dbm key/data database',
		'comment' => '
GNU dbm is a library of database functions that use extensible
hashing and work similar to the standard UNIX dbm. These routines are
provided to a programmer needing to create and manipulate a hashed
database.
<br />
The basic use of GDBM is to store key/data pairs in a data file. Each
key must be unique and each key is paired with only one data item.
<br />
The library provides primitives for storing key/data pairs, searching
and retrieving the data by its key and deleting a key along with its
data. It also supports sequential iteration over all key/data pairs in
a database.
<br />
For compatibility with programs using old UNIX dbm functions, the
package also provides traditional dbm and ndbm interfaces.
'
	),
	'db' => array(
		'name' => 'db',
		'upstream' => 'http://oracle.com/technetwork/products/berkeleydb/',
		'source' => 'http://download.oracle.com/berkeley-db/db-%{version}.tar.gz',
		'version' => '4.8.30',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'System/Libraries',
		'summary' => 'Berkeley DB Database Library',
		'comment' => '
The Berkeley DB Database is a programmatic toolkit that provides
database support for applications.
'
	),
	'perl' => array(
		'name' => 'perl',
		'upstream' => 'http://www.perl.org/',
		'source' => 'http://www.cpan.org/src/5.0/perl-%{version}.tar.xz',
		'version' => '5.26.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Artistic-1.0 or GPL-2.0-or-later',
		'category' => 'Development/Languages/Perl',
		'summary' => 'The Perl interpreter',
		'comment' => '
perl - Practical Extraction and Report Language<br />
<br />
Perl is optimized for scanning arbitrary text files, extracting
information from those text files, and printing reports based on that
information.  It is also good for many system management tasks. Perl is
intended to be practical (easy to use, efficient, and complete) rather
than beautiful (tiny, elegant, and minimal).<br />
<br />
Some of the modules available on CPAN can be found in the "perl"
series.
'
	),
	'autoconf' => array(
		'name' => 'autoconf',
		'upstream' => 'http://www.gnu.org/software/autoconf',
		'source' => 'http://ftp.gnu.org/gnu/autoconf/%{name}-%{version}.tar.gz',
		'version' => '2.69',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 0,
		'atari' => 0,
		'amiga' => 0,
		'noarch' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Tools/Building',
		'summary' => 'A GNU Tool for Automatically Configuring Source Code',
		'comment' => '
GNU Autoconf is a tool for configuring source code and makefiles. Using
autoconf, programmers can create portable and configurable packages,
because the person building the package is allowed to specify various
configuration options.<br />
<br />
You should install autoconf if you are developing software and would
like to create shell scripts to configure your source code packages.<br />
<br />
Note that the autoconf package is not required for the end user who may
be configuring software with an autoconf-generated script; autoconf is
only required for the generation of the scripts, not their use.
'
	),
	'autoconf-archive' => array(
		'name' => 'autoconf-archive',
		'upstream' => 'https://savannah.gnu.org/projects/autoconf-archive',
		'source' => 'https://ftp.gnu.org/pub/gnu/autoconf-archive/%{name}-%{version}.tar.xz',
		'version' => '2023.02.20',
		'patch' => 0,
		'script' => 1,
		'dev' => 0,
		'bin' => 0,
		'atari' => 0,
		'amiga' => 0,
		'noarch' => 1,
		'license' => 'GPL-3.0-or-later WITH Autoconf-exception-3.0',
		'category' => 'Development/Tools/Building',
		'summary' => 'A Collection of macros for GNU autoconf',
		'comment' => '
The GNU Autoconf Archive is a collection of more than 450 macros for `GNU
Autoconf &lt;http://www.gnu.org/software/autoconf&gt;` that have been contributed as
free software by friendly supporters of the cause from all over the Internet.
Every single one of those macros can be re-used without imposing any
restrictions whatsoever on the licensing of the generated `configure` script. In
particular, it is possible to use all those macros in `configure` scripts that
are meant for non-free software. This policy is unusual for a Free Software
Foundation project. The FSF firmly believes that software ought to be free, and
software licenses like the GPL are specifically designed to ensure that
derivative work based on free software must be free as well. In case of
Autoconf, however, an exception has been made, because Autoconf is at such a
pivotal position in the software development tool chain that the benefits from
having this tool available as widely as possible outweigh the disadvantage that
some authors may choose to use it, too, for proprietary software.
'
	),
	'automake' => array(
		'name' => 'automake',
		'upstream' => 'https://www.gnu.org/software/automake',
		'source' => 'https://ftp.gnu.org/gnu/automake/%{name}-%{version}.tar.xz',
		'version' => '1.16',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 0,
		'atari' => 0,
		'amiga' => 0,
		'noarch' => 1,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Development/Tools/Building',
		'summary' => 'A Program for Automatically Generating GNU-Style Makefile.in Files',
		'comment' => '
Automake is a tool for automatically generating "Makefile.in" files
from "Makefile.am" files.  "Makefile.am" is a series of "make" macro
definitions (with rules occasionally thrown in).  The generated
"Makefile.in" files are compatible with the GNU Makefile standards.
'
	),
	'libbeecrypt' => array(
		'name' => 'libbeecrypt',
		'upstream' => 'http://sourceforge.net/projects/beecrypt',
		'source' => $download_dir . 'beecrypt-%{version}.tar.bz2',
		'version' => '4.1.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'An open source cryptography library',
		'comment' => '
BeeCrypt is an ongoing project to provide a strong and fast
cryptography toolkit. Includes entropy sources, random generators,
block ciphers, hash functions, message authentication codes,
multiprecision integer routines, and public key primitives.
'
	),
	'lua53' => array(
		'name' => 'lua53',
		'upstream' => 'http://www.lua.org',
		'source' => 'http://www.lua.org/ftp/lua-%{version}.tar.gz',
		'version' => '5.3.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Languages/Other',
		'summary' => 'Small Embeddable Language with Procedural Syntax',
		'comment' => '
Lua is a programming language originally designed for extending
applications, but is also frequently used as a general-purpose,
stand-alone language.<br />
<br />
Lua combines procedural syntax (similar to Pascal) with
data description constructs based on associative arrays and extensible
semantics. Lua is dynamically typed, interpreted from byte codes, and
has automatic memory management, making it suitable for configuration,
scripting, and rapid prototyping. Lua is implemented as a small library
of C functions, written in ANSI C.
'
	),
	'lua51' => array(
		'name' => 'lua51',
		'upstream' => 'http://www.lua.org',
		'source' => 'http://www.lua.org/ftp/lua-%{version}.tar.gz',
		'version' => '5.1.5',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Languages/Other',
		'summary' => 'Small Embeddable Language with Procedural Syntax',
		'comment' => '
Lua is a programming language originally designed for extending
applications, but is also frequently used as a general-purpose,
stand-alone language.<br />
<br />
Lua combines procedural syntax (similar to Pascal) with
data description constructs based on associative arrays and extensible
semantics. Lua is dynamically typed, interpreted from byte codes, and
has automatic memory management, making it suitable for configuration,
scripting, and rapid prototyping. Lua is implemented as a small library
of C functions, written in ANSI C.
'
	),
	'popt' => array(
		'name' => 'popt',
		'upstream' => 'http://www.rpm5.org/',
		'source' => 'http://rpm5.org/files/popt/popt-%{version}.tar.gz',
		'version' => '1.16',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A C library for parsing command line parameters',
		'comment' => '
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions. It
improves on them by allowing more powerful argument expansion. Popt can
parse arbitrary argv[] style arrays and automatically set variables
based on command line arguments.  Popt allows command line arguments to
be aliased via configuration files and includes utility functions for
parsing arbitrary strings into argv[] arrays using shell-like rules.
'
	),
	'rpm' => array(
		'name' => 'rpm',
		'upstream' => 'http://www.rpm.org/',
		'source' => 'http://ftp.rpm.org/releases/rpm-4.15.x/rpm-%{version}.tar.bz2',
		'version' => '4.15.1.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'System/Packages',
		'summary' => 'The RPM Package Manager',
		'comment' => '
The RPM Package Manager (RPM) is a powerful package management system capable of<br />
<br />
    <ul><li>building computer software from source into easily distributable packages</li>
    <li>installing, updating and uninstalling packaged software</li>
    <li>querying detailed information about the packaged software, whether installed or not</li>
    <li>verifying integrity of packaged software and resulting software installation</li></ul>
'
	),
	'rhash' => array(
		'name' => 'rhash',
		'upstream' => 'https://github.com/rhash/RHash',
		'source' => 'https://github.com/rhash/RHash/archive/v%{version}.tar.gz',
		'version' => '1.3.8',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Productivity/File utilities',
		'summary' => 'Recursive Hasher',
		'comment' => '
RHash (Recursive Hasher) is a console utility for computing and
verifying magnet links and hash sums of files.<br />
It supports CRC32, MD4, MD5, SHA1/SHA2, Tiger, DC++ TTH, BitTorrent
BTIH, AICH, eDonkey hash, GOST R 34.11-94, RIPEMD-160, HAS-160, EDON-R,
Whirlpool and Snefru hash algorithms. Hash sums are used to ensure and
verify integrity of large volumes of data for a long-term storing or
transferring.
'
	),
	'libarchive' => array(
		'name' => 'libarchive',
		'upstream' => 'http://rhash.anz.ru/?l=en',
		'source' => 'http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz',
		'version' => '3.3.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-2-Clause',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'Creates and reads several different streaming archive formats',
		'comment' => '
Libarchive is a programming library that can create and read several
different streaming archive formats, including most popular tar
variants and several cpio formats. It can also write shar archives and
read ISO9660 CDROM images. The bsdtar program is an implementation of
tar(1) that is built on top of libarchive. It started as a test
harness, but has grown and is now the standard system tar for FreeBSD 5
and 6.
'
	),
	'elfutils' => array(
		'name' => 'elfutils',
		'upstream' => 'https://sourceware.org/elfutils/',
		'source' => 'ftp://sourceware.org/pub/%{name}/%{version}/%{name}-%{version}.tar.bz2',
		'version' => '0.170',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Tools/Building',
		'summary' => 'Higher-level library to access ELF files',
		'comment' => '
elfutils is a collection of utilities and libraries to read, create
and modify ELF binary files, find and handle DWARF debug data,
symbols, thread state and stacktraces for processes and core files.
'
	),
	'libuv' => array(
		'name' => 'libuv',
		'upstream' => 'http://libuv.org',
		'source' => 'https://github.com/libuv/libuv/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz',
		'version' => '1.18.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Asychronous I/O support library',
		'comment' => '
libuv is a support library with a focus on asynchronous I/O. It was
primarily developed for use by Node.js, but it is also used by
Mozilla&apos;s Rust language, Luvit, Julia, pyuv, and others.
'
	),
	'cmake' => array(
		'name' => 'cmake',
		'upstream' => 'http://www.cmake.org/',
		'source' => 'http://www.cmake.org/files/v3.10/%{name}-%{version}.tar.gz',
		'version' => '3.10.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Tools/Building',
		'summary' => 'Cross-platform, open-source make system',
		'comment' => '
CMake is a cross-platform, open-source build system
'
	),
	'libsolv' => array(
		'name' => 'libsolv',
		'upstream' => 'https://github.com/openSUSE/libsolv',
		'source' => 'https://github.com/openSUSE/%{name}/archive/%{version}.tar.gz',
		'version' => '0.6.33',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Package dependency solver using a satisfiability algorithm',
		'comment' => '
libsolv is a library for solving packages and reading repositories.
The solver uses a satisfiability algorithm.
'
	),
	'python2' => array(
		'name' => 'python2',
		'upstream' => 'http://www.python.org/',
		'source' => 'http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz',
		'version' => '2.7.14',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Python-2.0',
		'category' => 'Development/Languages/Python',
		'summary' => 'Python Interpreter',
		'comment' => '
Python is an interpreted, object-oriented programming language, and is
often compared to Tcl, Perl, Scheme, or Java.  You can find an overview
of Python in the documentation and tutorials included in the python-doc
(HTML) or python-doc-pdf (PDF) packages.
'
	),
	'python3' => array(
		'name' => 'python3',
		'upstream' => 'http://www.python.org/',
		'source' => 'http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz',
		'version' => '3.11.8',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Python-2.0',
		'category' => 'Development/Languages/Python',
		'summary' => 'Python 3 Interpreter',
		'comment' => '
Python 3 is modern interpreted, object-oriented programming language,
often compared to Tcl, Perl, Scheme, or Java.  You can find an overview
of Python in the documentation and tutorials included in the python3-doc
package.
'
	),
	'libffi' => array(
		'name' => 'libffi',
		'upstream' => 'http://sourceware.org/libffi',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '3.2.1.git',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'Foreign Function Interface Library',
		'comment' => '
The libffi library provides a portable, high level programming
interface to various calling conventions.  This allows a programmer to
call any function specified by a call interface description at run
time.
'
	),
	'libgpg-error' => array(
		'name' => 'libgpg-error',
		'upstream' => 'http://www.gnupg.org/',
		'source' => 'ftp://ftp.gnupg.org/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2',
		'version' => '1.46',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later and LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Library That Defines Common Error Values for All GnuPG Components',
		'comment' => '
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon, and possibly more in the future.
'
	),
	'libassuan' => array(
		'name' => 'libassuan',
		'upstream' => 'http://www.gnupg.org/related_software/libassuan/index.en.html',
		'source' => 'ftp://ftp.gnupg.org/gcrypt/libassuan/%{name}-%{version}.tar.bz2',
		'version' => '2.5.5',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later and LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'IPC library used by GnuPG version 2',
		'comment' => '
Libassuan is the IPC library used by gpg2 (GnuPG version 2)
'
	),
	'gettext' => array(
		'name' => 'gettext',
		'upstream' => 'http://www.gnu.org/software/gettext/',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '0.19.8.1-2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later and LGPL-2.0-or-later',
		'category' => 'Development/Tools/Other',
		'summary' => 'Tools for Native Language Support (NLS)',
		'comment' => '
This package contains the intl library as well as tools that ease the
creation and maintenance of message catalogs. It allows you to extract
strings from source code. The supplied Emacs mode (po-mode.el) helps
editing these catalogs (called PO files, for portable object) and
adding translations. A special compiler turns these PO files into
binary catalogs.
'
	),
	'libksba' => array(
		'name' => 'libksba',
		'upstream' => 'http://www.gnupg.org/aegypten/',
		'source' => 'ftp://ftp.gnupg.org/gcrypt/libksba/%{name}-%{version}.tar.bz2',
		'version' => '1.6.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => '(LGPL-3.0-or-later or GPL-2.0-or-later) and GPL-3.0-or-later and MIT',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A X.509 Library',
		'comment' => '
KSBA is a library to simplify the task of working with X.509
certificates, CMS data, and related data.
'
	),
	'libgcrypt' => array(
		'name' => 'libgcrypt',
		'upstream' => 'http://directory.fsf.org/wiki/Libgcrypt',
		'source' => 'ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2',
		'version' => '1.10.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later AND LGPL-2.1-or-later AND GPL-3.0-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'The GNU Crypto Library',
		'comment' => '
Libgcrypt is a general purpose library of cryptographic building
blocks.  It is originally based on code used by GnuPG.  It does not
provide any implementation of OpenPGP or other protocols.  Thorough
understanding of applied cryptography is required to use Libgcrypt.
'
	),
	'giflib' => array(
		'name' => 'giflib',
		'upstream' => 'http://giflib.sf.net/',
		'source' => 'http://downloads.sf.net/giflib/%{name}-%{version}.tar.bz2',
		'version' => '5.1.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A Library for Working with GIF Images',
		'comment' => '
This Library allows manipulating GIF Image files. Since the LZW patents
have expired, giflib can again be used instead of libungif.
'
	),
	'libexif' => array(
		'name' => 'libexif',
		'upstream' => 'http://libexif.sourceforge.net',
		'source' => 'https://downloads.sourceforge.net/project/libexif/%{name}/%{version}/%{name}-%{version}.tar.bz2',
		'version' => '0.6.22',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'An EXIF Tag Parsing Library for Digital Cameras',
		'comment' => '
This library is used to parse EXIF information from JPEGs created by
digital cameras.
<br /><br />
This library is also available as a <a href="../sharedlibs.php#exif">shared library.</a>
'
	),
	'tiff' => array(
		'name' => 'tiff',
		'upstream' => 'http://www.simplesystems.org/libtiff/',
		'source' => 'http://download.osgeo.org/libtiff/%{name}-%{version}.tar.gz',
		'version' => '4.5.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'rpm' => '3',
		'license' => 'HPND',
		'category' => 'Productivity/Graphics/Convertors',
		'summary' => 'Tools for Converting from and to the Tagged Image File Format',
		'comment' => '
This package contains the library and support programs for the TIFF
image format.
<br /><br />
This library is also available as a <a href="../sharedlibs.php#tiff">shared library.</a>
'
	),
	'isl' => array(
		'name' => 'isl',
		'upstream' => 'http://isl.gforge.inria.fr/',
		'source' => 'http://isl.gforge.inria.fr/isl-%{version}.tar.xz',
		'version' => '0.20',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'Integer Set Library',
		'comment' => '
ISL is a library for manipulating sets and relations of integer points
bounded by linear constraints.
It is used by Cloog and the GCC Graphite optimization framework.
'
	),
	'libmikmod' => array(
		'name' => 'libmikmod',
		'upstream' => 'http://mikmod.raphnet.net/',
		'source' => 'http://sourceforge.net/projects/mikmod/files/%{name}/%{version}/%{name}-%{version}.tar.gz',
		'version' => '3.3.7',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'MikMod Sound Library',
		'comment' => '
Libmikmod is a portable sound library, capable of playing samples as
well as module files. It was originally written by Jean-Paul Mikkers
(MikMak) for DOS. It supports OSS /dev/dsp, ALSA, and Esound and can
also write wav files. Supported file formats include mod, stm, s3m,
mtm, xm, and it.
'
	),
	'libogg' => array(
		'name' => 'libogg',
		'upstream' => 'http://www.vorbis.com/',
		'source' => 'http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.xz',
		'version' => '1.3.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'amiga' => 1,
		'atari' => 1,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Languages/C and C++',
		'summary' => 'Ogg Bitstream Library',
		'comment' => '
Libogg is a library for manipulating Ogg bitstreams.  It handles both
making Ogg bitstreams and getting packets from Ogg bitstreams.
<br />
Ogg is the native bitstream format of libvorbis (Ogg Vorbis audio
codec) and libtheora (Theora video codec).
'
	),
	'flac' => array(
		'name' => 'flac',
		'upstream' => 'https://xiph.org/flac/',
		'source' => 'http://downloads.xiph.org/releases/flac/%{name}-%{version}.tar.xz',
		'version' => '1.3.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'BSD-3-Clause and GPL-2.0-or-later and GFDL-1.2',
		'category' => 'Productivity/Multimedia/Sound/Utilities',
		'summary' => 'Free Lossless Audio Codec',
		'comment' => '
FLAC is an audio coding format for lossless compression of digital
audio, and is also the name of the reference software package that
includes a codec implementation. Digital audio compressed by FLAC&apos;s
algorithm can typically be reduced to between 50 and 70 percent of
its original size, and decompresses to an identical copy of the
original audio data.
'
	),
	'libvorbis' => array(
		'name' => 'libvorbis',
		'upstream' => 'http://www.vorbis.com/',
		'source' => 'http://downloads.xiph.org/releases/vorbis/%{name}-%{version}.tar.xz',
		'version' => '1.3.6',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'The Vorbis General Audio Compression Codec',
		'comment' => '
Vorbis is a fully open, nonproprietary, patent-and-royalty-free, and
general-purpose compressed audio format for audio and music at fixed
and variable bit rates from 16 to 128 kbps/channel.
<br />
The native bitstream format of Vorbis is libogg (Ogg). Alternatively,
libmatroska (matroska) can also be used.
'
	),
	'vorbis-tools' => array(
		'name' => 'vorbis-tools',
		'upstream' => 'http://www.xiph.org/',
		'source' => 'http://downloads.xiph.org/releases/vorbis/%{name}-%{version}.tar.gz',
		'version' => '1.4.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0',
		'category' => 'Productivity/Multimedia/Sound/Utilities',
		'summary' => 'Ogg Vorbis Tools',
		'comment' => '
This package contains some tools for Ogg Vorbis:
<br />
oggenc (an encoder) and ogg123 (a playback tool). It also has vorbiscomment (to
add comments to Vorbis files), ogginfo (to give all useful information about an
Ogg file, including streams in it), oggdec (a simple command line decoder), and
vcut (which allows you to cut up Vorbis files).
'
	),
	'sdl_mixer' => array(
		'name' => 'SDL_mixer',
		'upstream' => 'http://libsdl.org/projects/SDL_mixer/release-1.2.html',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '1.2.13',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'Zlib',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'SDL sound mixer library',
		'comment' => '
A multichannel audio mixer. It supports four channels of 16-bit stereo
audio, plus a single channel of music, mixed by the popular MikMod MOD,
Timidity MIDI, and SMPEG MP3 libraries.<br />
<br />
Cross compiling hint: on modern platforms, it is sufficient to just link
against SDL_mixer, because the other libraries are referenced there as
shared libraries. Since for atari we have only static libraries, you
have to link those explicitly. The correct link command (order is important) is:<br />
<code>
-lSDL_mixer -lSDL -lFLAC -lvorbisfile -lvorbis -lmikmod -logg -lmpg123 -lgem -lm
</code><br />
See also other hints about SDL.
'
	),
	'sdl_image' => array(
		'name' => 'SDL_image',
		'upstream' => 'http://libsdl.org/projects/SDL_image/release-1.2.html',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '1.2.13',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/X11',
		'summary' => 'SDL image loading library',
		'comment' => '
This is a simple library to load images of various formats as SDL
surfaces. This library supports the BMP, PPM, PCX, GIF, JPEG, PNG,
TIFF and WEBP formats.
<br />
Cross compiling hint: on modern platforms, it is sufficient to just link
against SDL_images, because the other libraries are referenced there as
shared libraries. Since for atari we have only static libraries, you
have to link those explicitly. The correct link command (order is important) is:<br />
<code>
-lSDL -lSDL_image -ltiff -ljpeg -lpng -llzma -lz -lbz2 -lgem -lm
</code><br />
See also other hints about SDL.
'
	),
	'sdl_ttf' => array(
		'name' => 'SDL_ttf',
		'upstream' => 'http://libsdl.org/projects/SDL_ttf/release-1.2.html',
		'source' => $download_dir . '%{name}-%{version}.tar.bz2',
		'version' => '2.0.11',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'Zlib',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'SDL TrueType library',
		'comment' => '
This is a sample library that allows you to use TrueType fonts in your
SDL applications.
The correct link command (order is important) is:<br />
<code>
-lSDL -lSDL_ttf -lfreetype -lpng -lz -lbz2 -lgem -lm
</code><br />
See also other hints about SDL.
'
	),
	'sdl_net' => array(
		'name' => 'SDL_net',
		'upstream' => 'http://libsdl.org/projects/SDL_net/release-1.2.html',
		'source' => $download_dir . '%{name}-%{version}.tar.bz2',
		'version' => '1.2.8',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Zlib',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'SDL networking library',
		'comment' => '
This is a small cross-platform networking library for use with SDL.
'
	),
	/*
	'povray36pml' => array(
		'name' => 'povray',
		'upstream' => 'http://www.povray.org',
		'source' => $download_dir . '%{name}-%{version}.tar.bz2',
		'version' => '3.6.1',
		'date' => 'pml',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'AGPL-3.0 and CC-BY-SA-3.0',
		'category' => 'Productivity/Graphics/Visualization/Raytracers',
		'summary' => 'Ray Tracer',
		'comment' => '
The Persistence of Vision Ray tracer creates three-dimensional,
photo-realistic images using a rendering technique called ray tracing.
It reads in a text file containing information describing the objects
and lighting in a scene and generates an image of that scene from the
view point of a camera also described in the text file. Ray tracing is
not a fast process by any means, (the generation of a complex image can
take several hours) but it produces very high quality images with
realistic reflections, shading, perspective, and other effects.
<br /><br />
<span style="color:red">Note:</span> for testing purposes, povray 3.6 comes in 2 flavours. This
version was compiled with the pml math library.
'
	),
	*/
	'povray36fdlibm' => array(
		'name' => 'povray',
		'upstream' => 'http://www.povray.org',
		'source' => $download_dir . '%{name}-%{version}.tar.bz2',
		'version' => '3.6.1',
		'date' => 'fdlibm',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'AGPL-3.0 and CC-BY-SA-3.0',
		'category' => 'Productivity/Graphics/Visualization/Raytracers',
		'summary' => 'Ray Tracer',
		'comment' => '
The Persistence of Vision Ray tracer creates three-dimensional,
photo-realistic images using a rendering technique called ray tracing.
It reads in a text file containing information describing the objects
and lighting in a scene and generates an image of that scene from the
view point of a camera also described in the text file. Ray tracing is
not a fast process by any means, (the generation of a complex image can
take several hours) but it produces very high quality images with
realistic reflections, shading, perspective, and other effects.
'
/*
<br /><br />
<span style="color:red">Note:</span> for testing purposes, povray 3.6 comes in 2 flavours. This
version was compiled with the fdlibm math library.
*/
	),
	'smpeg' => array(
		'name' => 'smpeg',
		'upstream' => 'http://www.lokigames.com/development/smpeg.php3',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '0.4.5',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Software MPEG decoder',
		'comment' => '
SMPEG is based on UC Berkeley&apos;s mpeg_play software MPEG decoder
and SPLAY, an mpeg audio decoder created by Woo-jae Jung. We have
completed the initial work to wed these two projects in order to 
create a general purpose MPEG video/audio player.
'
	),
	'mpg123' => array(
		'name' => 'mpg123',
		'upstream' => 'http://www.mpg123.de/',
		'source' => 'https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.bz2',
		'version' => '1.25.10',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 1,
		'license' => 'LGPL-2.1-only',
		'category' => 'Productivity/Multimedia/Sound/Players',
		'summary' => 'Console MPEG audio player and decoder library',
		'comment' => '
The mpg123 distribution contains an MPEG 1.0/2.0/2.5 audio player/decoder for
layers 1, 2 and 3 (most commonly MPEG 1.0 Layer 3 aka MP3), as well as re-usable decoding
and output libraries.
'
	),
	'libtheora' => array(
		'name' => 'libtheora',
		'upstream' => 'http://www.theora.org/',
		'source' => 'http://downloads.xiph.org/releases/theora/%{name}-%{version}.tar.bz2',
		'version' => '1.1.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Theora video compression codec',
		'comment' => '
Theora is a free and open video compression format from the Xiph.org Foundation. Like all our 
multimedia technology it can be used to distribute film and video online and on disc without 
the licensing and royalty fees or vendor lock-in associated with other formats.
'
	),
	'ping' => array(
		'name' => 'ping',
		'upstream' => 'http://cvsweb.netbsd.org/bsdweb.cgi/basesrc/sbin/ping/',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '20190714',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'System/Base',
		'summary' => 'The ping command',
		'comment' => '
The ping command. <br />
Ported from BSD sources.
'
	),
	'libmad' => array(
		'name' => 'libmad',
		'upstream' => 'http://www.underbit.com/products/mad/',
		'source' => 'https://sourceforge.net/projects/mad/files/libmad/%{version}/libmad-%{version}.tar.gz',
		'version' => '0.15.1b',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Productivity/Multimedia/Other',
		'summary' => 'An MPEG audio decoder library',
		'comment' => '
MAD is a MPEG audio decoder. It currently supports MPEG-1 and the
MPEG-2 extension to Lower Sampling Frequencies, as well as the
so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are implemented.
<br />
MAD supports 24-bit PCM output. MAD computes using 100% fixed-point
(integer) computation, so you can run it without a floating point
unit.
'
	),
	'gnucobol' => array(
		'name' => 'gnucobol',
		'upstream' => 'https://sourceforge.net/projects/open-cobol/',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '3.0rc1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later AND LGPL-3.0-or-later',
		'category' => 'Development/Languages/Other',
		'summary' => 'COBOL compiler',
		'comment' => '
GnuCOBOL (formerly OpenCOBOL) is a COBOL compiler.
cobc translates COBOL to executable using intermediate C sources,
providing full access to nearly all C libraries. <br />
<span class="important">Note: this is not a cross-compiler. Do not install these on
a cross-development environment.</span>
'
	),
	'zstd' => array(
		'name' => 'zstd',
		'upstream' => 'http://www.zstd.net/',
		'repo' => 'https://github.com/facebook/zstd/releases',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '1.5.5',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause and GPL-2.0',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => 'Zstandard compression tools',
		'comment' => '
Zstd, short for Zstandard, is a lossless compression algorithm. Speed
vs. compression trade-off is configurable in small increments.
Decompression speed is preserved and remains roughly the same at all
settings, a property shared by most LZ compression algorithms, such
as zlib or lzma. <br />
 <br />
At roughly the same ratio, zstd (v1.4.0) achieves ~870% faster
compression than gzip. For roughly the same time, zstd achives a
~12% better ratio than gzip. LZMA outperforms zstd by ~10% faster
compression for the same ratio, or ~1-4% size reduction for same time.
'
	),
	'dosfstools' => array(
		'name' => 'dosfstools',
		'upstream' => '',
		'repo' => 'https://github.com/th-otto/dosfstools',
		'branch' => 'mint',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '4.1+git',
		'patch' => 0,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'System/Filesystems',
		'summary' => 'Utilities for Making and Checking FAT File Systems',
		'comment' => '
The dosfstools package includes the mkdosfs and dosfsck utilities, which
respectively make and check MS-DOS FAT file systems on hard drives or on
floppies.
'
	),
	'opkg' => array(
		'name' => 'opkg',
		'upstream' => 'https://git.yoctoproject.org/cgit/cgit.cgi/opkg/',
		'branch' => '',
		'source' => 'https://git.yoctoproject.org/cgit/cgit.cgi/%{name}/snapshot/%{name}-%{version}.tar.bz2',
		'version' => '0.6.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'System/Packages',
		'summary' => 'Opkg lightweight package management system',
		'comment' => '
Opkg is a lightweight distribution package manager, optimized for embedded applications and static image generation.

'
	),
	'tree' => array(
		'name' => 'tree',
		'upstream' => 'http://mama.indstate.edu/users/ice/tree/',
		'branch' => '',
		'source' => 'http://mama.indstate.edu/users/ice/tree/src/%{name}-%{version}.tgz',
		'version' => '1.8.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Productivity/File utilities',
		'summary' => 'File listing as a tree',
		'comment' => '
Tree is a recursive directory listing command that produces a depth
indented listing of files, which is colorized ala dircolors if the
LS_COLORS environment variable is set and output is to tty.
'
	),
	'libxmp' => array(
		'name' => 'libxmp',
		'upstream' => 'http://xmp.sourceforge.net/',
		'repo' => 'https://github.com/libxmp/libxmp',
		'branch' => '',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '4.6.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Module Player library for MOD, S3M, IT and others',
		'comment' => '
Libxmp is a library that renders module files to PCM data. It supports
over 90 mainstream and obscure module formats including Protracker (MOD),
Scream Tracker 3 (S3M), Fast Tracker II (XM), and Impulse Tracker (IT). <br />
 <br />
Many compressed module formats are supported, including popular Unix, DOS,
and Amiga file packers including gzip, bzip2, SQSH, Powerpack, etc.
 <br />
Contains small optimizations from mikrosk.
'
	),
	'libxmp-lite' => array(
		'name' => 'libxmp-lite',
		'upstream' => 'http://xmp.sourceforge.net/',
		'repo' => 'https://github.com/libxmp/libxmp',
		'branch' => '',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '4.6.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Module Player library for MOD, S3M, IT and others',
		'comment' => '
Lite version of Libxmp.
'
	),
	'asap' => array(
		'name' => 'asap',
		'upstream' => 'http://asap.sourceforge.net/',
		'branch' => '',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '5.0.1',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0',
		'category' => 'Productivity/Multimedia/Sound/Players',
		'summary' => 'Player of Atari 8-bit chiptunes',
		'comment' => '
ASAP is a player of Atari 8-bit chiptunes for modern computers and
mobile devices. It emulates the POKEY sound chip and the 6502
processor. The project was initially based on the routines from the
Atari800 emulator, but the current version has an original emulation
core.
'
	),
	'p7zip' => array(
		'name' => 'p7zip',
		'upstream' => 'http://p7zip.sourceforge.net/',
		'branch' => '',
		'source' => $download_dir . '%{name}-%{version}.tar.bz2',
		'version' => '16.02',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Productivity/Archiving/Compression',
		'summary' => '7-zip file compression program',
		'comment' => '
p7zip is a quick port of 7z.exe and 7za.exe (command line version of
7zip, see www.7-zip.org) for Unix. 7-Zip is a file archiver with
highest compression ratio. Since 4.10, p7zip (like 7-zip) supports
little-endian and big-endian machines. <br />
 <br />
This package provides: <br />
 * 7za - a stand-alone executable (handles less archive formats than 7z) <br />
 * p7zip - a gzip-like wrapper around 7zr/7za
'
	),
	'netpbm' => array(
		'name' => 'netpbm',
		'upstream' => 'http://netpbm.sourceforge.net/',
		'branch' => '',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '10.91.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause AND GPL-2.0-or-later AND IJG AND MIT',
		'category' => 'Productivity/Graphics/Convertors',
		'summary' => 'A Graphics Conversion Package',
		'comment' => '
These are the Portable Bitmap Plus Utilities. <br />
 <br />
This package provides tools for graphics conversion. Using these
tools, images can be converted from virtually any format into any
other format. A few of the supported formats include: GIF,
PC-Paintbrush, IFF ILBM, Gould Scanner file, MTV ray tracer, Atari
Degas .pi1 and .pi3, Macintosh PICT, HP Paintjet file, QRT raytracer,
AUTOCAD slide, Atari Spectrum (compressed and uncompressed), Andrew
Toolkit raster object, and many more. On top of that, man pages are
included for all tools.
'
	),
	'mksh' => array(
		'name' => 'mksh',
		'upstream' => 'http://www.mirbsd.org/mksh.htm',
		'branch' => '',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '57',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MirOS and ISC',
		'category' => 'System/Shells',
		'summary' => 'MirBSD Korn Shell',
		'comment' => '
The MirBSD Korn Shell is an actively developed free implementation of the Korn
Shell programming language and a successor to the Public Domain Korn Shell
(pdksh).
'
	),
	'cpio' => array(
		'name' => 'cpio',
		'upstream' => 'https://www.gnu.org/software/cpio/cpio.html',
		'branch' => '',
		'source' => 'https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2',
		'version' => '2.13',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'rpm' => '1',
		'license' => 'GPL-3.0',
		'category' => 'Productivity/Archiving/Backup',
		'summary' => 'A Backup and Archiving Utility',
		'comment' => '
GNU cpio is a program to manage archives of files. Cpio copies files
into or out of a cpio or tar archive. An archive is a file that contains
other files plus information about them, such as their pathname, owner,
time stamps, and access permissions. The archive can be another file on
the disk, a magnetic tape, or a pipe.
'
	),
	'libwebp' => array(
		'name' => 'libwebp',
		'upstream' => 'https://chromium.googlesource.com/webm/libwebp',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '1.3.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Library and tools for the WebP graphics format',
		'comment' => '
WebP codec is a library to encode and decode images in WebP format.
This package contains the library that can be used in other programs to
add WebP support, as well as the command line tools &apos;cwebp&apos; and &apos;dwebp&apos;
to compress and decompress images respectively.<br />
<br />
Original MiNT-Patch by medmed.
'
	),
	'pth' => array(
		'name' => 'pth',
		'upstream' => 'https://www.gnu.org/software/pth/',
		'source' => 'https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz',
		'version' => '2.0.7',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'GNU Pth threads library',
		'comment' => 'Pth is a very portable POSIX/ANSI-C
based library for Unix platforms which provides non-preemptive
priority-based scheduling for multiple threads of execution (aka
``multithreading&apos;&apos;) inside event-driven applications. All threads run
in the same address space of the server application, but each thread
has it&apos;s own individual program-counter, run-time stack, signal mask
and errno variable. <br />
<br />
The thread scheduling itself is done in a cooperative way, i.e., the
threads are managed by a priority- and event-based non-preemptive
scheduler. The intention is that this way one can achieve better
portability and run-time performance than with preemptive scheduling.
The event facility allows threads to wait until various types of events
occur, including pending I/O on filedescriptors, asynchronous signals,
elapsed timers, pending I/O on message ports, thread and process
termination, and even customized callback functions.<br />
<br />
Original MiNT-Patch by Patrice Mandin &amp; medmed.
'
	),
	'libyuv' => array(
		'name' => 'libyuv',
		'upstream' => 'https://chromium.googlesource.com/libyuv/libyuv/',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '1837',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Open source project that includes YUV scaling and conversion functionality',
		'comment' => '
libyuv is an open source project that includes YUV scaling and conversion functionality.
<br /><br />
You need to use g++ to link against this library.
'
	),
	'openh264' => array(
		'name' => 'openh264',
		'upstream' => 'https://github.com/cisco/openh264',
		'source' => 'https://github.com/cisco/openh264/archive/refs/tags/v2.3.0.tar.gz',
		'version' => '2.3.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-2-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Library which supports H.264 encoding and decoding',
		'comment' => '
OpenH264 is a codec library which supports H.264 encoding and decoding.
It is suitable for use in real time applications such as WebRTC. See
<a href="http://www.openh264.org/">http://www.openh264.org/</a> for more details.
<br /><br />
Needs the pth library from above.<br />
You need to use g++ to link against this library.
<br />
Original MiNT-Patch by medmed.<br />
A simple GEM example can be found in <a href="https://www.atari-forum.com/viewtopic.php?p=436559#p436559">this thread</a>
'
	),
	'fdk-aac' => array(
		'name' => 'fdk-aac',
		'upstream' => 'https://github.com/mstorsjo/fdk-aac',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '2.0.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'FDK-AAC',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A standalone library of the Fraunhofer FDK AAC code',
		'comment' => '
A standalone library of the Fraunhofer FDK AAC code from Android.
'
	),
	'mp4v2' => array(
		'name' => 'mp4v2',
		'upstream' => 'https://mp4v2.org/',
		'source' => 'https://github.com/enzo1982/mp4v2/archive/refs/tags/v%{version}.tar.gz',
		'version' => '2.1.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MPL-1.1',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'A C/C++ library to create, modify and read MP4 files',
		'comment' => '
The MP4v2 library provides an API to create and modify MP4 files as
defined by ISO-IEC:14496-1:2001 MPEG-4 Systems. This file format is
derived from Apple&apos;s QuickTime file format that has been used as a
multimedia file format in a variety of platforms and applications. It
is a very powerful and extensible format that can accommodate
practically any type of media.
'
	),
	'libsndfile' => array(
		'name' => 'libsndfile',
		'upstream' => 'https://github.com/libsndfile/libsndfile',
		'source' => 'https://github.com/libsndfile/libsndfile/releases/download/%{version}/%{name}-%{version}.tar.xz',
		'version' => '1.1.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'C library for reading and writing sound files',
		'comment' => '
libsndfile is a C library for reading and writing files containing sampled audio data.
'
	),
	'zita-resampler' => array(
		'name' => 'zita-resampler',
		'upstream' => 'https://kokkinizita.linuxaudio.org/linuxaudio/zita-resampler/resampler.html',
		'source' => 'https://kokkinizita.linuxaudio.org/linuxaudio/downloads/%{name}-%{version}.tar.bz2',
		'version' => '1.8.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-only',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'C++ library for resampling audio signals',
		'comment' => '
Libzita-resampler is a C++ library for resampling audio signals. It is
designed to be used within a real-time processing context, to be fast,
and to provide high-quality sample rate conversion.
<br /><br />
The library operates on signals represented in single-precision
floating point format. For multichannel operation both the input and
output signals are assumed to be stored as interleaved samples.
<br /><br />
The API allows a trade-off between quality and CPU load. For the latter
a range of approximately 1:6 is available. Even at the highest quality
setting libzita-resampler will be faster than most similar libraries,
e.g. libsamplerate.
<br /><br />
The source distribution includes the resample application. Input format
is any file readable by libsndfile, output is either WAV (WAVEX for
more than 2 channels) or CAF. Apart from resampling you can change the
sample format to 16-bit, 24-bit or float, and for 16-bit output, add
dithering. Available dithering types are rectangular, triangular, and
Lipschitz&apos; optimised error feedback filter. Some examples of dithering
can be seen <a href="https://kokkinizita.linuxaudio.org/linuxaudio/dithering.html">here</a>.
'
	),
	'wolfssl' => array(
		'name' => 'wolfssl',
		'upstream' => 'https://www.wolfssl.com/',
		'source' => $download_dir . '%{name}-%{version}.tar.bz2',
		'repo' => 'https://github.com/wolfssl/wolfssl',
		'version' => '5.5.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Productivity/Networking/Security',
		'summary' => 'Embedded TLS Library',
		'comment' => '
The wolfSSL embedded TLS library is a lightweight, portable,
C-language-based SSL/TLS library targeted at IoT, embedded, and RTOS
environments primarily because of its size, speed, and feature set. It
works seamlessly in desktop, enterprise, and cloud environments as
well. wolfSSL supports industry standards up to the current TLS 1.3 and
DTLS 1.3, is up to 20 times smaller than OpenSSL, offers a simple API,
an OpenSSL compatibility layer, OCSP and CRL support, is backed by the
robust wolfCrypt cryptography library, and much more.
'
	),
	'libde265' => array(
		'name' => 'libde265',
		'upstream' => 'https://github.com/strukturag/libde265/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'repo' => 'https://github.com/strukturag/libde265',
		'version' => '1.0.9',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Open h.265 codec implementation',
		'comment' => '
libde265 is an open source implementation of the h.265 video codec. It
is written from scratch and has a plain C API to enable a simple
integration into other software.
<br />
<br /><br />
Needs the pth library from above.<br />
You need to use g++ to link against this library.<br />
<br />
Original MiNT-Patch contributed by medmed.<br />
'
	),
	'x265' => array(
		'name' => 'x265',
		'upstream' => 'https://bitbucket.org/multicoreware/x265_git',
		'source' => 'https://bitbucket.org/multicoreware/x265_git/downloads/%{name}_%{version}.tar.gz',
		'repo' => 'https://bitbucket.org/multicoreware/x265_git',
		'version' => '3.5',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Productivity/Multimedia/Video/Editors and Convertors',
		'summary' => 'A free h265/HEVC encoder - encoder binary',
		'comment' => '
x265 is a free library for encoding next-generation H265/HEVC video
streams.
'
	),
	'libheif' => array(
		'name' => 'libheif',
		'upstream' => 'https://github.com/strukturag/libheif/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'repo' => 'https://github.com/strukturag/libheif',
		'version' => '1.14.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-3.0-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'HEIF and AVIF (AV1 Image File Format) file format decoder and encoder',
		'comment' => '
libheif is an ISO/IEC 23008-12:2017 HEIF and AVIF (AV1 Image File
Format) file format decoder and encoder.
<br />
HEIF and AVIF are new image file formats employing HEVC (h.265) or AV1
image coding, respectively, for the best compression ratios currently
possible.
<br />
libheif makes use of libde265 for HEIF image decoding and x265 for
encoding. For AVIF, libaom, dav1d, svt-av1, or rav1e are used as
codecs.
'
	),
	'mtm' => array(
		'name' => 'mtm',
		'upstream' => 'https://github.com/deadpixi/mtm/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'repo' => 'https://github.com/deadpixi/mtm/',
		'version' => '1.2.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'System/Console',
		'summary' => 'mtm is the Micro Terminal Multiplexer, a terminal multiplexer',
		'comment' => '
mtm is the Micro Terminal Multiplexer, a terminal multiplexer.<br />
<br />
Original MiNT-Patch contributed by medmed.
'
	),
	'man' => array(
		'name' => 'man',
		'upstream' => 'https://savannah.nongnu.org/projects/man-db',
		'source' => 'ftp://ftp.win.tue.nl/pub/linux/util/man/man-%{version}.tar.gz',
		'version' => '1.5g',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'System/Base',
		'summary' => 'A set of documentation tools: man, apropos and whatis',
		'comment' => '
The man package includes three tools for finding information and/or
documentation about your Linux system:  man, apropos and whatis.  The man
system formats and displays on-line manual pages about commands or
functions on your system.  Apropos searches the whatis database
(containing short descriptions of system commands) for a string.  Whatis
searches its own database for a complete word.<br />
<br />
The man package should be installed on your system because it is the
primary way for finding documentation.
'
	),
	'help2man' => array(
		'name' => 'help2man',
		'upstream' => 'https://www.gnu.org/software/help2man/',
		'source' => 'https://ftp.gnu.org/gnu/help2man/%{name}-%{version}.tar.xz',
		'version' => '1.49.3',
		'patch' => 0,
		'script' => 1,
		'dev' => 0,
		'bin' => 0,
		'atari' => 0,
		'amiga' => 0,
		'noarch' => 1,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Development/Tools/Doc Generators',
		'summary' => 'Script for generating man pages from --help output',
		'comment' => '
help2man is a script to create simple man pages from the --help and
--version output of programs.<br />
<br />
Since most GNU documentation is now in info format, this provides a way
to generate a placeholder man page pointing to that resource while
still providing some useful information.
'
	),
	'sed' => array(
		'name' => 'sed',
		'upstream' => 'https://www.gnu.org/software/sed/',
		'source' => 'https://ftp.gnu.org/gnu/sed/%{name}-%{version}.tar.xz',
		'version' => '4.9',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'System/Base',
		'summary' => 'A Stream-Oriented Non-Interactive Text Editor',
		'comment' => '
Sed takes text input, performs one or more operations on it, and
outputs the modified text. Sed is typically used for extracting parts
of a file using pattern matching or  for substituting multiple
occurrences of a string within a file.
'
	),
	'traceroute' => array(
		'name' => 'traceroute',
		'upstream' => 'ftp://ftp.ee.lbl.gov/',
		'source' => 'ftp://ftp.ee.lbl.gov/traceroute-1.4a5.tar.xz',
		'version' => '1.4a5',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Applications/Internet',
		'summary' => 'Traces the route taken by packets over a TCP/IP network',
		'comment' => '
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.  Traceroute displays
the IP number and host name (if possible) of the machines along the
route taken by the packets.  Traceroute is used as a network debugging
tool.  If you&apos;re having network connectivity problems, traceroute will
show you where the trouble is coming from along the route.<br />
<br />
Install traceroute if you need a tool for diagnosing network connectivity
problems.
'
	),
	'x3270' => array(
		'name' => 'x3270',
		'upstream' => 'https://github.com/pmattes/x3270',
		'source' => $download_dir . 'x3270-%{version}.tar.xz',
		'version' => '4.2ga9',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'System/X11/Terminals',
		'summary' => 'A Family of IBM 3270 Terminal Emulators',
		'comment' => '
This package contains a family of IBM 3270 mainframe terminal
emulators:<br />
<br />
* terminal emulators for interactive use x3270	X Window System
   c3270  curses based
<br />
* terminal emulators for scripted use s3270    see the x3270-script
   man page tcl3270  Tcl based
<br />
* printer emulator pr3287
<br />
x3270 is an IBM 3270 terminal emulator for the X Window System.  x3270
runs over a telnet connection (with or without TN3270E) and emulates
either an IBM 3279 (color) or 3278 (monochrome).  It supports APL2
characters, IND$FILE file transfer, NVT mode, a pop-up keypad for
3270-specific keys, alternative keymaps, 3287 printer sessions, and a
scrollbar and has extensive debugging and scripting facilities.
<br />
x3270a is a script that computes the correct font sizes for
higher-resolution displays, then runs x3270.
(x3270 handles scaling of visual elements automatically,
but it cannot adjust the font sizes by itself.)
<br />
b3270 is a generic back-end for 3270 emulators.
It implements the 3270 protocol and host input/output,
and communicates with a front end application using a simple XML-based protocol.
<br />
c3270 is the curses-based version of x3270.  It runs on any dumb
terminal (an xterm or a console, for example), and supports (almost)
all of the x3270 features.  c3270 scripts are compatible with x3270
scripts, and the subset of command line options and resource
definitions are also compatible.
<br />
s3270 is a scripting-only version of x3270.  This program is intended
primarily for writing "screen-scraping" applications, for example a CGI
back-end script that retrieves database information from a mainframe.
'
	),
	'wget' => array(
		'name' => 'wget',
		'source' => 'https://ftp.gnu.org/gnu/wget/%{name}-%{version}.tar.gz',
		'version' => '1.21.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Applications/Networking',
		'summary' => 'Retrieve files from the World Wide Web using HTTP and FTP',
		'comment' => '
Wget enables you to retrieve WWW documents or FTP files from a server.
This can be done in script files or via the command line.
'
	),
	'physfs' => array(
		'name' => 'physfs',
		'upstream' => 'https://www.icculus.org/physfs/',
		'source' => 'https://github.com/icculus/physfs/archive/refs/tags/release-%{version}.tar.gz',
		'version' => '3.2.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => '(CPL-1.0 OR LGPL-2.1-or-later) AND Zlib',
		'category' => 'System/Libraries',
		'summary' => 'PhysicsFS file abstraction layer for games',
		'comment' => '
PhysicsFS is a library to provide abstract access to various archives.
It is intended for use in video games, and the design was somewhat
inspired by Quake 3&apos;s file subsystem. The programmer defines a "write
directory" on the physical filesystem. No file writing done through the
PhysicsFS API can leave that write directory, for security. For
example, an embedded scripting language cannot write outside of this
path if it uses PhysFS for all of its I/O, which means that untrusted
scripts can run more safely. Symbolic links can be disabled as well,
for added safety. For file reading, the programmer lists directories
and archives that form a "search path". Once the search path is
defined, it becomes a single, transparent hierarchical filesystem. This
makes for easy access to ZIP files in the same way as you access a file
directly on the disk, and it makes it easy to ship a new archive that
will override a previous archive on a per-file basis. Finally,
PhysicsFS gives you platform-abstracted means to determine if CD-ROMs
are available, the user&apos;s home directory, where in the real filesystem
your program is running, etc.
'
	),
	'libedit' => array(
		'name' => 'libedit',
		'upstream' => 'https://www.thrysoee.dk/editline/',
		'source' => 'https://www.thrysoee.dk/editline/libedit-%{version}.tar.gz',
		'version' => '20230828-3.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Command Line Editing and History Library',
		'comment' => '
libedit is a command line editing and history library. It is designed
to be used by interactive programs that allow the user to type commands
at a terminal prompt.
'
	),
	'dash' => array(
		'name' => 'dash',
		'upstream' => 'http://gondor.apana.org.au/~herbert/dash/',
		'source' => 'http://gondor.apana.org.au/~herbert/dash/files/%{name}-%{version}.tar.gz',
		'version' => '0.5.12',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'System/Shells',
		'summary' => 'POSIX-compliant Implementation of /bin/sh',
		'comment' => '
DASH is a POSIX-compliant implementation of /bin/sh that aims to be as small as
possible without sacrificing speed where possible.
'
	),
	'xpdf' => array(
		'name' => 'xpdf',
		'upstream' => 'https://www.xpdfreader.com/',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '4.04',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later AND GPL-3.0-or-later',
		'category' => 'System/Shells',
		'summary' => 'A PDF file viewer',
		'comment' => '
The Xpdf open source project includes a PDF viewer along with a
collection of command line tools which perform various functions on PDF
files.
'
	),
	'libaacplus' => array(
		'name' => 'libaacplus',
		'upstream' => 'https://www.tipok.org.ua/node/17',
		/* 'source' => 'https://www.tipok.org.ua/downloads/media/aacplus/%{name}/%{name}-%{version}.tar.gz', */
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '2.0.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => '-',
		'category' => 'Development/Libraries/C and C++',
		'summary' => '3GPP AAC+ High Efficiency Advanced Audio Codec v2 (HE-AAC+) Encoder Library',
		'comment' => '
3GPP released reference implementation of 3GPP AAC Advanced Audio -
(HE-AAC+) Encoder (3GPP TS 26.410 V8.0.0).
<br />
Original MiNT-Patch by medmed.
'
	),
	'a52dec' => array(
		'name' => 'a52dec',
		'upstream' => 'https://git.adelielinux.org/community/a52dec/',
		'source' => 'https://distfiles.adelielinux.org/source/a52dec/%{name}-%{version}.tar.gz',
		'version' => '0.8.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'ATSC A/52 stream decoder library',
		'comment' => '
liba52 is a library for decoding ATSC A/52 streams.
'
	),
	'pixman' => array(
		'name' => 'pixman',
		'upstream' => 'https://gitlab.freedesktop.org/pixman/pixman',
		'source' => 'https://www.cairographics.org/releases/%{name}-%{version}.tar.gz',
		'version' => '0.42.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Pixel manipulation library',
		'comment' => '
Pixman is a pixel manipulation library for X and cairo.
'
	),
	'cairo' => array(
		'name' => 'cairo',
		'upstream' => 'https://cairographics.org',
		'source' => 'https://cairographics.org/releases/%{name}-%{version}.tar.xz',
		'version' => '1.18.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later OR MPL-1.1',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Vector Graphics Library with Cross-Device Output Support',
		'comment' => '
Cairo is a vector graphics library with cross-device output support.
Currently supported output targets include the X Window System,
in-memory image buffers, and PostScript. Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available.
'
	),
 	'libaom' => array(
		'name' => 'libaom',
		'upstream' => 'https://aomedia.googlesource.com/aom/',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '3.7.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-2-Clause',
		'category' => 'Productivity/Multimedia/Other',
		'summary' => 'AV1 codec library',
		'comment' => '
This is a library for AOMedia Video 1 (AV1), an open, royalty-free
video coding format designed for video transmissions over the Internet.
'
	),
 	'opus' => array(
		'name' => 'opus',
		'upstream' => 'https://opus-codec.org/',
		'source' => 'https://github.com/xiph/opus/releases/download/v%{version}/%{name}-%{version}.tar.gz',
		'version' => '1.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Audio Codec Library',
		'comment' => '
The Opus codec is designed for interactive speech and audio transmission over
the Internet. It is designed by the IETF Codec Working Group and incorporates
technology from Skype&apos;s SILK codec and Xiph.Org&apos;s CELT codec.
'
	),
 	'lame' => array(
		'name' => 'lame',
		'upstream' => 'https://lame.sourceforge.net/',
		'source' => 'http://prdownloads.sourceforge.net/lame/lame-%{version}.tar.gz',
		'version' => '3.100',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.0-or-later',
		'category' => 'Productivity/Multimedia/Sound/Editors and Convertors',
		'summary' => 'The LAME MP3 encoder',
		'comment' => '
LAME is an educational tool to be used for learning about MP3 encoding.
The goal of the LAME project is to use the open source model to improve the
psycho acoustics, noise shaping and speed of MP3.
Another goal of the LAME project is to use these improvements for the basis of
a patent free audio compression codec for the GNU project.
'
	),
 	'libvpx' => array(
		'name' => 'libvpx',
		'upstream' => 'https://www.webmproject.org/',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '1.13.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause AND GPL-2.0-or-later',
		'category' => 'Productivity/Multimedia/Other',
		'summary' => 'VP8/VP9 codec library',
		'comment' => '
WebM is an open, royalty-free, media file format designed for the web.
<br />
WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VP8 video codec
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.
'
	),
 	'x264' => array(
		'name' => 'x264',
		'upstream' => 'https://code.videolan.org/videolan/x264',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '20230215',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Productivity/Multimedia/Other',
		'summary' => 'H.264/MPEG-4 AVC format encoder',
		'comment' => '
x264 package provides a library for encoding video streams into the H.264/MPEG-4 AVC format. 
<br /><br />
Needs the pth library from above.<br />
'
	),
 	'fribidi' => array(
		'name' => 'fribidi',
		'upstream' => 'https://github.com/fribidi/fribidi',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'version' => '1.0.13',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-only',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'An implementation of the Unicode BiDi algorithm',
		'comment' => '
This library implements the algorithm as described in "Unicode
Standard Annex #9, the Bidirectional Algorithm,
http://www.unicode.org/unicode/reports/tr9/". FriBidi is
tested against the Bidi Reference Code and, to the best of the
developers&apos; knowledge, does not contain any conformance bugs.
<br />
The API was inspired by the document "Bi-Di languages support - BiDi
API proposal" by Franck Portaneri, which he wrote as a proposal for
adding BiDi support to Mozilla.
'
	),
 	'graphite2' => array(
		'name' => 'graphite2',
		'upstream' => 'http://graphite.sil.org/',
		'source' => 'https://github.com/silnrsi/graphite/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz',
		'version' => '1.3.14',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later OR LGPL-2.1-or-later OR MPL-2.0',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Font rendering capabilities for complex non-Roman writing systems',
		'comment' => '
Graphite2 is a project within SIL&apos;s Non-Roman Script Initiative and Language
Software Development groups to provide rendering capabilities for complex
non-Roman writing systems. Graphite can be used to create "smart fonts" capable
of displaying writing systems with various complex behaviors. With respect to
the Text Encoding Model, Graphite handles the "Rendering" aspect of writing
system implementation.
'
	),
 	'lcms2' => array(
		'name' => 'lcms2',
		'upstream' => 'https://www.littlecms.com/',
		'source' => 'https://github.com/mm2/Little-CMS/releases/download/lcms%{version}/lcms2-%{version}.tar.gz',
		'version' => '2.15',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'MIT',
		'category' => 'Productivity/Graphics/Other',
		'summary' => 'Little CMS Engine - A color management library and tools',
		'comment' => '
Littlecms is a small speed optimized color management engine.
Little CMS intends to be a small-footprint color management engine
with a special focus on accuracy and performance. It uses the International
Color Consortium standard (ICC), which is the modern standard when
regarding to color management. The ICC specification is widely used and is
referred to in many International and other de-facto standards.
'
	),
 	'faad2' => array(
		'name' => 'faad2',
		'upstream' => 'https://github.com/knik0/faad2',
		'source' => 'https://github.com/knik0/faad2/archive/refs/tags/%{version}.tar.gz',
		'version' => '2.10.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-2.0-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'Freeware Advanced Audio (AAC) Decoder including SBR decoding',
		'comment' => '
FAAD2 is a HE, LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder.
FAAD2 includes code for SBR (HE AAC) decoding.
FAAD2 is licensed under the GPL.
'
	),
 	'ffmpeg' => array(
		'name' => 'ffmpeg',
		'upstream' => 'https://ffmpeg.org/',
		'source' => 'https://github.com/silnrsi/graphite/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz',
		'version' => '6.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'Productivity/Multimedia/Video/Editors and Convertors',
		'summary' => 'Set of libraries for working with various multimedia formats',
		'comment' => '
FFmpeg is a multimedia framework, able to decode, encode,
transcode, mux, demux, stream, filter and play several formats
that humans and machines have created.
'
	),
 	'sdl_gfx' => array(
		'name' => 'SDL_gfx',
		'upstream' => 'http://www.ferzkopp.net/wordpress/2016/01/02/sdl_gfx-sdl2_gfx/',
		'source' => 'http://www.ferzkopp.net/Software/SDL_gfx-2.0/%{name}-%{version}.tar.gz',
		'version' => '2.0.26',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Zlib',
		'category' => 'Development/Libraries/X11',
		'summary' => 'SDL Graphics Routines for Primitives and Other Support Functions',
		'comment' => '
The SDL_gfx library evolved out of the SDL_gfxPrimitives code which
provided basic drawing routines such as lines, circles or polygons and
SDL_rotozoom which implemented a interpolating rotozoomer for SDL
surfaces. The current components of the SDL_gfx library are:
<ul>
<li>Graphic Primitives (SDL_gfxPrimitves.h)</li>
<li>Rotozoomer (SDL_rotozoom.h)</li>
<li>Framerate control (SDL_framerate.h)</li>
<li>MMX image filters (SDL_imageFilter.h)</li>
</ul>
The library is backwards compatible to the above mentioned code. It is
written in plain C and can be used in C++ code.
'
	),
 	'sdl_sound' => array(
		'name' => 'SDL_sound',
		'repo' => 'https://github.com/icculus/SDL_sound',
		'branch' => 'stable-1.0',
		'upstream' => 'https://icculus.org/SDL_sound/',
		'version' => '1.0.4',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/C and C++',
		'summary' => 'SDL_sound; an abstract soundfile decoder.',
		'comment' => '
SDL_sound is a library that handles the decoding of several popular
sound file formats, such as .WAV and .MP3. It is meant to make the
programmer&apos;s sound playback tasks simpler. The programmer gives
SDL_sound a filename, or feeds it data directly from one of many
sources, and then reads the decoded waveform data back at their
leisure. If resource constraints are a concern, SDL_sound can process
sound data in programmer-specified blocks. Alternately, SDL_sound can
decode a whole sound file and hand back a single pointer to the whole
waveform. SDL_sound can also handle sample rate, audio format, and
channel conversion on-the-fly and behind-the-scenes, if the programmer
desires.
'
	),
 	'sqlite3' => array(
		'name' => 'sqlite3',
		'repo' => 'https://github.com/sqlite/sqlite',
		'upstream' => 'https://www.sqlite.org/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '3.44.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Public-Domain',
		'category' => 'Productivity/Databases/Servers',
		'summary' => 'Embeddable SQL Database Engine',
		'comment' => '
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.
<br />
SQLite is not a client library used to connect to a big database
server. SQLite is a server and the SQLite library reads and writes
directly to and from the database files on disk.
<br />
SQLite can be used via the sqlite command line tool or via any
application that supports the Qt database plug-ins.
'
	),
 	'fltk' => array(
		'name' => 'fltk',
		'repo' => 'https://github.com/fltk/fltk',
		'upstream' => 'https://www.fltk.org/',
		'version' => '1.3.9',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'noelf' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'LGPL-2.1-or-later',
		'category' => 'Development/Libraries/X11',
		'summary' => 'C++ GUI Toolkit for the X Window System, OpenGL, and WIN32',
		'comment' => '
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a cross-platform C++ GUI toolkit for
for the X Window System), Microsoft&#x00AE; Windows&#x00AE;, and macOS&#x00AE;.
FLTK provides modern GUI functionality without the bloat and
supports 3D graphics via OpenGL&#x00AE; and its built-in GLUT
emulation. It was originally developed by Mr. Bill Spitzak
and is currently maintained by a small group of developers
across the world with a central repository on GitHub.
<br/><br/>
<span style="color:red">Note:</span> You&apos;ll need the <a href="/download/rpm/RPMS/noarch/index.php">X11-Libaries</a> to
compile FLTK applications for Atari, and a <a href="/download/rpm/RPMS/m68020/index.php#XServer">X-Server</a> to run them.
'
	),
 	'dillo' => array(
		'name' => 'dillo',
		'repo' => 'https://github.com/dillo-browser/dillo',
		'upstream' => 'https://web.archive.org/web/20220518060405/https://www.dillo.org/',
		'version' => '3.1-dev',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'noelf' => 1,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'GPL-3.0-or-later',
		'category' => 'X11/Applications',
		'summary' => 'Dillo is a multi-platform graphical web browser',
		'comment' => '
Dillo is a minimalistic web browser particularly intended for older or
slower computers and embedded systems. It supports only plain
HTML/XHTML (with CSS rendering) and images over HTTP; scripting is
ignored entirely. Current versions of Dillo can run on Linux,
BSD, OS X, IRIX and Cygwin. Due to its small size, it is the browser
of choice in several space-conscious Linux distributions.
<br/><br/>
<span style="color:red">Note:</span> You&apos;ll need a <a href="/download/rpm/RPMS/m68020/index.php#XServer">X-Server</a> to run it.
'
	),
 	'ntp' => array(
		'name' => 'ntp',
		'upstream' => 'http://www.ntp.org/',
		'version' => '4.2.8p17',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'noelf' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'BSD-3-Clause AND MIT AND BSD-4-Clause AND GPL-2.0-only',
		'category' => 'Productivity/Networking/Other',
		'summary' => 'Network Time Protocol daemon (version 4)',
		'comment' => '
The Network Time Protocol (NTP) is used to synchronize the time of a
computer client or server to another server or reference time source,
such as a radio, satellite receiver, or modem.
<br/><br/>
Ntpd is an operating system daemon that sets and maintains the system
time-of-day synchronized with Internet standard time servers.
'
	),
 	'meson' => array(
		'name' => 'meson',
		'upstream' => 'https://mesonbuild.com/',
		'version' => '1.4.0',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'noelf' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Apache-2.0',
		'category' => 'Development/Tools/Building',
		'summary' => 'Python-based build system',
		'comment' => '
Meson is a build system designed to optimise programmer productivity.
It aims to do this by providing support for software development
tools and practices, such as unit tests, coverage reports, Valgrind,
CCache and the like. Supported languages include C, C++, Fortran,
Java, Rust. Build definitions are written in a non-turing complete
Domain Specific Language.
<br/><br/>
Requires python3 >= 3.7
<br/><br/>
Note: the meson-dev package just contains the cross configuration files.
Use them with `meson setup --crossfile m68k-atari-mint.ini`
'
	),
 	'ninja' => array(
		'name' => 'ninja',
		'upstream' => 'https://ninja-build.org/',
		'version' => '1.11.1',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'noelf' => 0,
		'atari' => 1,
		'amiga' => 0,
		'license' => 'Apache-2.0',
		'category' => 'Development/Tools/Building',
		'summary' => 'A small build system closest in spirit to Make',
		'comment' => '
Ninja is yet another build system. It takes as input the interdependencies
of files (typically source code and output executables) and orchestrates
building them, quickly.
'
	),
/*
	'vttest' => array(
		'name' => 'vttest',
		'upstream' => 'http://invisible-island.net/vttest/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'version' => '20190710',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'atari' => 1,
		'amiga' => 0,
		'comment' => '
vttest is a program to test the compatibility (or to demonstrate the non-compatibility) of so-called "VT100-compatible" terminals.
'
	),
*/
);

?>
