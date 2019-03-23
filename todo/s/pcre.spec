%define name pcre
%define version 3.4
%define release 2

Summary: PCRE (Perl-compatible regular expression library)
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
Copyright: see COPYING
BuildRoot: /var/tmp/%{name}-buildroot
Group: System Environment/Libraries
Vendor: Sparemint
Packager: Patrice Mandin <pmandin@caramail.com>
Prefix: %{_prefix}
Provides: libpcre

%description
PCRE is a library of functions to support regular expressions whose syntax
and semantics are as close as possible to those of the Perl 5 language.

%package devel
Summary: Libraries, includes and more to develop PCRE applications.
Group: Development/Libraries

%description devel
PCRE is a library of functions to support regular expressions whose syntax
and semantics are as close as possible to those of the Perl 5 language.

This is the libraries, include files and other resources you can use
to develop PCRE applications.

%prep
rm -rf ${RPM_BUILD_ROOT}

%setup -q
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
 --prefix=%prefix \
 --mandir=%_mandir

%build
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
gzip $RPM_BUILD_ROOT/%{_mandir}/*/*.?

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(-,root,root)
%doc COPYING README NEWS ChangeLog AUTHORS
%doc doc/*.html doc/*.txt doc/Tech.Notes
%doc %{_mandir}/man1/*
%doc %{_mandir}/man3/*
%{prefix}/bin/pcre-config
%{prefix}/bin/pcregrep
%{prefix}/include/pcre.h
%{prefix}/include/pcreposix.h
%{prefix}/lib/libpcre.la
%{prefix}/lib/libpcre.a
%{prefix}/lib/libpcreposix.la
%{prefix}/lib/libpcreposix.a

%changelog
* Sat Sep 07 2002 Patrice Mandin <pmandin@caramail.com>
- Created spec file for Sparemint


