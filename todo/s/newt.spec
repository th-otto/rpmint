Summary: A development library for text mode user interfaces.
Name: newt
%define version 0.50
Version: %{version}
Release: 4
Copyright: LGPL
Group: Applications/System
Source: ftp://ftp.redhat.com/pub/redhat/code/newt/newt-%{version}.tar.gz
Patch0: newt-inc.patch
Patch1: newt-mint.patch
#Requires: slang
#Provides: snack
Prefix: %{_prefix}
Packager: Guido Flohr <guido@freemint.de>
Vendor: Sparemint
Summary(de): Eine Entwicklungsbibliothek fÅr Text-Modus Benutzerschnittstellen.

%package devel
Summary: Newt windowing toolkit development files.
%ifarch m68kmint
Requires: slang
%else
Requires: slang-devel
%endif
Group: Development/Libraries
BuildRoot: /var/tmp/newtroot

%description
Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package also contains the
shared library needed by programs built with newt, as well as a
/usr/bin/dialog replacement called whiptail.  Newt is based on the
slang library.

%description devel
The newt-devel package contains the header files and libraries
necessary for developing applications which use newt.  Newt is a
development library for text mode user interfaces.  Newt is based on
the slang library.

Install newt-devel if you want to develop applications which will use
newt.

%description -l de
Newt ist eine Programmierbibliothek f¸r farbigen Text-Modus mit einer auf
Widgets aufbauenden Benutzerschnittstelle.  Newt kann benutzt werden, um
Fenster zu stapeln, und um einer Benutzerschnittstelle im Textmodus,
Eingabefelder, Checkboxen, Radioknˆpfe, Beschriftungen, Textfelder,
Rollbalken usw. hinzuzuf¸gen.  Diese Paket enth‰lt nicht nur die Bibliothek,
die benˆtigt wird, um Programme mit Newt zu erzeugen, sondern auch einen
Ersatz namens Whiptail f¸r das Programm /usr/bin/dialog.  Newt basiert
auf der S-Lang-Bibliothek.

%description -l de devel
Das Paket newt-devel enth‰lt die Headerdateien und Bibliotheken, die f¸r
die Entwicklung von Prgorammen, die newt benutzen, benˆtigt werden.  Newt
ist eine Entwicklungsbibliothek, f¸r Benutzerschnittstellen im Textmodus.
Newt baut auf der S-Lang-Bibliothek auf.

Newt sollte installiert werden, wenn die Entwicklung von Anwendungen,
die newt benutzen, geplant ist.

%prep
%setup
%patch0 -p1 -b .inc
%patch1 -p1 -b .mint

%build
%ifarch m68kmint
CFLAGS="$RPM_OPT_FLAGS" \
CXXFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix}
make RPM_OPT_FLAGS="${RPM_OPT_FLAGS}" libnewt.a
make RPM_OPT_FLAGS="${RPM_OPT_FLAGS}" whiptail
%else
CFLAGS="$RPM_OPT_FLAGS" \
CXXFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix} \
	--with-gpm-support
make RPM_OPT_FLAGS="${RPM_OPT_FLAGS}"
%endif
# make shared

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make instroot=$RPM_BUILD_ROOT install
# make instroot=$RPM_BUILD_ROOT install-sh

%clean
rm -rf $RPM_BUILD_ROOT

#%#post -p /sbin/ldconfig

#%#postun -p /sbin/ldconfig

%files
%defattr (-,root,root)
%doc CHANGES COPYING
#%#{_prefix}/lib/libnewt.so.*
%{_prefix}/bin/whiptail
#%#{_prefix}/lib/python1.5/snack.py
#%#{_prefix}/lib/python1.5/lib-dynload/_snackmodule.so

%files devel
%defattr (-,root,root)
%doc tutorial.sgml
%{_prefix}/include/newt.h
%{_prefix}/lib/libnewt.a
#%#{_prefix}/lib/libnewt.so

%changelog
* Sat Apr 01 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Sun Dec 26 1999 Guido Flohr <guido@freemint.de>
- Don't use color mode on monochrome terminals.

* Sun Dec 19 1999 Guido Flohr <guido@freemint.de>
- First release for Sparemint.
