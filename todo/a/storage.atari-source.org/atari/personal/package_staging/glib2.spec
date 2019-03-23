%define		_sysconfdir	/etc
Summary: 	A library of handy utility functions.
Name: 		glib2
Version: 	2.2.3
Release: 	2
License: 	LGPL
Group: 		System/Libraries
Packager: 	Keith Scroggins <kws@radix.net>
Vendor:		Sparemint
Source: 	ftp://ftp.gtk.org/pub/gtk/v2.2/glib-%{version}.tar.gz
BuildRoot: 	%{_tmppath}/glib-%{PACKAGE_VERSION}-root
URL: 		http://www.gtk.org

%description
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

Glib is used by GDK, GTK+ and many applications.
You should install Glib because many of your applications
will depend on this library.

This package contains the library needed to run programs dynamically
linked with the glib.

%package devel
Summary: GIMP Toolkit and GIMP Drawing Kit support library
Group: Development/C

%description devel
Static libraries and header files for the support library for the GIMP's X
libraries, which are available as public libraries.  GLIB includes generally
useful data structures.

%prep
%setup -q -n glib-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" LIBS=-lsocket ./configure --prefix=/usr \
	--host=m68k-atari-mint --target=m68k-atari-mint \
	--build=m68k-atari-mint --enable-threads=yes \
	--with-threads=posix
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
cd $RPM_BUILD_ROOT/usr/include && ln -sf ../lib/glib-2.0/include/glibconfig.h glibconfig.h

strip -R.comment -R.note $RPM_BUILD_ROOT/bin/* 2>/dev/null || : 
strip -R.comment -R.note $RPM_BUILD_ROOT/sbin/* 2>/dev/null || :
strip -R.comment -R.note $RPM_BUILD_ROOT/lib/*.a 2>/dev/null || :
strip -R.comment -R.note $RPM_BUILD_ROOT/usr/bin/* 2>/dev/null || :
strip -R.comment -R.note $RPM_BUILD_ROOT/usr/sbin/* 2>/dev/null || :
strip -R.comment -R.note $RPM_BUILD_ROOT/usr/lib/*.a 2>/dev/null || :
strip -R.comment -R.note $RPM_BUILD_ROOT/usr/local/bin/* 2>/dev/null || :
strip -R.comment -R.note $RPM_BUILD_ROOT/usr/local/sbin/* 2>/dev/null || :
strip -R.comment -R.note $RPM_BUILD_ROOT/usr/local/lib/*.a 2>/dev/null || :
strip -R.comment -R.note $RPM_BUILD_ROOT/usr/X11R6/bin/* 2>/dev/null || :
strip -R.comment -R.note $RPM_BUILD_ROOT/usr/X11R6/lib/*.a 2>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
#/usr/lib/lib*.so.*
/usr/lib/lib*.a
/usr/lib/*.la

%files devel
%defattr(-, root, root)
/usr/bin
/usr/include
/usr/lib/pkgconfig
/usr/lib/glib-2.0
/usr/share
/usr/man

%changelog
* Fri Jan 09 2004 Keith Scroggins <kws@radix.net>
- Rebuilt RPM using Mark Duckworth's Glib2 build
* Fri Dec 05 2003 Keith Scroggins <kws@radix.net>
- Initial build of glib 2.2.3 for MiNT
