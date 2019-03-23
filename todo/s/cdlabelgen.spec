Name            : cdlabelgen
Summary         : Generates frontcards and traycards for inserting in CD/DVD jewel cases.
Version         : 4.1.0
Release         : 1
Source0         : http://www.aczoom.com/pub/tools/cdlabelgen-%{version}.tgz
Source1         : cdlabelgen-sparemint.tgz
URL             : http://www.aczoom.com/tools/cdinsert/
BuildRoot       : %{_tmppath}/%{name}-%{version}-buildroot
License         : BSD
Group           : Applications/Publishing
BuildArch       : noarch
Vendor          : Sparemint
Packager        : Martin Tarenskeen <m.tarenskeen@zonnet.nl>

%description
Cdlabelgen is a utility which generates frontcards and traycards (in
PostScript(TM) format) for CD/DVD jewelcases.

%prep
%setup -q
%setup -q -a 1 -n %{name}-%{version}

%build
pod2man cdlabelgen.pod > cdlabelgen.1
pod2html cdlabelgen.pod > cdlabelgen.html

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/cdlabelgen
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 755 cdlabelgen $RPM_BUILD_ROOT%{_bindir}
install -m 644 postscript/* $RPM_BUILD_ROOT%{_datadir}/cdlabelgen
install -m 644 cdlabelgen.1 $RPM_BUILD_ROOT%{_mandir}/man1
gzip $RPM_BUILD_ROOT%{_mandir}/man1/cdlabelgen.1

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc ChangeLog README INSTALL INSTALL.WEB cdinsert.pl cdlabelgen.html
%{_bindir}/cdlabelgen
%{_datadir}/cdlabelgen
%{_mandir}/*/*

%changelog
* Wed Aug 18 2010 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- update for version 4.1.0

* Wed Nov 28 2007 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- update for version 4.0.0

* Sat Aug 27 2005 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- update for version 3.6.0

* Thu Jan 20 2005 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- update for version 3.5.0
- URL "aczone" moved to "aczoom"
- added "SpareMiNT" and "Powered by FreeMiNT" eps images to distribution.
- Name of specfile changed to cdlabelgen.spec without a version number
- gzipped manpage
- other small changes in specfile

* Sun Jan 09 2005 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- first release for SpareMiNT

* Wed Jul 15 2003 Avinash Chopde <avinash@aczone.com>
- see file ChangeLog for newer changes

* Wed Aug 21 2002 Alessandro Dotti Contra <alessandro.dotti@libero.it>
- update for version 2.5.0

* Thu Mar 14 2002 Peter Bieringer <pb@bieringer.de>
- update for version 2.2.1

* Wed Feb 20 2002 Peter Bieringer <pb@bieringer.de>
- update for version 2.2.0

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- built for the distro

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jun 5 2000 Tim Powers <timp@redhat.com>
- fix man page location

* Mon May 8 2000 Tim Powers <timp@redhat.com>
- rebuilt for 7.0
* Tue Jan 4 2000 Tim Powers <timp@redhat.com>
- removed unneeded defines
- rebuilt for 6.2
* Mon Aug 23 1999 Preston Brown <pbrown@redhat.com>
- adopted for Powertools 6.1.
