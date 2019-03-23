Summary       : Apache Portable Runtime library
Name          : apr
Version       : 0.9.17
Release       : 1
License       : Apache Software License
Group         : System Environment/Libraries

Packager      : Keith Scroggins <kws@radix.net>
Vendor        : Sparemint
URL           : http://apr.apache.org/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0       : %{name}-%{version}.tar.gz
Patch0        : apr-0.9.12-mint.patch

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.

This package provides the support files which can be used to 
build applications using the APR library.  The mission of the
Apache Portable Runtime (APR) is to provide a free library of 
C data structures and routines.

%prep
%setup -q
%patch0 -p1 -b .mint

%build
CFLAGS="${RPM_OPT_FLAGS}" \
 ./configure \
       --enable-static --disable-shared --disable-dso \
       --disable-threads --disable-ipv6 --prefix=%{_prefix}

make 

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

make install \
	DESTDIR="${RPM_BUILD_ROOT}"

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE
%doc docs/APRDesign.html docs/canonical_filenames.html
%doc docs/incomplete_types docs/non_apr_programs
/usr/build/*
%{_bindir}/apr*config
%{_libdir}/libapr-0.*a
%dir %{_includedir}/apr-0
%{_includedir}/apr-0/*.h

%changelog
* Tue Mar 10 2009 Keith Scroggins <kws@radix.net>
- Updated to latest version

* Mon Jan 07 2008 Keith Scroggins <kws@radix.net>
- Initial build for MiNT

