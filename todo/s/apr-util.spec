Summary		: Apache Portable Runtime Utility library
Name		: apr-util
Version		: 0.9.15
Release		: 1
License		: Apache Software License
Group		: System Environment/Libraries

Packager	: Keith Scroggins <kws@radix.net>
Vendor		: Sparemint
URL		: http://apr.apache.org/

Prefix		: %{_prefix}
Docdir		: %{_prefix}/doc
BuildRoot	: %{_tmppath}/%{name}-root

Source0: %{name}-%{version}.tar.gz

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

This package also provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.

%prep
%setup -q

%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} --with-apr=%{_prefix} --with-berkeley-db=/usr

make 

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE
%{_bindir}/apu-config
%{_libdir}/libaprutil-0.*a
%{_includedir}/apr-0/*.h
#%doc --parents html

%changelog
* Tue Mar 10 2009 Keith Scroggins <kws@radix.net>
- Updated to latest version

* Mon Jan 07 2008 Keith Scroggins <kws@radix.net>
- Initial build for MiNT
