Summary       : Library providing XML and HTML support
Name          : libxml2
Version       : 2.4.20
Release       : 1
Copyright     : MIT
Group         : Development/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://xmlsoft.org/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://xmlsoft.org/libxml2-%{version}.tar.gz


%description
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package devel
Summary       : Libraries, includes, etc. to develop XML and HTML applications
Group         : Development/Libraries
Requires      : libxml2 = %{PACKAGE_VERSION}
Requires      : zlib-devel, libiconv

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
LIBS=-liconv \
./configure \
	--prefix=%{_prefix} \
	--sysconfdir="/etc" \
	--host=m68k-atari-mint \
	--without-python
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=${RPM_BUILD_ROOT}%{_prefix}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README Copyright TODO
%{_prefix}/bin/xmlcatalog
%{_prefix}/bin/xmllint
%{_prefix}/share/man/man1/xmlcatalog.1*
%{_prefix}/share/man/man1/xmllint.1*

%files devel
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README Copyright TODO
%doc doc/*.html doc/html doc/*.gif doc/*.png
%{_prefix}/bin/xml2-config
%{_prefix}/include/*
%{_prefix}/lib/*a
%{_prefix}/lib/*.sh
%{_prefix}/share/aclocal/libxml.m4
%{_prefix}/share/man/man1/xml2-config.1*
%{_prefix}/share/man/man3/libxml.3*


%changelog
* Tue Apr 23 2002 Frank Naumann <fnaumann@freemint.de>
- updated to 2.4.20

* Tue Jul 10 2001 Frank Naumann <fnaumann@freemint.de>
- first release
