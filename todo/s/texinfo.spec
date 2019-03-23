Summary       : texinfo formatter and info reader
Summary(de)   : texinfo-Formatier- und Leseprogramm
Summary(fr)   : Formatteur texinfo et lecteur pour info.
Summary(tr)   : texinfo biçimleyici ve info okuyucu
Name          : texinfo
Version       : 4.0
Release       : 2
Copyright     : GPL
Group         : Applications/Publishing

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.gnu.org/software/texinfo/

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.gz
Source1: info-dir
Source2: info.desktop
Patch1:  texinfo-3.12h-fix.patch
Patch2:  texinfo-fileextension.patch
Patch3:  texinfo-4.0-zlib.patch
Patch4:  texinfo-4.0-danish.patch
Patch5:  texinfo-4.0-mint.patch


%description
Texinfo is a documentation system that can produce both online information
and printed output from a single source file.  Normally, you'd have to
write two separate documents: one for online help or other online
information and the other for a typeset manual or other printed work.
Using Texinfo, you only need to write one source document.  Then when the
work needs revision, you only have to revise one source document.  The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you are
going to write documentation for the GNU Project.

%package -n info
Summary       : A standalone TTY-based reader for GNU texinfo documentation.
Summary(de)   : Unabhängiges tty-basiertes Leseprogramm für GNU-texinfo-Dokumente
Summary(fr)   : Lecteur autonome de documents texinfo pour terminal.
Summary(tr)   : GNU texinfo belgeleri için tty tabanlý görüntüleyici
Group         : Utilities/System
Prereq        : bash
# By making info prereq bash, other packages which have triggers based on
# info don't run those triggers until bash is in place as well. This is an
# ugly method of doing it (triggers which fire on set intersection would
# be better), but it's the best we can do for now. Talk to Erik before
# removing this.

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

You should install info, because GNU's texinfo documentation is a valuable
source of information about the software on your system.

%description -l de -n info
Das GNU-Projekt benutzt das texinfo-Dateiformat für den Großteil seiner
Dokumentation. Dieses Paket enthält ein selbständiges Browser-Programm 
zum Einsehen dieser Dateien in Terminals.

Das Paket info sollte installiert werden, denn GNUs Texinfo-Dokumentatio
ist eine wertvolle Informationsquelle für die auf dem System installierte
Software.

%description -l fr -n info
Le projet GNU utilise le format de fichier texinfo pour la plupart de sa
documentation. Ce paquetage contient un navigateur pour visualiser ces
fichiers.

%description -l fr
Le projet GBU utilise le format de fichier texinfo pour la plupart de sa
documentation. Ce paquetage contient les outils pour créer des fichiers .info
à partir des fichiers sources .texinfo, ainsi qu'une interface emacs pour tous
ces outils.

%description -l tr -n info
Bu pakette, info biçimindeki dosyalarý okumak için bir görüntüleyici
bulunur.

%description -l tr
GNU projesi, belgelemesinin büyük bölümünde texinfo dosyalarýný kullanýr.
Bu paket, texinfo dosyalarýndan info dosyalarýnýn türetilmesini saðlayan
araçlarla birlikte, tüm bu araçlar için bir emacs arayüzü de sunar.


%prep
%setup -q
%patch1 -p1
%patch2 -p1 -b .ext
%patch3 -p1 -b .zlib
%patch4 -p1 -b .danish
%patch5 -p1 -b .mint


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}
make

rm util/install-info
make -C util LIBS=%{_prefix}/lib/libz.a


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/sbin
make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

install -m644 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/info-dir
ln -sf ../../etc/info-dir ${RPM_BUILD_ROOT}%{_prefix}/info/dir
mv -f ${RPM_BUILD_ROOT}%{_prefix}/bin/install-info ${RPM_BUILD_ROOT}/sbin

mkdir -p ${RPM_BUILD_ROOT}/etc/X11/applnk/Utilities
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}/etc/X11/applnk/Utilities

strip ${RPM_BUILD_ROOT}/sbin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/*info*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/texinfo.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/texinfo.gz %{_prefix}/info/dir
fi

%post -n info
/sbin/install-info %{_prefix}/info/info-stnd.info.gz %{_prefix}/info/dir

%preun -n info
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/info-stnd.info.gz %{_prefix}/info/dir
fi


%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL INTRODUCTION NEWS README TODO
%doc info/README
%{_prefix}/bin/makeinfo
%{_prefix}/bin/texindex
%{_prefix}/bin/texi2dvi
%{_prefix}/info/texinfo*
%{_prefix}/share/locale/*/*/*
%{_prefix}/share/man/man1/makeinfo.1*
%{_prefix}/share/man/man1/texindex.1*
%{_prefix}/share/man/man1/texi2dvi.1*
%{_prefix}/share/man/man5/texinfo.5*

%files -n info
%defattr(-,root,root)
%config(missingok) /etc/X11/applnk/Utilities/info.desktop
%config(noreplace) %verify(not md5 size mtime) /etc/info-dir
%config(noreplace) %{_prefix}/info/dir
%{_prefix}/bin/info
%{_prefix}/info/info.info*
%{_prefix}/info/info-stnd.info*
/sbin/install-info
%{_prefix}/share/man/man1/info.1*
%{_prefix}/share/man/man1/install-info.1*
%{_prefix}/share/man/man5/info.5*


%changelog
* Mon Sep 17 2001 Frank Naumann <fnaumann@freemint.de>
- fixed a illegal memory access bug in texinfo

* Wed Sep 12 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 4.0

* Sun Aug 13 1999 Guido Flohr <guido@freemint.de>
- Updated to version 3.12f
- Changed vendor to Sparemint
- Incorporated changes from Redhat Linux 6.0:
  o Wed Mar 17 1999 Erik Troan <ewt@redhat.com>
  - hacked to use zlib to get rid of the requirement on gzip

  o Wed Mar 17 1999 Matt Wilson <msw@redhat.com>
  - install-info prerequires gzip

  o Thu Mar 11 1999 Cristian Gafton <gafton@redhat.com>
  - version 3.12f
  - make %{_prefix}/info/dir to be a %config(noreplace)
