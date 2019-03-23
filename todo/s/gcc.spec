%define is_sparemint %(test -e /etc/sparemint-release && echo 1 || echo 0)

Summary		: C & C++ Compilers
Name		: gcc
Version		: 4.5.2
Release		: 1
License		: GPL
Group		: Development/Languages
Packager	: Keith Scroggins <kws@radix.net>
Vendor		: Sparemint
URL		: http://gcc.gnu.org/

%if %is_sparemint
Requires	: binutils mintlib-devel
BuildRequires	: gmp >= 4.2.4 mpfr >= 2.4.2 mpc >= 0.8.2
Prereq		: /sbin/install-info
%endif

Prefix		: %{_prefix}
Docdir		: %{_prefix}/doc
BuildRoot	: %{_tmppath}/%{name}-root

Source0		: gcc-core-%{version}.tar.bz2
Source1		: gcc-g++-%{version}.tar.bz2
Patch0		: gcc-4.5.2-mint-20110102.patch
Patch1		: gcc-4.5.0-limits-include.patch

%define TARGET m68k-atari-mint
%undefine __os_install_post

%description
The gcc package contains the GNU Compiler Collection: cc and gcc. You'll need
this package in order to compile C code.

%package c++
Summary       : C++ support for gcc
Group         : Development/Languages
Requires      : gcc = %{version}

%description c++
This package adds C++ support to the GNU C compiler. It includes support
for most of the current C++ specification, including templates and
exception handling. It does include the static standard C++
library and C++ header files.

%prep
%setup -q -b 1
%patch0 -p1 -b .mint
%patch1 -p1 -b .include

%build
rm -rf build-%{TARGET}
mkdir build-%{TARGET}
cd build-%{TARGET}
../configure \
	--enable-languages="c,c++" \
	--prefix=%{_prefix} \
	--disable-nls \
	--disable-libstdcxx-pch \
	--target=%{TARGET} \
%if %is_sparemint
	--disable-bootstrap
%else
	--host=%{TARGET}
%endif

make CFLAGS="-O2 -fomit-frame-pointer" LIBCFLAGS="-g -O2" \
	LIBCXXFLAGS="-g -O2 -fno-implicit-templates"

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd build-%{TARGET}
make prefix=${RPM_BUILD_ROOT}%{_prefix} install

%if %is_sparemint
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --size=960k ${RPM_BUILD_ROOT}%{_prefix}/bin/gcc
stack --size=960k ${RPM_BUILD_ROOT}%{_prefix}/bin/g++
%else
%{TARGET}-strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
%{TARGET}-stack --size=960k ${RPM_BUILD_ROOT}%{_prefix}/bin/gcc
%{TARGET}-stack --size=960k ${RPM_BUILD_ROOT}%{_prefix}/bin/g++
%endif

FULLVER=`${RPM_BUILD_ROOT}%{_prefix}/bin/%{TARGET}-gcc --version | cut -d' ' -f1`
FULLPATH=$(dirname ${RPM_BUILD_ROOT}%{_prefix}/libexec/gcc/%{TARGET}/%{version}/cc1)

%if %is_sparemint
strip ${FULLPATH}/cc1
stack --size=960k ${FULLPATH}/cc1
strip ${FULLPATH}/collect2
stack --size=128k ${FULLPATH}/collect2
strip ${FULLPATH}/cc1plus
stack --size=960k ${FULLPATH}/cc1plus
%else
%{TARGET}-strip ${FULLPATH}/cc1
%{TARGET}-stack --size=960k ${FULLPATH}/cc1
%{TARGET}-strip ${FULLPATH}/collect2
%{TARGET}-stack --size=128k ${FULLPATH}/collect2
%{TARGET}-strip ${FULLPATH}/cc1plus
%{TARGET}-stack --size=960k ${FULLPATH}/cc1plus
%endif

# fix some things
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/info/dir
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/info/*.info*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*

#Some cleanup for new RPM versions
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/lib/gcc/%{TARGET}/%{version}/include-fixed
mkdir ${RPM_BUILD_ROOT}%{_prefix}/lib/gcc/%{TARGET}/%{version}/include-fixed
cp ../limits.h ${RPM_BUILD_ROOT}%{_prefix}/lib/gcc/%{TARGET}/%{version}/include-fixed/
cp ../syslimits.h ${RPM_BUILD_ROOT}%{_prefix}/lib/gcc/%{TARGET}/%{version}/include-fixed/
rm -f ${RPM_BUILD_ROOT}%{_prefix}/lib/libiberty.a
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man7

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%pre
#mkdir -p %{_prefix}/lib/gcc-lib/%{TARGET} 2>/dev/null ||:
mkdir -p %{_prefix}/lib/m5475/mshort 2>/dev/null ||:
mkdir -p %{_prefix}/lib/m68020-60/mshort 2>/dev/null ||:
mkdir -p %{_prefix}/lib/mshort 2>/dev/null ||:
mkdir -p %{_prefix}/%{TARGET}/include 2>/dev/null ||:

%files
%defattr(-,root,root)
#%doc gcc/README* gcc/*ChangeLog* gcc/PROBLEMS gcc/NEWS gcc/SERVICE gcc/BUGS gcc/LANGUAGES
%{_prefix}/bin/gcc
%{_prefix}/bin/m68k-atari-mint-gcc-%{version}
%{_prefix}/bin/cpp
%{_prefix}/bin/gccbug
%{_prefix}/bin/gcov
%{_prefix}/bin/%{TARGET}-gcc
%{_prefix}/share/man/man1/cpp.1.gz
%{_prefix}/share/man/man1/gcc.1.gz
%{_prefix}/share/man/man1/gcov.1.gz
%{_prefix}/share/info/cpp*
%{_prefix}/share/info/gcc*
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}/include
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}/include-fixed
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}/m5475
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}/m5475/mshort
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}/m68020-60
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}/m68020-60/mshort
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}/mshort
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}/install-tools
%dir %{_prefix}/lib/gcc/%{TARGET}/%{version}/install-tools/include
%{_prefix}/libexec/gcc/%{TARGET}/%{version}/cc1
%{_prefix}/libexec/gcc/%{TARGET}/%{version}/collect2
%{_prefix}/libexec/gcc/%{TARGET}/%{version}/lto-wrapper
%{_prefix}/libexec/gcc/%{TARGET}/%{version}/install-tools/*
%{_prefix}/lib/gcc/%{TARGET}/%{version}/include/*.h
%{_prefix}/lib/gcc/%{TARGET}/%{version}/include/ssp/*.h
%{_prefix}/lib/gcc/%{TARGET}/%{version}/include-fixed/*.h
%{_prefix}/lib/gcc/%{TARGET}/%{version}/install-tools/*
%{_prefix}/lib/gcc/%{TARGET}/%{version}/libgcc.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/libgcov.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/m5475/libgcc.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/m5475/libgcov.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/m5475/mshort/libgcc.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/m5475/mshort/libgcov.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/m68020-60/libgcc.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/m68020-60/libgcov.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/m68020-60/mshort/libgcc.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/m68020-60/mshort/libgcov.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/mshort/libgcc.a
%{_prefix}/lib/gcc/%{TARGET}/%{version}/mshort/libgcov.a
%{_prefix}/lib/libssp.a
%{_prefix}/lib/libssp.la
%{_prefix}/lib/libssp_nonshared.a
%{_prefix}/lib/libssp_nonshared.la
%{_prefix}/lib/libmudflap.a
%{_prefix}/lib/libmudflap.la
%{_prefix}/lib/m5475/libssp.a
%{_prefix}/lib/m5475/libssp.la
%{_prefix}/lib/m5475/libssp_nonshared.a
%{_prefix}/lib/m5475/libssp_nonshared.la
%{_prefix}/lib/m5475/libmudflap.a
%{_prefix}/lib/m5475/libmudflap.la
%{_prefix}/lib/m68020-60/libssp.a
%{_prefix}/lib/m68020-60/libssp.la
%{_prefix}/lib/m68020-60/libssp_nonshared.a
%{_prefix}/lib/m68020-60/libssp_nonshared.la
%{_prefix}/lib/m68020-60/libmudflap.a
%{_prefix}/lib/m68020-60/libmudflap.la
#%{_prefix}/lib/m68020-60/mshort/libssp.a
#%{_prefix}/lib/m68020-60/mshort/libssp_nonshared.a
#%{_prefix}/lib/mshort/libssp.a
#%{_prefix}/lib/mshort/libssp_nonshared.a

%files c++
%defattr(-,root,root)
#%doc gcc/cp/NEWS gcc/cp/ChangeLog*
%{_prefix}/bin/g++
%{_prefix}/bin/m68k-atari-mint-g++
%{_prefix}/bin/c++
%{_prefix}/bin/m68k-atari-mint-c++
%{_prefix}/share/man/man1/g++.1.gz
%{_prefix}/libexec/gcc/%{TARGET}/%{version}/cc1plus
%{_prefix}/include/c++/%{version}/*
#%{_prefix}/include/c++/%{version}/backward/*
#%{_prefix}/include/c++/%{version}/bits/*
#%{_prefix}/include/c++/%{version}/debug/*
#%{_prefix}/include/c++/%{version}/decimal/*
#%{_prefix}/include/c++/%{version}/ext/*
#%{_prefix}/include/c++/%{version}/m68k-atari-mint/bits/*
#%{_prefix}/include/c++/%{version}/m68k-atari-mint/m5475/bits/*
#%{_prefix}/include/c++/%{version}/m68k-atari-mint/m5475/mshort/bits/*
#%{_prefix}/include/c++/%{version}/m68k-atari-mint/m68020-60/bits/*
#%{_prefix}/include/c++/%{version}/m68k-atari-mint/m68020-60/mshort/bits/*
#%{_prefix}/include/c++/%{version}/m68k-atari-mint/mshort/bits/*
#%{_prefix}/include/c++/%{version}/profile/*
#%{_prefix}/include/c++/%{version}/tr1/*
#%{_prefix}/include/c++/%{version}/tr1_impl/*
%{_prefix}/lib/libstdc++.a
%{_prefix}/lib/libstdc++.a-gdb.py
%{_prefix}/lib/libstdc++.la
%{_prefix}/lib/m5475/libstdc++.a
%{_prefix}/lib/m5475/libstdc++.a-gdb.py
%{_prefix}/lib/m5475/libstdc++.la
%{_prefix}/lib/m68020-60/libstdc++.a
%{_prefix}/lib/m68020-60/libstdc++.a-gdb.py
%{_prefix}/lib/m68020-60/libstdc++.la
#%{_prefix}/lib/m68020-60/mshort/libstdc++.a
#%{_prefix}/lib/mshort/libstdc++.a
%{_prefix}/lib/libsupc++.a
%{_prefix}/lib/libsupc++.la
%{_prefix}/lib/m5475/libsupc++.a
%{_prefix}/lib/m5475/libsupc++.la
%{_prefix}/lib/m68020-60/libsupc++.a
%{_prefix}/lib/m68020-60/libsupc++.la
#%{_prefix}/lib/m68020-60/mshort/libsupc++.a
#%{_prefix}/lib/mshort/libsupc++.a
%{_prefix}/share/gcc-%{version}/python/libstdcxx/__init__.py
%{_prefix}/share/gcc-%{version}/python/libstdcxx/v6/__init__.py
%{_prefix}/share/gcc-%{version}/python/libstdcxx/v6/printers.py


%changelog
* Mon Jan 03 2011 Keith Scroggins <kws@radix.net>
- GCC 4.5.2 for FreeMiNT

* Thu Dec 23 2010 Keith Scroggins <kws@radix.net>
- Built with latest (2.21) Binutils

* Tue Aug 03 2010 Keith Scroggins <kws@radix.net>
- GCC 4.5.1 for FreeMiNT

* Sun May 30 2010 Keith Scroggins <kws@radix.net>
- GCC 4.5.0 for FreeMiNT

* Wed Jan 23 2008 Keith Scroggins <kws@radix.net>
- Initial native build of GCC 4.2.2 for MiNT, only the C and C++ 
- compilers, with patches from Vincent Riviere and Miro Kropacek

* Thu Feb 27 2003 Frank Naumann <fnaumann@freemint.de>
- fixed bug in -pg option for the mint port

* Sat Mar 17 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.95.3

* Sat Mar 03 2001 Frank Naumann <fnaumann@freemint.de>
- rebuild against MiNTLib 0.56

* Sat Feb 29 2000 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release

