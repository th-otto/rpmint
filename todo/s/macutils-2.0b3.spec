Summary: Utilities for manipulating Macintosh file formats.
Name: macutils
Version: 2.0b3
Release: 2
Copyright: distributable
Group: Applications/System
Source: ftp://sunsite.unc.edu/pub/Linux/utils/compress/macutils.tar.gz
Patch: macutils-misc.patch
Patch1: macutils-mint.patch
BuildRoot: /var/tmp/%{name}-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Summary(de): Utilities zum Bearbeiten von Macintosh-Dateiformaten.

%description
The macutils package includes a set of utilities for manipulating
files that are commonly used by Macintosh machines.  Macutils includes
utilities like binhex, hexbin, macunpack, etc.

Install macutils if you need to manipulate files that are commonly used
by Macintosh machines.

%description -l de
Das Paket macutils beinhaltet eine Gruppe von Hilfen zur Handhabung
von Dateien, die auf Macintosh-Computern gebräuchlich sind. Macutils 
beinhaltet unter anderem binhex, hexbin, macunpack.

Installieren Sie macutils, falls Sie Macintosh-Dateien bearbeiten müssen.

%prep
%setup -q -n macutils
%patch -p1
%patch1 -p1 -b .mint
%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man1}

make BINDIR=$RPM_BUILD_ROOT/usr/bin install
strip $RPM_BUILD_ROOT/usr/bin/binhex
strip $RPM_BUILD_ROOT/usr/bin/hexbin
strip $RPM_BUILD_ROOT/usr/bin/macsave
strip $RPM_BUILD_ROOT/usr/bin/macstream
strip $RPM_BUILD_ROOT/usr/bin/macunpack
strip $RPM_BUILD_ROOT/usr/bin/frommac
strip $RPM_BUILD_ROOT/usr/bin/tomac

cp man/* $RPM_BUILD_ROOT/usr/man/man1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/binhex.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/hexbin.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/macsave.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/macstream.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/macunpack.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/macutil.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/frommac.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/tomac.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
/usr/bin/macunpack
/usr/bin/hexbin
/usr/bin/macsave
/usr/bin/macstream
/usr/bin/binhex
/usr/bin/tomac
/usr/bin/frommac
/usr/man/man1/binhex.1.gz
/usr/man/man1/frommac.1.gz
/usr/man/man1/hexbin.1.gz
/usr/man/man1/macsave.1.gz
/usr/man/man1/macstream.1.gz
/usr/man/man1/macunpack.1.gz
/usr/man/man1/macutil.1.gz
/usr/man/man1/tomac.1.gz

%changelog
* Sun Sep 12 1999 Edgar Aichinger <eaiching@t0.or.at>
- improved german description (style, iso-conversion)
- compressed manpages, stripped binaries

* Sat Sep 11 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT 
- added Vendor, Packager, german Summary
