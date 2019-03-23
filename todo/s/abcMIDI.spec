%define versionyear 2012
%define versionmonth 08
%define versionday 08
%define urlbase http://ifdo.pugmarks.com/~seymour/runabc

Summary     : ABC <-> Midi conversion utilities
Name        : abcMIDI
Version     : %{versionyear}_%{versionmonth}_%{versionday}
Release     : 1
License     : GPL
Group       : Applications/Sound

Packager    : Martin Tarenskeen <m.tarenskeen@zonnet.nl>
Vendor      : Sparemint

URL         : %{urlbase}/top.html
Source      : %{urlbase}/%{name}-%{versionyear}-%{versionmonth}-%{versionday}.zip

Prefix      : %{_prefix}
Buildroot   : %{_tmppath}/%{name}-buildroot
#BuildArch   : m68kmint

%description
The abcMIDI package contains four programs: abc2midi to convert ABC music
notation to midi, midi2abc to convert midi files to (a first approximation
to) the corresponding ABC, abc2abc to reformat and/or transpose ABC files,
and yaps to typeset ABC files as PostScript.

For a description of the abc syntax, please see the abc userguide 
which is a part of the abc2mtex package written by Chris Walshaw.

Note: version numbering has changed. If rpm complains about this package 
being older than the one already installed, try the --oldpackage option. 

%prep
rm -rf abcmidi
unzip ${RPM_SOURCE_DIR}/%{name}-%{versionyear}-%{versionmonth}-%{versionday}.zip -d ${RPM_BUILD_DIR}

%build
cd abcmidi
%configure 
make  CFLAGS="$RPM_OPT_FLAGS -c -DANSILIBS"

#in case of memory problems try compiling the binaries separately: 
#make -f makefiles/unix.mak abc2midi CFLAGS="$RPM_OPT_FLAGS -c -DANSILIBS"
#make -f makefiles/unix.mak midi2abc CFLAGS="$RPM_OPT_FLAGS -c -DANSILIBS"
#make -f makefiles/unix.mak abc2abc CFLAGS="$RPM_OPT_FLAGS -c -DANSILIBS"
#make -f makefiles/unix.mak mftext CFLAGS="$RPM_OPT_FLAGS -c -DANSILIBS"
#make -f makefiles/unix.mak yaps CFLAGS="$RPM_OPT_FLAGS -c -DANSILIBS"
#make -f makefiles/unix.mak midicopy CFLAGS="$RPM_OPT_FLAGS -c -DANSILIBS"
#make -f makefiles/unix.mak abcmatch CFLAGS="$RPM_OPT_FLAGS -c -DANSILIBS"

%install
cd abcmidi
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 abc2midi $RPM_BUILD_ROOT%{_bindir}
install -m 755 abcmatch $RPM_BUILD_ROOT%{_bindir}
install -m 755 midi2abc $RPM_BUILD_ROOT%{_bindir}
install -m 755 midicopy $RPM_BUILD_ROOT%{_bindir}
install -m 755 abc2abc $RPM_BUILD_ROOT%{_bindir}
install -m 755 mftext $RPM_BUILD_ROOT%{_bindir}
install -m 755 yaps $RPM_BUILD_ROOT%{_bindir}
strip $RPM_BUILD_ROOT%{_bindir}/*
stack -S 128k $RPM_BUILD_ROOT%{_bindir}/*

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
gzip $RPM_BUILD_ROOT%{_mandir}/man1/*.1

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc abcmidi/doc/AUTHORS abcmidi/doc/CHANGES
%doc abcmidi/doc/*.txt 
%doc abcmidi/samples
%{_mandir}/*
%{_bindir}/*
 
%changelog
* Fri Aug 24 2012 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 2012_08_08

* Tue Dec 27 2011 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 2011_12_19

* Wed Nov 09 2011 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 2011_10_21

* Fri Dec 31 2010 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 2010_12_12
- more abc examples in documentation 

* Tue Apr 22 2008 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 2008_03_31

* Wed Feb 22 2006 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 2006_02_07
- changed specfile to be able to use the original source zip file.

* Sat Nov 12 2005 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 2005_11_06
- abcmatch added to package

* Sat Oct 15 2005 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 2005_10_10

* Fri Jul 23 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 2004_07_19
- contains new program midicopy
