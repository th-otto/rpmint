Summary: The System V system initialization program.
Name: mintinit
%define version 0.1.1
Version: %{version}
Release: 1
Copyright: GPL
Group: System Environment/Base
Source: mintinit-%{version}.tar.gz
Buildroot: /var/tmp/init-root
Packager: Guido Flohr <guido@atari.org>
Vendor: Sparemint
Summary(de): Das System-V Initialisierungs-Programm.

%description
The mintinit package contains a group of programs that
control the very basic functions of your system. Mintinit is
the first program started by the FreeMiNT kernel when the
system boots, controlling the startup, running and shutdown
of all other programs.

Please note that mintinit is still highly experimental. There are
quite a few packages and features that mintinit depends on that are
still missing.  You should contact the author of the package before
you attempt to install it.

%description -l de
Das Paket mintinit enthält eine Gruppe von Programmen, die 
grundlegende Systemfunktionen steuern. Mintinit ist das erste
Programm, das vom FreeMiNT-Kernel nach dem Booten gestartet
wird, und kontrolliert die Startsequenz, den Ablauf und die
Beendigung aller anderen Programme.

ACHTUNG: Mintinit ist noch sehr experimentell. Einige Pakete und
sonstige Dinge, die mintint benötigt, fehlen noch. Vor einer 
Installation sollte man den Autor des Paketes kontaktieren.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT/usr mandir=$RPM_BUILD_ROOT/usr/share/man \
  sbindir=$RPM_BUILD_ROOT/sbin install
echo ".so man1/last.1.gz" >$RPM_BUILD_ROOT/usr/share/man/man1/lastb.1
echo ".so man8/halt.8.gz" >$RPM_BUILD_ROOT/usr/share/man/man1/poweroff.8
echo ".so man8/halt.8.gz" >$RPM_BUILD_ROOT/usr/share/man/man1/reboot.8
gzip -9nf $RPM_BUILD_ROOT/usr/share/man/*/*
strip $RPM_BUILD_ROOT/usr/bin/* $RPM_BUILD_ROOT/sbin/* || :

%post
[ -e /var/run/initrunlvl ] && ln -s ../var/run/initrunlvl /etc/initrunlvl
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS
/sbin/halt
/sbin/init
/sbin/killall5
/sbin/pidof
/sbin/poweroff
/sbin/reboot
/sbin/runlevel
/sbin/shutdown
/sbin/sulogin
/sbin/telinit

/usr/bin/last
/usr/bin/lastb
/usr/bin/mesg
/usr/bin/utmpdump
%attr(2555,root,tty)  /usr/bin/wall
/usr/share/man/*/*
#/etc/initrunlvl
#/dev/initctl

%changelog
* Sun Dec 26 1999 Guido Flohr <guido@atari.org>
- Initial release for Sparemint.
