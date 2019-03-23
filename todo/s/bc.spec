Summary: GNU's bc (a numeric processing language) and dc (a calculator).
Summary(de): GNUs bc (eine Zahlenverarbeitungssprache) und dc (ein Rechner).
Name: bc
Version: 1.05a
Release: 2
Vendor: Sparemint
Packager: John Blakeley (johnnie@ligotage.demon.co.uk)
Copyright: GPL
Group: Applications/Engineering
Source: ftp://ftp.gnu.org/pug/gnu/bc-%{version}.tar.bz2
Prereq: /sbin/install-info grep
Buildroot: /var/tmp/%{name}-root

%description
The bc package includes bc and dc.  Bc is an arbitrary precision numeric
processing arithmetic language.  Dc is an interactive arbitrary precision
stack based calculator, which can be used as a text mode calculator.

Install the bc package if you need its number handling capabilities or
if you would like to use its text mode calculator.

%description -l de
Das bc-Paket enthält bc und dc. Bc ist eine Zahlenverarbeitungssprache mit
beliebiger Genauigkeit. Dc ist ein interaktiver, stapelbasierter Rechner mit
beliebiger Genauigkeit, der im Textmodus benutzt werden kann.

Installieren Sie bc, wenn Sie seine Zahlenverarbeitungsfähigkeiten brauchen,
oder wenn Sie einen Textmodus-Rechner haben wollen.

%prep
%setup -q -n bc-1.05

%configure --with-readline

%build
# CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --with-readline
make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT/usr mandir=$RPM_BUILD_ROOT/usr/share/man install
gzip -9f $RPM_BUILD_ROOT/usr/info/dc.info
gzip -9f $RPM_BUILD_ROOT/usr/share/man/man1/*

strip $RPM_BUILD_ROOT/usr/bin/dc $RPM_BUILD_ROOT/usr/bin/bc

%clean
rm -rf $RPM_BUILD_ROOT

%post
# previous versions of bc put an improper entry into /usr/info/dir -- remove
# it
if grep 'dc: (bc)' /usr/info/dir > /dev/null; then
    grep -v 'The GNU RPN calculator' < /usr/info/dir > /usr/info/dir.$$
    mv -f /usr/info/dir.$$ /usr/info/dir
fi

/sbin/install-info /usr/info/dc.info.gz /usr/info/dir --entry="* dc: (dc).                      The GNU RPN calculator."

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete /usr/info/dc.info.gz /usr/info/dir --entry="* dc: (dc).                      The GNU RPN calculator."
fi

%files
%defattr(-,root,root)
/usr/bin/dc
/usr/bin/bc
/usr/share/man/man1/bc.1.gz
/usr/share/man/man1/dc.1.gz
/usr/info/dc.info.gz

%changelog
* Mon Oct 18 1999 John Blakeley <johnnie@ligotage.demon.co.uk>
- Second release for SpareMiNT
- corrected man-page locations - thanks Guido ;-)

* Fri Oct 15 1999 John Blakeley <johnnie@ligotage.demon.co.uk>
- First SpareMiNT adaptations
- gzip man/info pages
