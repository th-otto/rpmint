Summary       : A general purpose sound file conversion tool.
Summary(de)   : Ein Audio-Konvertierprogramm.
Name          : sox
Version       : 12.17.3
Release       : 1
Copyright     : distributable
Group         : Applications/Multimedia

Packager      : Edgar Aichinger <eaiching@t0.or.at>
Vendor        : Sparemint
URL           : http://home.sprynet.com/sprynet/cbagwell/

BuildRequires : gsm

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root
Source        : http://home.sprynet.com/sprynet/cbagwell/%{name}-%{version}.tar.gz
Patch         : %{name}-mint.patch

%description
SoX (Sound eXchange) is a sound file format converter for MiNT, Linux,
UNIX and DOS PCs. The self-described 'Swiss Army knife of sound
tools,' SoX can convert between many different digitized sound
formats and perform simple sound manipulation functions,
including sound effects.

%description -l de
SoX (Sound eXchange) ist ein Audio-Dateiformat-Konverter, für 
MiNT, Linux, UNIX und DOS PC's. Das 'Schweizermesser der sound tools', 
wie es sich selbst nennt, kann zwischen vielen verschiedenen Soundformaten 
konvertieren und einfache Manipulationen durchführen, wie auch
Klangeffekte einrechnen.

Installieren Sie sox, falls Sie gerne Audio-Dateiformate konvertieren würden 
oder Klänge manipulieren wollen.

%package -n  sox-devel
Summary: The SoX sound file format converter libraries.
Group: Development/Libraries
Summary(de): Die SoX-Bibliotheken zum Konvertieren von Audio-Dateiformate.

%description -n sox-devel 
This package contains the library needed for compiling applications
which will use the SoX sound file format converter.

Install sox-devel if you want to develop applications which will use
SoX.

%description -l de -n sox-devel 
Dieses Paket beinhaltet die benötigten Bibliotheken, um Anwendungen 
zu kompilieren, die SoX, den Audio-Dateiformat-Konvertierer, benützen.

Installieren Sie sox-devel, falls Sie Applikationen entwickeln, die
SoX benützen.


%prep
%setup -q 
%patch -p1

%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	m68k-atari-mint \
	--prefix=%{_prefix}

make 
make play

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/{bin,lib,man/{man1,man3}}

make prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}%{_exec_prefix} install
make prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}%{_exec_prefix} install-lib 
make prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}%{_exec_prefix} install-play

echo '#!/bin/sh' > ${RPM_BUILD_ROOT}%{_prefix}/bin/soxplay
echo "" >> ${RPM_BUILD_ROOT}%{_prefix}/bin/soxplay
echo '%{_prefix}/bin/sox $1 -t .au - > /dev/audio' >> ${RPM_BUILD_ROOT}%{_prefix}/bin/soxplay
chmod 755 ${RPM_BUILD_ROOT}%{_prefix}/bin/soxplay

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/sox
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/soxmix

# no rec support in mint
#ln -snf play ${RPM_BUILD_ROOT}%{_prefix}/bin/rec
rm ${RPM_BUILD_ROOT}%{_prefix}/bin/rec
rm ${RPM_BUILD_ROOT}%{_prefix}/man/man1/rec.1

# install header files
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/include/sox
install -m 644 *.h ${RPM_BUILD_ROOT}%{_prefix}/include/sox
install -m 644 libst.3 ${RPM_BUILD_ROOT}%{_prefix}/man/man3

# remove bad symlink for soxmix.1
rm ${RPM_BUILD_ROOT}%{_prefix}/man/man1/soxmix.1

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/*/*

# fix symlink for soxmix.1
( cd ${RPM_BUILD_ROOT}%{_prefix}/man/man1; ln -snf sox.1.gz soxmix.1.gz )

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc Changelog README TODO INSTALL 
%{_prefix}/bin/sox
%{_prefix}/bin/soxmix
%{_prefix}/bin/play
# no rec support in mint
#%{_prefix}/bin/rec
%{_prefix}/bin/soxplay
%{_prefix}/share/man/man1/*

%files -n sox-devel
%defattr(-,root,root)
%{_prefix}/include/sox
%{_prefix}/lib/libst.a
%{_prefix}/share/man/man3/*


%changelog
* Sun Feb 10 2002 Edgar Aichinger <eaiching@t0.or.at>
- updated to 12.17.3
- fix for broken soxmix manpage (specfile)
- patched play script to work under MiNT
- removed /usr/bin/rec from distribution (not only manpage)

%changelog
* Wed Oct 17 2001 Edgar Aichinger <eaiching@t0.or.at>
- updated to 12.17.2

* Sun Feb 18 2001 Marc-Anton Kehr <m.kehr@ndh.net>
- updated to 12.17.1
- added gsm support 

* Sat Sep 25 1999 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT 
