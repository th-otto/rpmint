Summary       : An XML library.
Summary(de)   : Eine XML-Bibliothek.
Name          : libxml
Version       : 1.8.9
Release       : 1
Copyright     : LGPL
Group         : System Environment/Libraries

Packager      : Edgar Aichinger <eaiching@t0.or.at>
Vendor        : Sparemint
URL           : http://xmlsoft.org/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.gnome.org/pub/GNOME/stable/sources/libxml/libxml-%{version}.tar.gz
Patch0: libxml-mint.patch


%description
The libxml package contains an XML library, which allows you to
manipulate XML files. XML (eXtensible Markup Language) is a data
format for structured document interchange via the Web.

%description -l de
Das Paket libxml enthält eine XML-Bibliothek, die Ihnen ermöglicht,
XML-Dateien zu manipulieren. XML (eXtensible Markup Language) ist
ein Datenformat für den Austausch strukturierter Dokumente über das Web.

%package devel
Summary       : Libraries, includes and other files to develop libxml applications.
Summary(de)   : Bibliotheken, includes und andere Dateien zur Entwicklung von libxml-Applikationen.
Group         : Development/Libraries
Requires      : libxml = %{PACKAGE_VERSION}
Requires      : zlib-devel

%description devel
The libxml-devel package contains the libraries, include and other
files you can use to develop libxml applications.

%description devel -l de
Das Paket libxml-devel enthält die Bibliotheken, include- und andere
Dateien, die Sie verwenden können, um libxml-Applikationen zu entwickeln.


%prep
%setup -q
%patch0 -p1 -b .mint


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--sysconfdir="/etc" \
	--host=m68k-atari-mint

make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}%{_prefix}


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING COPYING.LIB TODO
%doc doc/html
%{_prefix}/bin/xml-config

%files devel
%defattr(-, root, root)
%{_prefix}/lib/*a
%{_prefix}/lib/*.sh
%{_prefix}/include/*


%changelog
* Wed Apr 26 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.8.9

* Sat Apr 01 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Sun Nov 07 1999 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT 
