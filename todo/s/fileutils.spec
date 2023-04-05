Summary       : GNU File Utilities
Summary(de)   : GNU-Datei-Utilities 
Summary(fr)   : Utilitaires fichier de GNU
Summary(pl)   : GNU File Utilities
Summary(tr)   : GNU dosya iþlemleri yardýmcý yazýlýmlarý
Name          : fileutils
Version       : 4.1
Release       : 2
License       : GPL
Group         : Applications/File
Group(de)     : Applikationen/Datei
Group(pl)     : Aplikacje/Pliki

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.gnu.org/software/fileutils/

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://alpha.gnu.org/gnu/fetish/fileutils-%{version}.tar.gz
Source1: DIR_COLORS
Source2: fileutils.sh
Source3: fileutils.csh

Patch0: fileutils-4.1-info.patch
Patch1: fileutils-4.1-C.patch
Patch2: fileutils-4.1-install-specialbits.patch
Patch3: fileutils-4.1-sparc.patch
Patch4: fileutils-4.1-glibc22.patch
Patch5: fileutils-4.1-overwrite.patch
Patch6: fileutils-4.1-trunc.patch
Patch7: fileutils-4.1-mint.patch
Patch8: fileutils-4.1-getopt.patch


%description
The fileutils package includes a number of GNU versions of common and
popular file management utilities. Fileutils includes the following
tools:
- chgrp (changes a file's group ownership),
- chown (changes a file's ownership),
- chmod (changes a file's permissions),
- cp (copies files),
- dd (copies and converts files),
- df (shows a filesystem's disk usage),
- dir (gives a brief directory listing),
- dircolors (the setup program for the color version of the ls
  command),
- du (shows disk usage),
- install (copies files and sets permissions),
- ln (creates file links),
- ls (lists directory contents in color),
- mkdir (creates directories),
- mkfifo (creates FIFOs, which are named pipes),
- mknod (creates special files),
- mv (renames files),
- rm (removes/deletes files),
- rmdir (removes empty directories),
- sync (synchronizes memory and disk),
- touch (changes file timestamps),
- vdir (provides long directory listings).

You should install the fileutils package, because it includes many
file management utilities that you'll use frequently.

%description -l de
Dies sind die GNU-Dateiverwaltungs-Utilities. Sie enthalten Programme
zum Kopieren, Bewegen, Auflisten usw. von Dateien.

%description -l fr
Utilitaire de gestion de fichiers de GNU. Contient les programmes pour
copier, déplacer, lister, etc. les fichiers.

Le programme ls de ce paquetage incorpore maintenant ls en couleurs !

%description -l pl
Pakiet zawiera narzêdzia do zarz±dzania plikami, m.in. do kopiowania,
przemieszczania i listowania plików.

Program ls w tym pakiecie potrafi wy¶wietlaæ znaki ASCII w kolorach.

%description -l tr
Bu pakette yer alan programlar dosyalar üzerinde kopyalama, isim
deðiþtirme gibi temel iþlemleri yapmanýzý saðlar.


%prep
%setup -q
%patch0 -p1 -b .info
%patch1 -p1 -b .C
%patch2 -p1 -b .install-specialbits
%patch3 -p1 -b .sparc
%patch4 -p1 -b .glibc22
%patch5 -p1 -b .overwrite
%patch6 -p1 -b .trunc
%patch7 -p1 -b .mint
%patch8 -p1 -b .getopt


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--exec_prefix=/
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}/ \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

# move some things to %{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
for i in install du dir vdir dircolors shred ; do
    install -m 755 ${RPM_BUILD_ROOT}/bin/$i ${RPM_BUILD_ROOT}%{_prefix}/bin/$i
    rm -f ${RPM_BUILD_ROOT}/bin/$i
done

# don't ship mkfifo, mknod
rm ${RPM_BUILD_ROOT}/bin/mkfifo
rm ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/mkfifo.*
rm ${RPM_BUILD_ROOT}/bin/mknod
rm ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/mknod.*

mkdir -p ${RPM_BUILD_ROOT}/etc/profile.d
install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}/etc
install -m 755 %{SOURCE2} %{SOURCE3} ${RPM_BUILD_ROOT}/etc/profile.d

strip ${RPM_BUILD_ROOT}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

stack --fix=300k ${RPM_BUILD_ROOT}/bin/cp || :
stack --fix=128k ${RPM_BUILD_ROOT}/bin/rm || :

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/fileutils*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/fileutils.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/fileutils.info.gz %{_prefix}/info/dir
fi


%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%config /etc/DIR_COLORS
/etc/profile.d/*
/bin/*
%{_prefix}/bin/*
%{_prefix}/info/fileutils*
%{_prefix}/share/locale/*/*/*
%{_prefix}/share/man/man*/*


%changelog
* Fri Sep 28 2001 Frank Naumann <fnaumann@freemint.de>
- added missing df tool
- compiled against MiNTLib 0.57.1

* Wed Sep 19 2001 Frank Naumann <fnaumann@freemint.de>
- recompiled against bugfixed MiNTLib without PATHMAX problems

* Thu Sep 13 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 4.1

* Mon Nov 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against bugfixed MiNTLib 0.55 that solve wrong
  error code emulation (rm problems)

* Sun Jul 16 2000 Marc-Anton Kehr <m.kehr@ndh.net>
- rebuild against MiNTLib 0.55, this fixes some problems

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
