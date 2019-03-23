Summary       : A program for synchronizing files over a network.
Summary(de)   : Ein Program fuer die Synchronisierung von Dateien ueber ein Netzwerk.
Name          : rsync
Version       : 2.5.4
Release       : 1
Copyright     : GPL
Group         : Applications/Internet

Packager      : Guido Flohr <guido@freemint.de>
Vendor        : Sparemint
URL           : http://rsync.samba.org/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source:	ftp://rsync.samba.org/pub/rsync/rsync-%{version}.tar.gz
Patch0: rsync-2.3.1-chroot.patch


%description
Rsync uses a quick and reliable algorithm to very quickly bring
remote and host files into sync.  Rsync is fast because it just
sends the differences in the files over the network (instead of
sending the complete files).  Rsync is often used as a very powerful
mirroring process or just as a more capable replacement for the
rcp command.  A technical report which describes the rsync algorithm
is included in this package.

Install rsync if you need a powerful mirroring program.

%description -l de
Rsync benutzt einen schnellen und zuverlässigen Algorithmus, um
Dateien auf einem entfernten und dem lokalen Rechner in Einklang
zu bringen. Rsync ist schnell, weil es nur die Unterschiede
zwischen Dateien über das Netzwerk schickt (anstatt die kompletten
Dateien zu senden).  Rsync wird oft als ein mächtiger Mirror-Prozess
verwendet oder auch einfach als leistungsfähigerer Ersatz für 
dass rcp-Kommando.  Ein technisches Dokument, das den rsync-Algorithmus
beschreibt, ist Bestandteil dieses Paketes.

Rsync sollte installiert werden, wenn ein mächtiges Spiegelprogramm
benötigt wird.


%prep
%setup -q
%patch0 -p1 -b .chroot


%build
CFLAGS="${RPM_OPT_FLAGS}" \
LIBS="-lsocket" \
./configure \
	--prefix=%{_prefix} \
	--disable-largefile

make CCOPTFLAGS="${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make prefix=${RPM_BUILD_ROOT}%{_prefix} install

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/man*/* ||:

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc tech_report.tex README COPYING
%{_prefix}/bin/*
%{_prefix}/share/man/man*/*


%changelog
* Wed Mar 13 2002 Frank Naumann <fnaumann@freemint.de>
- updated to 2.5.5

* Wed Dec 04 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.5

* Sat Mar 16 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.4.6

* Tue Sep 08 1999 Guido Flohr <guido@freemint.de>
- Added chroot patch to hide security holes.
- Use correct optimization flags.

* Tue Sep 07 1999 Guido Flohr <guido@freemint.de>
- Initial revision.
