%define		_sysconfdir	/etc
Summary: 	A library of handy utility functions.
Name: 		glib2
Version: 	2.2.3
Release: 	1
License: 	LGPL
Group: 		System/Libraries
Packager: 	Keith Scroggins <kws@radix.net>
Vendor:		Sparemint
Source: 	ftp://ftp.gtk.org/pub/gtk/v2.2/glib-%{version}.tar.gz
BuildRoot: 	%{_tmppath}/glib-%{PACKAGE_VERSION}-root
URL: 		http://www.gtk.org
Requires:	pkgconfig pth-devel libiconv
BuildRequires:	pkgconfig pth-devel libiconv

%description 
Glib2 is a handy library of utility functions. This C library is designed
to solve some portability problems and provide other useful functionality
which most programs require.

Glib2 is used by GDK, GTK+ and many applications. You should install Glib
because it is hoped that many applications that use it will be ported to
MiNT.

This package contains the library needed to run programs statically
linked with the glib2 libraries.

=================
!!! IMPORTANT !!!
=================
2 test programs (out of 30) currently fail with this build:

mainloop-test fails in glib2 due to the pthread implemetation we are
using, which is pth.  This is supposedly due to the fact that pth is
cooperative library only, and glib2 wants a pre-emptive thread
implemetation.

strtod-test looks like it fails due to the size of the integers being
processed (just a wild guess).  Could also be a problem with Glib2 using it's
own 'trio' support instead of native support.  More research needed.

%package devel
Summary: GIMP Toolkit and GIMP Drawing Kit support library
Group: Development/C

%description devel
Static libraries and header files for the support library for the GIMP's X
libraries, which are available as public libraries.  GLIB includes generally
useful data structures.

=================
!!! IMPORTANT !!!
=================
2 test programs (out of 30) currently fail with this build:

mainloop-test fails in glib2 due to the pthread implemetation we are
using, which is pth.  This is supposedly due to the fact that pth is
cooperative library only, and glib2 wants a pre-emptive thread
implemetation.

strtod-test looks like it fails due to the size of the integers being
processed (just a wild guess).  Could also be a problem with Glib2 using it's
own 'trio' support instead of native support.  More research needed.

%prep
%setup -q -n glib-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" LIBS=-lsocket ./configure \
	--prefix=/usr --host=m68k-atari-mint --target=m68k-atari-mint \
	--build=m68k-atari-mint --enable-threads=yes \
	--with-threads=posix --disable-shared --enable-static \
	--with-libiconv=gnu --with-gnu-ld
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
cd $RPM_BUILD_ROOT/usr/include && ln -sf ../lib/glib-2.0/include/glibconfig.h glibconfig.h

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
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
* Thu Jan 22 2004 Keith Scroggins <kws@radix.net>
- After many builds on both Mark Duckworth's Falcon and my own, this is finally
- the initial, mostly working, release of Glib2 for MiNT!
