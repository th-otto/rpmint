Summary		: Freely Distributable Maths Library
Name		: fdlibm
Version		: 5.3
Release		: 2
Group		: Development/Libraries
License		: distributable
Source		: fdlibm-CVS-06042010.tar.bz2
Buildroot	: /var/tmp/%{name}-root
Vendor		: Sparemint
Packager	: Keith Scroggins <kws@radix.net>
Conflicts	: pml

%description
Freely Distributable Maths Library

%prep
%setup -q

%build
./configure --prefix=$RPM_BUILD_ROOT%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_prefix}/include/*
%{_prefix}/lib/*.a
%{_prefix}/lib/m5475/*.a
%{_prefix}/lib/m68020-60/*.a

%changelog
* Fri Jun 04 2010 Keith Scroggins <kws@radix.net>
- Added m5475 target

* Wed Sep 22 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 5.3

* Sun Jun 04 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- first release for Sparemint.
