Summary: A graphical login program.
Name: nlogin
Version: 0.1.2
Release: 1
Copyright: GPL
Group: GEM/Login
Source: nlogin-%{version}.tar.gz
Buildroot: /var/tmp/nlogin-root
Packager: Guido Flohr <guido@atari.org>
Vendor: Sparemint
Prefix: %{_prefix}
Summary(de): Ein graphisches Login-Programm.

%description
The nlogin package provides a graphical login screen.  The program
is usually invoked by a corresponding entry in /etc/inittab
for the GEM runlevel.  It will ask the login information from
whoever wants to start a GEM session and then starts GEM with her
identity.

Please note that nlogin is still highly experimental. There are
quite a few packages and features that nlogin depends on that are
still missing.  You should contact the author of the package before
you attempt to install it.

Nlogin features tiled background ASCII graphics, kewl as can be.
Be the envy of every Linux user and install nlogin!

%description -l de
Das Paket nlogin enth‰lt einen graphischen Login-Bildschirm.  Das
Programm wird normalerweise durch einen entsprechenden Eintrag
in /etc/inittab f¸r den GEM-Runlevel gestartet.  Es fragt die
Login-Informationen ab und startet dann GEM mit der Identit‰t
der entsprechenden Benutzerin.

ACHTUNG: Nlogin ist noch sehr experimentell. Einige Pakete und
sonstige Dinge, die nlogin benˆtigt, fehlen noch. Vor einer 
Installation sollte man den Autor des Paketes kontaktieren.

Nlogin bietet natÅrlich auch gekachelte ASCII-Hintergrund-Grafiken.
Installieren Sie nlogin und jeder Linux-User wird vor Neid erblassen!

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make prefix=${RPM_BUILD_ROOT}%{_prefix} \
  mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man install
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS
%{_prefix}/bin/*
%{_prefix}/share/man/*/*
%{_prefix}/share/nlogin/*

%changelog
* Sun Dec 27 1999 Guido Flohr <guido@atari.org>
- Yet another release, update to 0.1.2 to fix the priority problem.

* Sun Dec 26 1999 Guido Flohr <guido@atari.org>
- Initial release for Sparemint.
