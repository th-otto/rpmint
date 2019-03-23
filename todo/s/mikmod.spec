# libmikmod rpm specification file
%define version	3.1.5
%define release	4

Summary:	MikMod module player
Summary(de):	MikMod Modul Player
Summary(fr):	Lecteur de modules MikMod
Name:		mikmod
Version:	%version
Release:	%release
Copyright:	LGPL
Group:		Applications/Sound
URL:		http://www.multimania.com/miodrag/mikmod/index.html
PreReq:		/sbin/install-info
Prefix:		/usr
Buildroot:	/tmp/build/mikmod-%{PACKAGE_VERSION}
Packager:	Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor:		Sparemint

Source0:	http://www.multimania.com/miodrag/mikmod/mikmod-%{PACKAGE_VERSION}.tar.gz
Patch0:		http://www.multimania.com/miodrag/mikmod/patch-mikmod-3.1.5-a

%description
One of the best and most well known module players, based on libmikmod.
The player uses ncurses for console output and supports transparent loading
from a variety of archive formats, as well as playlists.

%description -l de
Einer der besten und bekanntesten Modul Player. Basiert auf der libmikmod
Library.. Der Player benutzt ncurses für Konsolen Ausgaben und unterstützt
das transparente Laden von verschiedenen Archivformaten und Playlisten.

%description -l fr
L'un des meilleurs et plus populaires lecteurs de modules, basé sur libmikmod.
Le lecteur dispose d'une interface ncurses et supporte le chargement à partir
d'un large choix de formats d'archives, ainsi que des 'playlists'.

Requires:	libmikmod
Requires:	ncurses

################################################################################

%prep
%setup
%patch0 -p1 -b .orig

%build
./configure --prefix=%prefix
make

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{prefix} install
gzip -9nf $RPM_BUILD_ROOT%{prefix}/man/man1/*

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL NEWS README
%{prefix}/bin/*
%{prefix}/man/man1/*

%changelog
* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
- added %description de and Summary(de)
