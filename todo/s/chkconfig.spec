Summary: A system tool for maintaining the /etc/rc.d hierarchy.
Name: chkconfig
%define version 1.0.7
Version: %{version}
Release: 2
Copyright: GPL
Group: System Environment/Base
Source: ftp://ftp.redhat.com/pub/redhat/code/chkconfig/chkconfig-%{version}.tar.gz
Patch0: chkconfig-nommap.patch
Patch1: chkconfig-mint.patch
BuildRoot: /var/tmp/chkconfig.root
Packager: Guido Flohr <guido@atari.org>
Vendor: Sparemint
Summary(de): Ein System-Werkzeug zur Pflege der /etc/rc.d-Hierarchie.

%description
Chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  Chkconfig manipulates the numerous
symbolic links in /etc/rc.d, so system administrators don't have to
manually edit the symbolic links as often.

%description -l de
Chkconfig ist ein Basis-System-Werkzeug. Es aktualisiert und überprüft
die Runlevel-Informationen für die System-Dienste. Chkconfig manipuliert
die diversen Links in /etc/rc.d, so dass SysAdmins diese Links nicht
ständig von Hand anlegen und löschen müssen.

%package -n ntsysv
Summary: A system tool for maintaining the /etc/rc.d hierarchy.
Group: System Environment/Base

%description -n ntsysv
ntsysv updates and queries runlevel information for system
services.  ntsysv relieves system administrators of having to
directly manipulate the numerous symbolic links in /etc/rc.d.

%description -n ntsysv -l de
Ntsysv aktualisiert und ermittelt Runlevel-Informationen für 
System-Services. Ntsysv nimmt System-Administratoren die Mühe ab, 
die zahlreichen symbolischen Links in /etc/rc.d direkt zu manipulieren.

%prep
%setup -q
%patch0 -p1 -b .nommap
%patch1 -p1 -b .mint
%build

%ifarch sparc
LIBMHACK=-lm
%endif
%ifarch m68kmint
LIBS=-lintl
%endif

make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" LIBS="$LIBS" LIBMHACK="$LIBMHACK"

%install
rm -rf $RPM_BUILD_ROOT
make instroot=$RPM_BUILD_ROOT MANDIR=/usr/share/man install

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
for n in 0 1 2 3 4 5 6; do
    mkdir -p $RPM_BUILD_ROOT/etc/rc.d/rc${n}.d
done
gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man8/*.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/sbin/chkconfig
/usr/share/man/man8/chkconfig.8.gz
%dir /etc/rc.d
%dir /etc/rc.d/*
/usr/share/locale/*/LC_MESSAGES/chkconfig.mo

%files -n ntsysv
%defattr(-,root,root)
/usr/sbin/ntsysv
/usr/share/man/man8/ntsysv.8.gz

%changelog
* Sun Dec 26 1999 Guido Flohr <guido@atari.org>
- Built against fixed libnewt to support monochrome terminals.

* Tue Dec 14 1999 Guido Flohr <guido@atari.org>
- Rebuild against MiNTLib 0.54.1c.
- Changed manpath to /usr/share/man.

* Sun Sep 19 1999 Guido Flohr <guido@atari.org>
- Initial release for Sparemint.

* Mon Aug 23 1999 Jeff Johnson <jbj@redhat.com>
- don't use strchr to skip unwanted files, look at extension instead (#4166).

* Thu Aug  5 1999 Bill Nottingham <notting@redhat.com>
- fix --help, --verson

* Mon Aug  2 1999 Matt Wilson <msw@redhat.com>
- rebuilt ntsysv against newt 0.50

* Mon Aug  2 1999 Jeff Johnson <jbj@redhat.com>
- fix i18n problem in usage message (#4233).
- add --help and --version.

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- release for Red Hat 6.0

* Thu Apr  8 1999 Matt Wilson <msw@redhat.com>
- added support for a "hide: true" tag in initscripts that will make
  services not appear in ntsysv when run with the "--hide" flag

* Thu Apr  1 1999 Matt Wilson <msw@redhat.com>
- added --hide flag for ntsysv that allows you to hide a service from the
  user.

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- fix glob, once and for all. Really. We mean it.

* Thu Mar 18 1999 Bill Nottingham <notting@redhat.com>
- revert fix for services@levels, it's broken
- change default to only edit the current runlevel

* Mon Mar 15 1999 Bill Nottingham <notting@redhat.com>
- don't remove scripts that don't support chkconfig

* Tue Mar 09 1999 Erik Troan <ewt@redhat.com>
- made glob a bit more specific so xinetd and inetd don't cause improper matches

* Thu Feb 18 1999 Matt Wilson <msw@redhat.com>
- removed debugging output when starting ntsysv

* Thu Feb 18 1999 Preston Brown <pbrown@redhat.com>
- fixed globbing error
- fixed ntsysv running services not at their specified levels.

* Tue Feb 16 1999 Matt Wilson <msw@redhat.com>
- print the value of errno on glob failures.

* Sun Jan 10 1999 Matt Wilson <msw@redhat.com>
- rebuilt for newt 0.40 (ntsysv)

* Tue Dec 15 1998 Jeff Johnson <jbj@redhat.com>
- add ru.po.

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- translation updates

* Thu Oct 08 1998 Cristian Gafton <gafton@redhat.com>
- updated czech translation (and use cs instead of cz)

* Tue Sep 22 1998 Arnaldo Carvalho de Melo <acme@conectiva.com.br>
- added pt_BR translations
- added more translatable strings
- support for i18n init.d scripts description

* Sun Aug 02 1998 Erik Troan <ewt@redhat.com>
- built against newt 0.30
- split ntsysv into a separate package

* Thu May 07 1998 Erik Troan <ewt@redhat.com>
- added numerous translations

* Mon Mar 23 1998 Erik Troan <ewt@redhat.com>
- added i18n support

* Sun Mar 22 1998 Erik Troan <ewt@redhat.com>
- added --back
