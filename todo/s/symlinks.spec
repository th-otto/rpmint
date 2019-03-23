Summary: A utility which maintains a system's symbolic links.
Name: symlinks
Version: 1.2
Release: 3
Group: Applications/System
Copyright: distributable
Source: sunsite.unc.edu:/pub/Linux/utils/file/symlinks-1.2.tar.gz
Patch: symlinks.usage.patch
Buildroot: /var/tmp/symlink-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Summary(de): Ein Utility zum Warten der symbolischen Links eines Systems.

%description
The symlinks utility performs maintenance on symbolic links.  Symlinks
checks for symlink problems, including dangling symlinks which point to
nonexistent files.  Symlinks can also automatically convert absolute
symlinks to relative symlinks.

Install the symlinks package if you need a program for maintaining
symlinks on your system.

%description -l de
Das Hilfsprogramm symlinks wartet symbolische Links.  Symlinks
sucht Symlink-Probleme, einschliežlich "verwaister" Symlinks, die auf
nicht existente Dateien zeigen.  Symlinks kann auch automatisch absolute
in relative Symlinks konvertieren.

Installieren Sie das symlinks-Paket, falls Sie ein Programm zur Wartung
der Symlinks auf Ihrem System brauchen.

%prep
%setup
%patch -p1 -b .usage

%build
make

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/man/man8
install -s -m 755 -o 0 -g 0 symlinks $RPM_BUILD_ROOT/usr/bin
install -m 644 -o 0 -g 0 symlinks.8 $RPM_BUILD_ROOT/usr/man/man8
gzip -9nf $RPM_BUILD_ROOT/usr/man/man8/symlinks.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/bin/symlinks
/usr/man/man8/symlinks.8.gz

%changelog
* Wed Sep 01 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpage

* Sun Aug 29 1999 Edgar Aichinger <eaiching@t0.or.at>
- added line for -t in usage_error()
- added Vendor, Packager, german Summary/Description
- First Release for SpareMiNT
