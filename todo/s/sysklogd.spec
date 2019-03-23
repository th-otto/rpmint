Summary       : MiNT system logger
Summary(de)   : MiNT System-Logger
Name          : sysklogd
Version       : 1.3
Release       : 5
Copyright     : GPL
Group         : System Environment/Daemons

Packager      : Guido Flohr <guido@freemint.de>
Vendor        : Sparemint

Prereq        : fileutils, /sbin/chkconfig
Requires      : logrotate

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://sunsite.unc.edu/pub/Linux/system/daemons/sysklogd-1.3.tar.gz
Source1: syslog.conf.rhs
Source2: syslog.init
Source3: syslog.log
Patch0: sysklogd-1.3-pl1.patch
Patch1: sysklogd-1.3-pl2.patch
Patch2: sysklogd-1.3-pl3.patch
Patch3: sysklogd-1.3-make.patch
Patch4: sysklogd-1.3-glibc.patch
Patch5: sysklogd-1.3-getutent.patch
Patch6: sysklogd-1.3-kernel21.patch
Patch7: sysklogd-1.3-exit.patch
Patch8: sysklogd-1.3-rh.patch
Patch9: sysklogd-1.3-utmp-process.patch
Patch10: sysklogd-1.3-jbj.patch
Patch11: sysklogd-mint.patch
Patch12: sysklogd-1.3-mint.patch


%description
This is the MiNT system (and not yet kernel) logging program.  It is run
as a daemon (background process) to log messages to different
places.  These are usually things like sendmail logs, security
logs, and errors from other daemons.

%description -l de
Dies ist das MiNT System- (und noch nicht Kernel-) Logging-Programm. Es
wird als ein D„mon (Hintergrundprozess) gestartet, um Nachrichten an
verschiedenen Stellen zu protokollieren.  Dies sind normalerweise Dinge
wie Sendmail-Logs, Sicherheits-Logs und Fehler anderer D„monen.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p2
%patch3 -p1
%patch5 -p1 -b .getutent
%patch4 -p1 -b .noglibc
%patch6 -p1 -b .broken
%patch7 -p1 -b .exit
%patch8 -p1 -b .rh
%patch9 -p1 -b .utmp
%patch10 -p1 -b .jbj
%patch11 -p1 -b .mint
%patch12 -p1 -b .mint


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

make install \
	TOPDIR=${RPM_BUILD_ROOT} \
	MANDIR=${RPM_BUILD_ROOT}%{_prefix}/share/man \
	MAN_GROUP=wheel

install -m644 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/syslog.conf

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
install -m755 %{SOURCE2} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/syslog
mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m644 %{SOURCE3} ${RPM_BUILD_ROOT}/etc/logrotate.d/syslog

chmod 755 ${RPM_BUILD_ROOT}%{_prefix}/sbin/syslogd

strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# fixup manpages
cd ${RPM_BUILD_ROOT} echo ".so man8/sysklogd.8.gz" >${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/syslogd.8

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
for n in /var/log/messages /var/log/secure /var/log/maillog /var/log/spooler ; do
  [ -f $n ] && continue
  touch $n
  chmod 600 $n
done
/sbin/chkconfig --add syslog

%preun
if [ $1 = 0 ]; then
  /sbin/chkconfig --del syslog
fi


%files
%defattr(-,root,root)
%doc ANNOUNCE README* NEWS INSTALL Sysklogd-1.3.lsm
%config /etc/syslog.conf
%config /etc/logrotate.d/syslog
%config /etc/rc.d/init.d/syslog
%{_prefix}/sbin/syslogd
%{_prefix}/share/man/man5/syslog.conf.5.gz
%{_prefix}/share/man/man8/syslogd.8.gz
%{_prefix}/share/man/man8/sysklogd.8.gz


%changelog
* Fri Jan 30 2004 Mark Duckworth <mduckworth@atari-source.com>
- Rebuild against MiNTLib 0.57.4

* Sat Sep 29 2001 Frank Naumann <fnaumann@freemint.de>
- Rebuild against MiNTLib 0.57.1 

* Mon Apr 3 2000 Guido Flohr <guido@freemint.de>
- Rebuild against MiNTLib 0.55.  This will hopefully fix the 
  "/pipe/log: file not found" bug.
  
* Mon Dec 20 1999 Guido Flohr <guido@freemint.de>
- Rebuild against MiNTLib 0.54.1c.
- Several fixes to meet MiNT requirements.

* Sun Oct 17 1999 Guido Flohr <guido@freemint.de>
- First Sparemint version.
- Added German description/summary.
- Compressed manpages.
