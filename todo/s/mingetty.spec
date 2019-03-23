Summary: A compact getty program for virtual consoles only.
Name: mingetty
Version: 0.9.4
Copyright: GPL
Release: 1
Group: System Environment/Base
Source0: ftp://jurix.jura.uni-sb.de/pub/linux/source/system/daemons/mingetty-0.9.4.tar.gz
Patch0: mingetty-0.9.4-make.patch
Patch1: mingetty-0.9.4-glibc.patch
Patch2: mingetty-0.9.4-isprint.patch
Patch3: mingetty-0.9.4-wtmplock.patch
Patch4: mingetty-mint.patch
BuildRoot: /var/tmp/mingetty-root
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): Ein kompaktes Getty-Programm nur für virtuelle Konsolen.

%description
The mingetty program is a lightweight, minimalist getty program for
use only on virtual consoles.  Mingetty is not suitable for serial
lines (you should use the mgetty program instead for that purpose).

%description -l de
Das Programm Mingetty ist ein super-simples, minimalistisches 
Getty-Programm für die Benutzung auf virtuellen Konsolen. Mingetty
ist nicht geeignet für serielle Leitungen (stattdessen sollte das
Programm Mgetty benutzt werden).

%prep
%setup -q
%patch0 -p0 -b .make
%patch1 -p1 -b .glibc
%patch2 -p1 -b .isprint
%patch3 -p1 -b .wtmplock
%patch4 -p1 -b .mint

%build
make "RPM_OPTS=$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{sbin,usr/share/man/man8}

install -m 0755 -s mingetty $RPM_BUILD_ROOT/sbin/
install -m 0644 mingetty.8 $RPM_BUILD_ROOT/usr/share/man/man8/
gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man8/mingetty.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ANNOUNCE COPYING TODO
/sbin/mingetty
/usr/share/man/man8/mingetty.8.gz

%changelog
* Fri Oct 8 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- First version for Sparemint.
