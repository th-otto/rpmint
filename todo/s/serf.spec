Summary		: Serf is a HTTP client library built upon the APR library
Name		: serf
Version		: 0.3.0
Release		: 1
License		: Apache License 2.0
Group		: System/Libraries

Packager	: Keith Scroggins <kws@radix.net>
Vendor		: Sparemint
URL 		: http://code.google.com/p/serf/

Prefix		: %{_prefix}
Docdir		: %{_prefix}/doc
BuildRoot	: %{_tmppath}/%{name}-root

Source0: %{name}-%{version}.tar.bz2

%description
The serf library is a C-based HTTP client library built upon the Apache Portable Runtime (APR) library. It multiplexes connections, running the read/write communication asynchronously. Memory copies and transformations are kept to a minimum to provide high performance operation.

%prep
%setup -q

%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}
cp Makefile Makefile.tmp
grep -v spider Makefile.tmp > Makefile
make

%install
[ "${RPM_BLUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

%clean
[ "${RPM_BLUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*

%changelog
* Wed Mar 11 2009 Keith Scroggins <kws@radix.net>
- Initial build for MiNT

