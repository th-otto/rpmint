# Note that this is NOT a relocatable package
%define ver     1.2.8
%define RELEASE 1
%define rel     %{?CUSTOM_RELEASE} %{!?CUSTOM_RELEASE:%RELEASE}
%define prefix  /usr

Summary: Handy library of utility functions
Name: glib
Version: %ver
Release: %rel
Copyright: LGPL
Group: Libraries
Source: ftp://ftp.gimp.org/pub/gtk/v1.1/glib-%{ver}.tar.gz
BuildRoot: /var/tmp/glib-%{PACKAGE_VERSION}-root
URL: http://www.gtk.org
Docdir: %{prefix}/doc
Packager: Frank Naumann <fnaumann@freemint.de>
Vendor: Sparemint

%description
Handy library of utility functions. Development libs and headers
files.
#are in glib-devel.
#
#%#package devel
#Summary: GIMP Toolkit and GIMP Drawing Kit support library
#Group: X11/Libraries
#
#%#description devel
#Static libraries and header files for the support library for the GIMP's X
#libraries, which are available as public libraries.  GLIB includes generally
#useful data structures.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{prefix}
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} install
mv $RPM_BUILD_ROOT%{prefix}/man $RPM_BUILD_ROOT%{prefix}/share
gzip -9nf $RPM_BUILD_ROOT%{prefix}/share/man/*/*

%clean
rm -rf $RPM_BUILD_ROOT

#%#post -p /sbin/ldconfig

#%#postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
#%#{prefix}/lib/libglib-1.2.so.*
#%#{prefix}/lib/libgthread-1.2.so.*
#%#{prefix}/lib/libgmodule-1.2.so.*

#%#files devel
#%#defattr(-, root, root)
#%#{prefix}/lib/lib*.so
%{prefix}/lib/*a
%{prefix}/lib/glib
%{prefix}/include/*
%{prefix}/share/aclocal/*
%{prefix}/share/man/man1/*
%{prefix}/bin/*

%changelog
* Wed Jul 06 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
