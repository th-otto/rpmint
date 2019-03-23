Summary       : MiNT Utilities
Summary(de)   : Nützliche Werkzeuge für MiNT
Name          : mint-util
Version       : 0.3.2
Release       : 2
Copyright     : GPL
Group         : System Environment/Base

Packager      : Guido Flohr <guido@freemint.de>
Vendor        : Sparemint
URL           : http://sparemint.atari.org/

Requires      : sh-utils, fileutils, textutils, /bin/bash

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: mint-util-%{version}.tar.gz


%description
The package mint-util is a collection of small utilities that don't 
really fit into other packages.  Thus the package hasn't got a real
theme.

%description -l de
Das Paket mint-util ist ein Sammelsurium kleiner Werkzeuge, die in
kein anderes Paket richtig hineinpassen.  Das Paket hat also kein
echtes Thema.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

mkdir -p ${RPM_BUILD_ROOT}/bin
# move some things to /bin
for i in aes crlf ctrlaltdel free kill more rename sln ; do
    install -m 755 ${RPM_BUILD_ROOT}%{_prefix}/bin/$i ${RPM_BUILD_ROOT}/bin/$i
    rm -f ${RPM_BUILD_ROOT}%{_prefix}/bin/$i
done

mkdir -p ${RPM_BUILD_ROOT}/sbin
mv ${RPM_BUILD_ROOT}%{_prefix}/sbin/drivers ${RPM_BUILD_ROOT}/sbin

strip ${RPM_BUILD_ROOT}/{bin,sbin,%{_prefix}/bin}/* ||:

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

# compress manuals
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:

# don't ship ctraltdel, not implemented yet
rm -f ${RPM_BUILD_ROOT}/bin/ctrlaltdel


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README COPYING ChangeLog NEWS text-utils/crlf.doc */README.*
/bin/*
/sbin/*
%{_prefix}/bin/*
%{_prefix}/share/man/*/*


%changelog
* Fri Nov 02 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.3.2
- new getif skript
- AES starter set now AESDIR

* Mon Sep 13 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.3.1, small bugfix in the AES starter

* Mon Sep 10 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.3, added lot of new and useful tools

* Fri Sep 03 1999 Frank Naumann <fnaumann@freemint.de>
- added mktemp patch to crlf.c, crlf work now with the new MiNTLib

* Wed Aug 11 1999 Guido Flohr <guido@freemint.de>
- Updated to version 0.2
- Built against MiNTLib 0.52.3b
- Added requirements
