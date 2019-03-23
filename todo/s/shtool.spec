Summary: GNU shtool is a compilation of several commonly used shell scripts.
Name: shtool
Version: 1.4.6
Release: 1
Source: ftp://ftp.gnu.org/gnu/shtool/%{name}-%{version}.tar.gz
Copyright: GPL
Group: Development/Tools
BuildArch: noarch
BuildRoot: /var/tmp/shtool-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Summary(de): GNU shtool ist eine Sammlung von etlichen oft benötigten Shellskripten.

%description
The GNU shtool program is a compilation of small but very stable and
portable shell scripts into a single shell tool. All ingredients
were in successful use over many years in various free software
projects. The compiled shtool program is intended to be used inside
the source tree of free software packages. There it can take over
various (usually non-portable) tasks related to the building and
installation of such packages.
It currently contains the following tools: echo, mdate, table, prop,
move, install, mkdir, mkln, mkshadow, fixperm, tarball, guessos, arx,
slo, scpp, version, path.

Install shtool if you are developing software and want to use it with your 
packages.

%description -l de
Das GNU-Programm shtool ist eine Sammlung von kleinen, aber sehr stabilen und
portablen Shellskripten in einem einzelnen Shellprogramm. Alle Bestandteile
wurden jahrelang in etlichen freien Softwareprojekten erfolgreich verwendet.
projects. Shtool sollte im Quelltextverzeichnis freier Softwarepakete
verwendet werden. Dort kann es etliche (normalerweise nicht portable)
Aufgaben übernehmen, die mit der Erzeugung und Installation solcher
Pakete verbunden sind.
Momentan beinhaltet es folgende Werkzeuge: echo, mdate, table, prop,
move, install, mkdir, mkln, mkshadow, fixperm, tarball, guessos, arx,
slo, scpp, version, path.

Installieren Sie shtool, falls Sie Software entwickeln und es in Ihren 
Paketen benützen wollen.

%prep
%setup -q
./configure --prefix=/usr

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT/usr exec_prefix=$RPM_BUILD_ROOT/usr install
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/shtool.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/shtoolize.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/shtool
/usr/bin/shtoolize
/usr/man/man1/shtool.1.gz
/usr/man/man1/shtoolize.1.gz
/usr/share/aclocal/shtool.m4
/usr/share/shtool/sh.echo
/usr/share/shtool/sh.mdate
/usr/share/shtool/sh.table
/usr/share/shtool/sh.prop
/usr/share/shtool/sh.move
/usr/share/shtool/sh.install
/usr/share/shtool/sh.mkdir
/usr/share/shtool/sh.mkln
/usr/share/shtool/sh.mkshadow
/usr/share/shtool/sh.fixperm
/usr/share/shtool/sh.tarball
/usr/share/shtool/sh.guessos
/usr/share/shtool/sh.arx
/usr/share/shtool/sh.slo
/usr/share/shtool/sh.scpp
/usr/share/shtool/sh.version
/usr/share/shtool/sh.path
%doc ChangeLog README AUTHORS THANKS INSTALL COPYING

%changelog
* Thu Oct 21 1999 Edgar Aichinger <eaiching@t0.or.at>
- first relase for Sparemint