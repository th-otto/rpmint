Summary       : Various compilers (C, C++, Objective-C, Chill, ...)
Name          : gcc2
Version       : 2.95.3
release       : 6
Copyright     : GPL
Group         : Development/Languages

Packager      : Keith Scroggins <kws@radix.net>
Vendor        : Sparemint
URL           : http://gcc.gnu.org/

Requires      : binutils
Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}.tar.gz
Source1: README.MiNT
Patch0:  gcc-2.95.2-warn.patch
Patch1:  gcc-2.95.3-mint-assert.patch
Patch2:  gcc-2.95.3-mint-config.patch
Patch3:  gcc-2.95.3-mint-make.patch
Patch4:  gcc-2.95.3-mint-target.patch
Patch5:  gcc-2.95.3-mintlib-c++.patch
Patch6:  gcc-2.95.3-bison-1.875.patch


%define STDC_VERSION 2.10.0
%define TARGET m68k-atari-mint


%description
The gcc package contains the GNU Compiler Collection: cc and gcc. You'll need
this package in order to compile C code.

%package c++
Summary       : C++ support for gcc
Group         : Development/Languages
Requires      : gcc2 = %{version}

%description c++
This package adds C++ support to the GNU C compiler. It includes support
for most of the current C++ specification, including templates and
exception handling. It does include the static standard C++
library and C++ header files.

%package objc
Summary       : Objective C support for gcc
Group         : Development/Languages
Requires      : gcc2 = %{version}

%description objc
gcc-objc provides Objective C support for the GNU C compiler (gcc).
Mainly used on systems running NeXTSTEP, Objective C is an
object-oriented derivative of the C language.

Install gcc-objc if you are going to do Objective C development and
you would like to use the gcc compiler.  You'll also need gcc.

%package g77
Summary       : Fortran 77 support for gcc
Group         : Development/Languages
Requires      : gcc2 = %{version}

%description g77
The gcc-g77 package provides support for compiling Fortran 77
programs with the GNU gcc compiler.

You should install gcc-g77 if you are going to do Fortran development
and you would like to use the gcc compiler.  You will also need gcc.

%package chill
Summary       : CHILL support for gcc
Group         : Development/Languages
Requires      : gcc2 = %{version}

%description chill
This package adds support for compiling CHILL programs with the GNU
compiler.

Chill is the "CCITT High-Level Language", where CCITT is the old
name for what is now ITU, the International Telecommunications Union.
It is is language in the Modula2 family, and targets many of the
same applications as Ada (especially large embedded systems).
Chill was never used much in the United States, but is still
being used in Europe, Brazil, Korea, and other places.

%package java
Summary       : Java support for gcc
Group         : Development/Languages
Requires      : gcc2 = %{version}

%description java
This package adds experimental support for compiling Java(tm) programs and
bytecode into native code. To use this you will also need the gcc-libgcj
package.
Note: gcc-libgcj is currently not available for m68k-atari-mint!


%prep
%setup -q -n gcc-2.95.3
#%patch0 -p1 -b .warn
%patch1 -p1 -b .mint-assert
%patch2 -p1 -b .mint-config
%patch3 -p1 -b .mint-make
%patch4 -p1 -b .mint-target
%patch5 -p1 -b .mintlib-c++
%patch6 -p1 -b .bison


%build
rm -rf build-%{TARGET}
mkdir build-%{TARGET}
cd build-%{TARGET}

# 
# C++ with simple optimization, C++ Optimizer seems to be buggy
# 
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
CXXFLAGS="${RPM_OPT_FLAGS} -O -D_GNU_SOURCE" \
CC=gcc-2.95.3 CXX=g++-2.95.3 \
../configure \
	--with-gnu-ld \
	--with-gnu-as \
	--program-suffix=-2.95.3 \
	--prefix=%{_prefix} \
	--target=%{TARGET} \
	--host=%{TARGET}

# rerun bison
# touch ../gcc/*.y

# don't run bison
touch ../gcc/*.h ../gcc/*.c
touch ../gcc/*/*.h ../gcc/*/*.c
touch ../gcc/*/*/*.h ../gcc/*/*/*.c

# as I have already installed the gcc 2.95.2 and compiled
# it several times there is no reason to bootstrap the
# compiler again and again
# it save lot of time to skip stage1 and stage2 and go
# directly to stage3
#make bootstrap ||:
make

# run the tests - not possible yet
# make -k check || true


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd build-%{TARGET}
make prefix=${RPM_BUILD_ROOT}%{_prefix} install

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

FULLVER=`${RPM_BUILD_ROOT}%{_prefix}/bin/%{TARGET}-gcc --version | cut -d' ' -f1`
FULLPATH=$(dirname ${RPM_BUILD_ROOT}%{_prefix}/lib/gcc-lib/%{TARGET}/${FULLVER}/cc1)

strip ${FULLPATH}/cc1
strip ${FULLPATH}/cc1chill
strip ${FULLPATH}/cc1obj
strip ${FULLPATH}/cc1plus
strip ${FULLPATH}/collect2
strip ${FULLPATH}/cpp0
strip ${FULLPATH}/f771
strip ${FULLPATH}/jc1
strip ${FULLPATH}/jvgenmain

# fix some things
rm -f ${RPM_BUILD_ROOT}%{_prefix}/info/dir
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/*.info*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/*/*

rm -f ${RPM_BUILD_ROOT}%{_prefix}/bin/c++-2.95.3

#ln -sf g++-2.95.3 ${RPM_BUILD_ROOT}%{_prefix}/bin/c++-2.95.3
ln -sf gcc-2.95.3 ${RPM_BUILD_ROOT}%{_prefix}/bin/cc-2.95.3
ln -sf g77-2.95.3 ${RPM_BUILD_ROOT}%{_prefix}/bin/f77-2.95.3
ln -sf cccp-2.95.3.1.gz ${RPM_BUILD_ROOT}%{_prefix}/man/man1/cpp-2.95.3.1.gz

# --program-suffix does not appear to work....

mv ${RPM_BUILD_ROOT}%{_prefix}/man/man1/cccp.1.gz ${RPM_BUILD_ROOT}%{_prefix}/man/man1/cccp-2.95.3.1.gz
mv ${RPM_BUILD_ROOT}%{_prefix}/man/man1/gcc.1.gz ${RPM_BUILD_ROOT}%{_prefix}/man/man1/gcc-2.95.3.1.gz
mv ${RPM_BUILD_ROOT}%{_prefix}/man/man1/g77.1.gz ${RPM_BUILD_ROOT}%{_prefix}/man/man1/g77-2.95.3.1.gz
mv ${RPM_BUILD_ROOT}%{_prefix}/man/man1/g++.1.gz ${RPM_BUILD_ROOT}%{_prefix}/man/man1/g++-2.95.3.1.gz

mv ${RPM_BUILD_ROOT}%{_prefix}/bin/c++ ${RPM_BUILD_ROOT}%{_prefix}/bin/c++-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/c++filt ${RPM_BUILD_ROOT}%{_prefix}/bin/c++filt-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/chill ${RPM_BUILD_ROOT}%{_prefix}/bin/chill-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/cpp ${RPM_BUILD_ROOT}%{_prefix}/bin/cpp-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/g++ ${RPM_BUILD_ROOT}%{_prefix}/bin/g++-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/g77 ${RPM_BUILD_ROOT}%{_prefix}/bin/g77-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/gcc ${RPM_BUILD_ROOT}%{_prefix}/bin/gcc-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/gcj ${RPM_BUILD_ROOT}%{_prefix}/bin/gcj-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/gcjh ${RPM_BUILD_ROOT}%{_prefix}/bin/gcjh-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/gcov ${RPM_BUILD_ROOT}%{_prefix}/bin/gcov-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/jcf-dump ${RPM_BUILD_ROOT}%{_prefix}/bin/jcf-dump-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/jv-scan ${RPM_BUILD_ROOT}%{_prefix}/bin/jv-scan-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/m68k-atari-mint-gcc ${RPM_BUILD_ROOT}%{_prefix}/bin/m68k-atari-mint-gcc-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/protoize ${RPM_BUILD_ROOT}%{_prefix}/bin/protoize-2.95.3
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/unprotoize ${RPM_BUILD_ROOT}%{_prefix}/bin/unprotoize-2.95.3

#(cd ${RPM_BUILD_ROOT}%{_prefix}/bin;
#	cp g++ g++.%{version}
#	cp gcc gcc.%{version}
#)

cd ..
cp %{SOURCE1} gcc/


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%pre
mkdir -p %{_prefix}/lib/gcc-lib/%{TARGET} 2>/dev/null ||:
mkdir -p %{_prefix}/lib/m68020-60/mshort 2>/dev/null ||:
mkdir -p %{_prefix}/lib/mshort 2>/dev/null ||:
mkdir -p %{_prefix}/%{TARGET}/include 2>/dev/null ||:

%post
/sbin/install-info \
	--info-dir=%{_prefix}/info %{_prefix}/info/cpp.info.gz
/sbin/install-info \
        --info-dir=%{_prefix}/info %{_prefix}/info/gcc.info.gz

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete \
	--info-dir=%{_prefix}/info %{_prefix}/info/cpp.info.gz
   /sbin/install-info --delete \
        --info-dir=%{_prefix}/info %{_prefix}/info/gcc.info.gz
fi

%post g77
/sbin/install-info \
	--info-dir=%{_prefix}/info %{_prefix}/info/g77.info.gz

%preun g77
if [ $1 = 0 ]; then
   /sbin/install-info --delete \
	--info-dir=%{_prefix}/info %{_prefix}/info/g77.info.gz
fi

%post chill
/sbin/install-info \
	--info-dir=%{_prefix}/info %{_prefix}/info/chill.info.gz

%preun chill
if [ $1 = 0 ]; then
   /sbin/install-info --delete \
	--info-dir=%{_prefix}/info %{_prefix}/info/chill.info.gz
fi


%files
%defattr(-,root,root)
%doc gcc/README* gcc/*ChangeLog* gcc/PROBLEMS gcc/NEWS gcc/SERVICE gcc/BUGS gcc/LANGUAGES
%{_prefix}/bin/gcc-2.95.3
#%{_prefix}/bin/gcc.%{version}
%{_prefix}/bin/cc-2.95.3
%{_prefix}/bin/cpp-2.95.3
%{_prefix}/bin/protoize-2.95.3
%{_prefix}/bin/unprotoize-2.95.3
%{_prefix}/bin/gcov-2.95.3
%{_prefix}/bin/%{TARGET}-gcc-2.95.3
%{_prefix}/man/man1/cccp-2.95.3.1.gz
%{_prefix}/man/man1/cpp-2.95.3.1.gz
%{_prefix}/man/man1/gcc-2.95.3.1.gz
%{_prefix}/info/cpp*
%{_prefix}/info/gcc*
%dir %{_prefix}/lib/gcc-lib/%{TARGET}/%{version}
%dir %{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include
%dir %{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/m68020-60
%dir %{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/m68020-60/mshort
%dir %{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/mshort
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/cc1
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/collect2
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/cpp0
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/float.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/iso646.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/limits.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/proto.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/stdarg.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/stdbool.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/stddef.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/syslimits.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/varargs.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/libgcc.a
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/m68020-60/libgcc.a
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/m68020-60/mshort/libgcc.a
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/mshort/libgcc.a
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/SYSCALLS.c.X
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/specs

%files c++
%defattr(-,root,root)
%doc gcc/cp/NEWS gcc/cp/ChangeLog*
%{_prefix}/bin/g++-2.95.3
#%{_prefix}/bin/g++.%{version}
%{_prefix}/bin/c++-2.95.3
%{_prefix}/man/man1/g++-2.95.3.1.gz
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/cc1plus
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/exception
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/new
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/new.h
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/typeinfo
%{_prefix}/include/g++-3
%{_prefix}/lib/libstdc++.a.%{STDC_VERSION}
%{_prefix}/lib/m68020-60/libstdc++.a.%{STDC_VERSION}
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/libstdc++.a
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/m68020-60/libstdc++.a
%{_prefix}/%{TARGET}/include/_G_config.h

%files objc
%defattr(-,root,root)
%doc gcc/objc/README libobjc/THREADS* libobjc/ChangeLog
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/cc1obj
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/libobjc.a
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/objc

%files g77
%defattr(-,root,root)
%doc gcc/f/README gcc/ChangeLog*
%{_prefix}/bin/g77-2.95.3
%{_prefix}/bin/f77-2.95.3
%{_prefix}/man/man1/g77-2.95.3.1.gz
%{_prefix}/info/g77*
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/f771
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/libg2c.a
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/m68020-60/libg2c.a
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/include/g2c.h

%files chill
%defattr(-,root,root)
%doc gcc/ch/README gcc/ch/chill.brochure gcc/ChangeLog*
%{_prefix}/bin/chill-2.95.3
%{_prefix}/info/chill*
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/cc1chill
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/chill*.o
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/libchill.a
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/m68020-60/chill*.o
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/m68020-60/libchill.a

%files java
%defattr(-,root,root)
%doc gcc/java/ChangeLog*
%{_prefix}/bin/gcj-2.95.3
%{_prefix}/bin/gcjh-2.95.3
%{_prefix}/bin/jcf-dump-2.95.3
%{_prefix}/bin/jv-scan-2.95.3
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/jc1
%{_prefix}/lib/gcc-lib/%{TARGET}/%{version}/jvgenmain


%changelog
* Tue Jun 15 2010 Keith Scroggins <kws@radix.net>
- Compiled against latest MiNTLib and renamed package to gcc2 to become the
- legacy compiler for MiNT

* Thu Feb 27 2003 Frank Naumann <fnaumann@freemint.de>
- fixed bug in -pg option for the mint port

* Sat Mar 17 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.95.3

* Sat Mar 03 2001 Frank Naumann <fnaumann@freemint.de>
- rebuild against MiNTLib 0.56

* Sat Feb 29 2000 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
