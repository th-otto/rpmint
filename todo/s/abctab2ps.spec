Summary         : abctab2ps: a tablature typesetting program for ABC music files. 
Name            : abctab2ps
Version         : 1.8.8
Release         : 1
License         : GPL
Group           : Applications/Multimedia

Packager        : Martin Tarenskeen <m.tarenskeen@zonnet.nl>
Vendor          : Sparemint
URL             : http://www.lautengesellschaft.de/cdmm

Prefix          : %{_prefix}
BuildRoot       : %{_tmppath}/%{name}-%{version}-buildroot

Source          : %{url}/%{name}-%{version}.tar.gz
Patch           : abctab2ps-%{version}.mint.patch

%description
A music and tablature typesetting program based on
Chris Walshaw's abc music language. abctab2ps converts
abc files directly into postscript without the need
of additional software.
In addition to the abc standard which only supports
music, abctab2ps supports lute and guitar tablature.
This version was compiled for -m68020-60: A 68881/2
compatible (co-)processor is required if you want to
use it.

%prep
%setup -q
%patch -p1

%build
cd src
make CC="gcc -m68020-60" OSVARIANT="MINT" CFLAGS="$RPM_OPT_FLAGS -g -Wall" LDFLAGS="-lstdc++"
cd ..

%install
cd src
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -d ${RPM_BUILD_ROOT}%{_mandir}
install -d ${RPM_BUILD_ROOT}%{_datadir}
make install PREFIX=$RPM_BUILD_ROOT%{_prefix}
install -m 644 ../doc/userguide/userguide.ps ${RPM_BUILD_ROOT}%{_prefix}/share/doc/abctab2ps/

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_prefix}/share/doc/abctab2ps/*
%{_prefix}/man/man1/*
%{_bindir}/*
%{_datadir}/abctab2ps

%changelog
* Wed Sep 09 2009 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 1.8.8

* Wed Dec 19 2007 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 1.8.3
- install userguide.ps documentation

* Sat Aug 25 2007 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 1.8.2

* Wed Aug 16 2006 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 1.7.0 

* Fri Apr 21 2006 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 1.6.8

* Sun Mar 19 2006 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 1.6.7
- minor changes in specfile

* Fri Nov 18 2005 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 1.6.6

* Thu Aug 24 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 1.6.3
- gzipped manpage
- small changes in specfile   

* Mon Apr 12 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- update to 1.6.2

* Fri Jan 23 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- update to 1.6.0
- small changes in Makefile and Specfile

* Tue Sep 30 2003 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- Correction in Makefile for MiNT. 

* Wed Jul 24 2003 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- update to 1.5.3
- use %patch in specfile, keeping original sources intact.

* Sun May 11 2003 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- Initial release for Sparemint
