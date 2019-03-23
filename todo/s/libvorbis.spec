Name:		libvorbis
Version:	1.3.1
Release:	1
Summary: 	Vorbis Library Development
Group: 		Development/Libraries
Vendor:	   	Sparemint
Packager:  	Keith Scroggins <kws@radix.net>
Distribution: 	Sparemint
License:	BSD
URL:		http://www.xiph.org/
Source:		http://www.xiph.org/pub/ogg/vorbis/download/%{name}-%{version}.tar.bz2
Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-root

Requires:	libogg >= 1.2.0
BuildRequires:	libogg >= 1.2.0 sed >= 4.2.1

%description
Ogg Vorbis is a fully open, non-proprietary, patent-and-royalty-free,
general-purpose compressed audio format for audio and music at fixed 
and variable bitrates from 16 to 128 kbps/channel.

The libvorbis package contains the header files, static libraries 
and documentation needed to develop applications with libvorbis.

%prep
%setup -q -n %{name}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS -m68020-60" LDFLAGS="-s -m68020-60" \
./configure --prefix=%prefix --libdir=/usr/lib/m68020-60
make
mkdir 68020-60
mv ./lib/.libs/libvorbis* 68020-60/
mv 68020-60/libvorbis.lai 68020-60/libvorbis.la
mv 68020-60/libvorbisenc.lai 68020-60/libvorbisenc.la
mv 68020-60/libvorbisfile.lai 68020-60/libvorbisfile.la
sed -i "s#lib #lib/m68020-60 #" 68020-60/*.la
sed -i "s#lib/lib#lib/m68020-60/lib#" 68020-60/*.la
make clean
CFLAGS="$RPM_OPT_FLAGS -mcpu=5475" LDFLAGS="-s -mcpu=5475" \
./configure --prefix=%prefix --libdir=/usr/lib/m5475 \
--host=m68k-atari-mint
make
mkdir 5475
mv ./lib/.libs/libvorbis* 5475/
mv 5475/libvorbis.lai 5475/libvorbis.la
mv 5475/libvorbisenc.lai 5475/libvorbisenc.la
mv 5475/libvorbisfile.lai 5475/libvorbisfile.la
sed -i "s#lib #lib/m5475 #" 5475/*.la
sed -i "s#lib/lib#lib/m5475/lib#" 5475/*.la
make clean
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s \
./configure --prefix=%prefix
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60
install -m644 68020-60/libvorbis.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libvorbis.a
install -m644 68020-60/libvorbis.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libvorbis.la
install -m644 68020-60/libvorbisenc.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libvorbisenc.a
install -m644 68020-60/libvorbisenc.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libvorbisenc.la
install -m644 68020-60/libvorbisfile.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libvorbisfile.a
install -m644 68020-60/libvorbisfile.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libvorbisfile.la
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475
install -m644 5475/libvorbis.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libvorbis.a
install -m644 5475/libvorbis.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libvorbis.la
install -m644 5475/libvorbisenc.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libvorbisenc.a
install -m644 5475/libvorbisenc.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libvorbisenc.la
install -m644 5475/libvorbisfile.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libvorbisfile.a
install -m644 5475/libvorbisfile.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libvorbisfile.la


%clean 
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%defattr(-,root,root)
%doc COPYING
%doc AUTHORS
%doc README
%doc doc/*.html
%doc doc/*.png
%doc doc/*.txt
%doc doc/vorbisfile
%doc doc/vorbisenc
%{_datadir}/aclocal/vorbis.m4
%{_includedir}/vorbis/codec.h
%{_includedir}/vorbis/vorbisfile.h
%{_includedir}/vorbis/vorbisenc.h
%{_libdir}/libvorbis.a
%{_libdir}/libvorbis.la
%{_libdir}/libvorbisfile.a
%{_libdir}/libvorbisfile.la
%{_libdir}/libvorbisenc.a
%{_libdir}/libvorbisenc.la
%{_libdir}/m68020-60/libvorbis.a
%{_libdir}/m68020-60/libvorbis.la
%{_libdir}/m68020-60/libvorbisfile.a
%{_libdir}/m68020-60/libvorbisfile.la
%{_libdir}/m68020-60/libvorbisenc.a
%{_libdir}/m68020-60/libvorbisenc.la
%{_libdir}/m5475/libvorbis.a
%{_libdir}/m5475/libvorbis.la
%{_libdir}/m5475/libvorbisfile.a
%{_libdir}/m5475/libvorbisfile.la
%{_libdir}/m5475/libvorbisenc.a
%{_libdir}/m5475/libvorbisenc.la

%changelog
* Tue Aug 24 2010 Keith Scroggins <kws@radix.net>
- Added 68020-60 and 5475 libs and updated to 1.3.1

* Tue Sep 28 2003 Adam Klobukowski <atari@gabo.pl>
- Adapted for FreeMiNT and SpareMiNT

* Sun Jul 14 2002 Thomas Vander Stichele <thomas@apestaart.org>
- Added BuildRequires:
- updated for 1.0 release

* Sat May 25 2002 Michael Smith <msmith@icecast.org>
- Fixed requires, copyright string.
* Sun Dec 31 2001 Jack Moffitt <jack@xiph.org>
- Updated for rc3 release.

* Sun Oct 07 2001 Jack Moffitt <jack@xiph.org>
- Updated for configurable prefixes

* Sat Oct 21 2000 Jack Moffitt <jack@icecast.org>
- initial spec file created
