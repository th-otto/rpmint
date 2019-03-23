Summary       : Library for UTF-8 locale support
Name          : libutf8
Version       : 0.8
Release       : 1
Copyright     : LGPL
Group         : System Environment/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://clisp.cons.org/~haible/packages-libutf8.html

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.ilog.fr/pub/Users/haible/utf8/libutf8-%{version}.tar.gz


%description
This library provides UTF-8 locale support, for use on systems which don't
have UTF-8 locales, or whose UTF-8 locales are unreasonably slow.

It provides support for
  - the wchar_t and wint_t types,
  - the mbs/wcs functions typically found in <stdlib.h>,
  - the wide string functions typically found in <wchar.h>,
  - the wide character classification functions typically found in <wctype.h>,
  - some of the wide character I/O functions typically found in <wchar.h>,
  - the setlocale function typically found in <locale.h>.
All this according to the ISO/ANSI C specifications, and with support for
old 8-bit locales and Unicode UTF-8 locales.

libutf8 is for you if your application supports 8-bit and multibytes locales
like chinese or japanese, and you wish to add UTF-8 locale support but the
corresponding support lacks from your system.

libutf8 is for you also if your application supports only 8-bit locales, and
you wish to add UTF-8 locale support. Because libutf8 implements an ISO/ANSI C
compatible set of types and functions, the support for libutf8 you add will
also automatically work (without libutf8) with other multibytes locales,
as far as supported by the system.

libutf8 concentrates on 8-bit and UTF-8 encodings and therefore does not
suffer from the complexity needed to support other multibytes locales.

%package devel
Summary       : Library for UTF-8 locale support
Group         : Development/Libraries

%description devel
This library provides UTF-8 locale support, for use on systems which don't
have UTF-8 locales, or whose UTF-8 locales are unreasonably slow.

It provides support for
  - the wchar_t and wint_t types,
  - the mbs/wcs functions typically found in <stdlib.h>,
  - the wide string functions typically found in <wchar.h>,
  - the wide character classification functions typically found in <wctype.h>,
  - some of the wide character I/O functions typically found in <wchar.h>,
  - the setlocale function typically found in <locale.h>.
All this according to the ISO/ANSI C specifications, and with support for
old 8-bit locales and Unicode UTF-8 locales.

libutf8 is for you if your application supports 8-bit and multibytes locales
like chinese or japanese, and you wish to add UTF-8 locale support but the
corresponding support lacks from your system.

libutf8 is for you also if your application supports only 8-bit locales, and
you wish to add UTF-8 locale support. Because libutf8 implements an ISO/ANSI C
compatible set of types and functions, the support for libutf8 you add will
also automatically work (without libutf8) with other multibytes locales,
as far as supported by the system.

libutf8 concentrates on 8-bit and UTF-8 encodings and therefore does not
suffer from the complexity needed to support other multibytes locales.

Header files and static library for libutf8.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}/usr
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%doc COPYING.LIB NEWS PORTS README
%doc extras
%{_prefix}/include/*.h
%{_prefix}/include/utf8
%{_prefix}/lib/lib*a
%{_prefix}/share/man/*/*


%changelog
* Mon Jul 09 2001 Frank Naumann <fnaumann@freemint.de>
- initial revision for SpareMiNT
