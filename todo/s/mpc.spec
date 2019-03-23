Version: 	0.8.2
Release: 	1
Summary: 	C Library for Multiple Precision Complex Arithmetic
Name: 		mpc
Source0: 	http://www.multiprecision.org/mpc/download/mpc-%{version}.tar.gz
License: 	LGPLv2+
Group: 		System Environment/Libraries
URL: 		http://www.multiprecision.org/
Packager: 	Keith Scroggins <kws@radix.net>
Vendor: 	Sparemint
BuildRoot:  	/var/tmp/%{name}-%{version}-root
Requires:	gmp >= 4.2.2 mpfr >= 2.4.2 mintlib-devel >= 0.58
BuildRequires:	gmp mpfr mintlib-devel

%description
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as MPFR.

%prep
%setup -q
%build 
%define CONFIG_FLAGS --prefix=/usr 
./configure %{CONFIG_FLAGS}
make
#make check - all tests pass!

%install
rm -rf $RPM_BUILD_ROOT
make install MANDIR=/usr/share/man DESTDIR="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING.LIB INSTALL NEWS README TODO
%attr(0644,root,root) /usr/lib/lib*.a
%attr(0644,root,root) /usr/include/*
%attr(0644,root,root) /usr/share/info/mpc*

%changelog
* Fri May 28 2010 Keith Scroggins <kws@radix.net>
- Initial build of MPC RPM
