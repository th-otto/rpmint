Summary         : abcm2ps: a program to typeset abc tunes into Postscript.
Name            : abcm2ps
Version         : 5.9.25
Release         : 1
License         : GPL
Group           : Applications/Multimedia

Packager        : Martin Tarenskeen <m.tarenskeen@zonnet.nl>
Vendor          : Sparemint
URL             : http://moinejf.free.fr

Prefix          : %{_prefix}
BuildRoot       : %{_tmppath}/%{name}-%{version}-buildroot
#BuildArch       : m68kmint
Source          : http://moinejf.free.fr/%{name}-%{version}.tar.gz


%description
abcm2ps is a package which converts music tunes from ABC format to
PostScript. Based on abc2ps version 1.2.5, it was developped originally to print
barock organ scores which have independant voices played on one or many
keyboards and a pedal-board. abcm2ps introduces many extensions to the ABC
language that make it suitable for classical music.
To print or preview scores, also install Ghostscript.
This program was compiled with -m68020-60. To use it a 68881/2 compatible 
(co)-processor is required.

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --enable-a4
make CC="gcc -m68020-60" CFLAGS="-fomit-frame-pointer" LDFLAGS=""
stack -S 128k abcm2ps

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install prefix=$RPM_BUILD_ROOT%{_prefix}
strip $RPM_BUILD_ROOT%{_bindir}/abcm2ps

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc Changes INSTALL License README *.abc *.txt *.eps
%{_bindir}/*
%{_datadir}/abcm2ps

%changelog
* Wed Nov 09 2011 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 5.9.25

* Sat May 01 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- specfile: moved strip command to %install section. 
- updated to 4.4.3

* Thu Apr 22 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 4.4.2

* Fri Jan 23 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 4.0.8
- small changes in specfile

* Mon Sep 15 2003 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- LDFLAGS=m68020-60 fixes problem with %%scale command

* Mon Sep 08 2003 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to 3.7.5

* Tue May 13 2003 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- modifications provided by Mark Lutz

* Sun May 4 2003 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- Initial release for Sparemint

* Mon Dec 31 2001 José Romildo Malaquias <romildo@iceb.ufop.br> 2.10.4-1
- New version
- More use of macros in spec file
- Use $RPM_OPT_FLAGS at compilation
- Configure with --enable-a4
- Install with "make install", instead of explicitly installing each
  file
- Move the *.fmt from the doc directory to the data directory

