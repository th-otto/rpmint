Name:		libogg
Version:	1.2.0
Release:	1
Summary: 	Ogg Bitstream Library Development
Group: 		Development/Libraries
License:	BSD
URL:		http://www.xiph.org/
Vendor:		Sparemint
Packager:	Keith Scroggins <kws@radix.net>
Distribution:	Sparemint
Source:		http://www.xiph.org/pub/ogg/vorbis/download/%{name}-%{version}.tar.gz
Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Libogg is a library for manipulating ogg bitstreams.  It handles
both making ogg bitstreams and getting packets from ogg bitstreams.

The libogg package contains the header files, static libraries
and documentation needed to develop applications with libogg.

%prep
%setup -q -n %{name}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS -m68020-60" LDFLAGS="-s -m68020-60" \
./configure --prefix=%prefix --libdir=/usr/lib/m68020-60
make
mkdir 68020-60
mv ./src/.libs/libogg.* 68020-60/
mv 68020-60/libogg.lai 68020-60/libogg.la
make clean
CFLAGS="$RPM_OPT_FLAGS -mcpu=5475" LDFLAGS="-s -mcpu=5475" \
./configure --prefix=%prefix --libdir=/usr/lib/m5475 \
--host=m68k-atari-mint
make
mkdir 5475
mv ./src/.libs/libogg.* 5475/
mv 5475/libogg.lai 5475/libogg.la
make clean
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s \
./configure --prefix=%prefix
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60
install -m644 68020-60/libogg.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libogg.a
install -m644 68020-60/libogg.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libogg.la
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475
install -m644 5475/libogg.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libogg.a
install -m644 5475/libogg.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libogg.la

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%defattr(-,root,root)
%doc share/doc/libogg-%{version}/*
%doc AUTHORS CHANGES COPYING README
%{_includedir}/ogg/ogg.h
%{_includedir}/ogg/os_types.h
%{_includedir}/ogg/config_types.h
%{_libdir}/libogg.a
%{_libdir}/libogg.la
%{_libdir}/m68020-60/libogg.a
%{_libdir}/m68020-60/libogg.la
%{_libdir}/m5475/libogg.a
%{_libdir}/m5475/libogg.la
%{_datadir}/aclocal/ogg.m4

%changelog
* Mon Aug 23 2010 Keith Scroggins <kws@radix.net>
- Added 68020-60 and 5475 libs and updated to 1.2.0

* Tue Sep 28 2003 Adam Klobukowski <atari@gabo.pl>
- adapted for FreeMiNT and SpareMiNT

* Sun Jul 14 2002 Thomas Vander Stichele <thomas@apestaart.org>
- update for 1.0 release
- conform Group to Red Hat's idea of it
- take out case where configure doesn't exist; a tarball should have it

* Tue Dec 18 2001 Jack Moffitt <jack@xiph.org>
- Update for RC3 release

* Sun Oct 07 2001 Jack Moffitt <jack@xiph.org>
- add support for configurable prefixes

* Sat Sep 02 2000 Jack Moffitt <jack@icecast.org>
- initial spec file created
