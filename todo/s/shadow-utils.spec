Summary       : Shadow password file utilities for MiNT
Name          : shadow-utils
Version       : 20000902
Release       : 1
Copyright     : BSD
Group         : System Environment/Base

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Requires      : sh-utils >= 2.0.11

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.ists.pwr.wroc.pl/pub/linux/shadow/shadow-%{version}.tar.gz
Source1: shadow-970616.login.defs
Source2: shadow-970616.useradd
Source3: adduser.8
Source4: pwunconv.8
Source5: grpconv.8
Source6: grpunconv.8

Patch0: shadow-20000826-redhat.patch
Patch1: shadow-19990827-nscd.patch
Patch2: shadow-19990827-group.patch
Patch3: shadow-20000902-isascii.patch
Patch4: shadow-useradd.patch
Patch5: shadow-utils-minimal-uid.patch
Patch6: shadow-20000902-mint.patch
Patch7: shadow-20000902-sparemint.patch


%description
This package includes the programs necessary to convert traditional
V7 UNIX password files to the SVR4 shadow password format and additional
tools to work with shadow passwords.  Even if you don't want to enable
shadow passwords on your system you have to install this package since
it also provides basic tools for traditional password handling.

	- 'pwconv' converts everything to the shadow password format.
	- 'pwunconv' converts back to non-shadow passwords.
	- 'pwck' checks the integrity of the password and shadow files.
	- 'lastlog' prints out the last login times of all users.
	- 'useradd', 'userdel', 'usermod' to manage user accounts.
	- 'groupadd', 'groupdel', 'groupmod' to manage groups.

A number of man pages are also included that relate to these utilities,
and shadow passwords in general.

NOTE: If you want to rebuild this package from the sources, contact
the packager first.

IMPORTANT: Currently you shouldn't activate shadow user passwords for
other than testing purposes.  Too many programs cannot grok with 
shadow password files.

%description -l de
Dieses Paket beinhaltet Program, die notwendig sind, um traditionelle
Unix-V7-Passwort-Dateien in das SVR4-Schatten-Passwort-Format umzuwandeln.
Des weiteren sind noch zusätzliche Werkzeuge zur Arbeit mit 
Schattenpasswörtern enthalten.  Selbst, wenn Sie keine Schatten-Passwörter
auf Ihrem System aktivieren wollen, sollte dieses Paket unbedingt 
installiert werden, da es auch einige Grundwerkzeuge für die traditionelle
Behandlung von Passwörtern enthält.

	- »pwconv« konvertiert alles ins Schattenpasswort-Format.
	- »pwunconv« konvertiert zurück zu Nicht-Schatten-Passwörtern.
	- »pwck« prüft die Integrität von Passwort- und Schattendateien.
	- »lastlog« druckt die letzte Login-Zeit aller User.
	- »faillog« druckt den letzten fehlgeschlagenen Login-Versuch.
	- »useradd«, »userdel« und »usermod« dienen der Benutzerverwaltung.
	- »groupadd«, »groupdel« und »groupmod« dienen der Gruppenerwaltung.

Eine Reihe von Manual-Pages, die sich mit diesen Hilfsmitteln und 
Schattenpasswörtern im allgemeinen befassen, ist ebenfalls enthalten.

BEMERKUNG: Wer dieses Paket aus den Quellen selbst bauen will, sollte sich
an den Ersteller des Pakets wenden.

WICHTIG: Zur Zeit sollten Schatten-Passwörter nur kurzzeitig für Testzwecke
aktiviert werden. Es gibt noch zuviele Programme, die damit nicht klarkommen.


%prep
%setup -q -n shadow-%{version}
%patch0 -p1 -b .redhat
%patch1 -p1 -b .nscd
%patch2 -p1 -b .group
%patch3 -p1 -b .isascii
%patch4 -p1 -b .useradd
%patch5 -p1 -b .uid_min
%patch6 -p1 -b .mint
%patch7 -p1 -b .sparemint

cp /usr/lib/rpm/config.{guess,sub} .
aclocal
automake
autoconf


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
LIBS="-lintl -lsocket" \
./configure \
	--prefix=%{_prefix} \
	--disable-shared \
	--disable-desrpc \
	--with-libcrypt

make LIBS="-lintl -lsocket"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man \
	localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale

install -d -m 750 ${RPM_BUILD_ROOT}/etc/default
install -c -m 0644 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/login.defs
install -c -m 0600 %{SOURCE2} ${RPM_BUILD_ROOT}/etc/default/useradd

install -m644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/
install -m644 %{SOURCE4} ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/
install -m644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/
install -m644 %{SOURCE6} ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/

perl -pi -e "s/encrpted/encrypted/g" ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/newusers.8

# fix some things
mv ${RPM_BUILD_ROOT}/lib ${RPM_BUILD_ROOT}%{_prefix}/
cp ${RPM_BUILD_ROOT}/bin/login ${RPM_BUILD_ROOT}%{_prefix}/bin/
cp ${RPM_BUILD_ROOT}%{_prefix}/bin/passwd ${RPM_BUILD_ROOT}/bin/

strip ${RPM_BUILD_ROOT}/{bin,sbin}/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/{bin,sbin}/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

  
%files
%defattr(-,root,root)
%doc doc/ANNOUNCE doc/CHANGES doc/HOWTO
%doc doc/LICENSE doc/README doc/README.*
%dir /etc/default
%attr(0644,root,root)	%config /etc/login.defs
%attr(0600,root,root)	%config /etc/default/useradd

/bin/*
%{_prefix}/bin/*
%{_prefix}/lib/*
%{_prefix}/sbin/*
%{_prefix}/share/man/man*/*
%{_prefix}/share/man/pl/man*/*
%{_prefix}/share/locale/*/LC_MESSAGES/shadow.mo


%changelog
* Thu Sep 06 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 20000902

* Sun Dec 26 1999 Guido Flohr <guido@atari.org>
- Rebuilt against MiNTLib 0.54.1c.

* Thu Nov  4 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Rebuilt against developper MiNTLib.

* Sun Oct  3 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Initial release for Sparemint.
