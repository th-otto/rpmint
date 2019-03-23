%define  ver     0.1.11
%define  rel     1
%define  prefix  /usr

Summary: Library to handle various audio file formats.
Name: audiofile
Version: %ver
Release: %rel
Copyright: LGPL
Group: System Environment/Libraries
Source: ftp://ftp.68k.org/pub/michael/audiofile-%{PACKAGE_VERSION}.tar.gz
URL: http://www.68k.org/~michael/audiofile/
Distribution: Sparemint
Vendor: Sparemint
Packager: Edgar Aichinger <eaiching@t0.or.at>

BuildRoot:/var/tmp/audiofile-%{PACKAGE_VERSION}-root
Docdir: %{prefix}/doc
Summary(de): Library für den Umgang mit verschiedenen Audio-Dateiformaten.

%description
The Audio File Library provides an elegant API for accessing a variety
of audio file formats, such as AIFF/AIFF-C, WAVE, and NeXT/Sun
.snd/.au, in a manner independent of file and data formats.

%description -l de
Die Audiofile-Bibliothek stellt ein elegantes API für den (vom Datei- und 
Datenformat unabhängigen) Zugriff auf eine Reihe von Audioformaten zu 
Verfügung, so wie AIFF/AIFF-C, WAVE, und NeXT/Sun .snd/.au. 

%package devel
Summary: Library, headers, etc. to develop with the Audio File Library.
Group: Libraries

%description devel
Library, header files, etc. for developing applications with the Audio
File Library.

%description devel -l de
Bibliotheken, Headerdateien und mehr, um mit audiofile Anwendungen
zu entwickeln.

%prep
%setup -q
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix --host=m68k-atari-mint

%build

make

%install

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

#
# makefile is broken, sets exec_prefix explicitely.
#
make exec_prefix=$RPM_BUILD_ROOT%{prefix} prefix=$RPM_BUILD_ROOT%{prefix} install 

# strip binaries
#strip `file $RPM_BUILD_ROOT%{prefix}/bin/* | awk -F':' '/not strip/ { print $1 }'`
strip $RPM_BUILD_ROOT%{prefix}/bin/sfinfo
strip $RPM_BUILD_ROOT%{prefix}/bin/sfconvert

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc COPYING TODO README ChangeLog docs
%{prefix}/bin/sf*
#%{prefix}/lib/lib*.so.*

%files devel
%defattr(-, root, root)
%{prefix}/bin/audiofile-config
#%{prefix}/lib/lib*.so
%{prefix}/lib/*.a
%{prefix}/include/*
%{prefix}/share/aclocal/*

%changelog
* Sat Dec 09 2000 Edgar Aichinger <eaiching@t0.or.at>
- new version

* Sat Apr 01 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Sun Nov 14 1999 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT 
