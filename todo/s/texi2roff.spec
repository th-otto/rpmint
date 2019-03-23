Summary: Texinfo to nroff/troff translator
Name: texi2roff
Version: 2.0
Release: 1
Group: Applications/Text
License: distributable
Source: ftp://ftp.funet.fi/usr/src/redhat/texi2roff-2.0.tar.gz
Patch0: texi2roff.patch
Buildroot: /var/tmp/%{name}-root
Vendor: Sparemint
Packager: Marc-Anton Kehr <m.kehr@ndh.net>
Summary(de): Texinfo nach nroff/troff Uebersetzer

%description
Translates Texinfo files to nroff/troffi

%prep
%setup -q
%patch0 -p1

%build
make "CFLAGS=$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
install -s -m755 texi2roff $RPM_BUILD_ROOT/usr/bin
install -m755 texi2index $RPM_BUILD_ROOT/usr/bin
install -m644 texi2roff.1 $RPM_BUILD_ROOT/usr/man/man1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/texi2roff.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/texi2roff
/usr/bin/texi2index
/usr/man/man1/texi2roff.1.gz

%changelog
* Wed Oct 21 1999 Marc-Anton Kehr <m.kehr@ndh.net>
- first release
