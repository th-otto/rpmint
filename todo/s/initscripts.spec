Summary       : Some simple init scripts.
Name          : initscripts
Version       : 1.3
Release       : 2
License       : GPL
Group         : System Environment/Base

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Requires      : bash >= 2.05-5, psmisc

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: initscripts-%{version}.tar.gz


%description
This package include some simple startup scripts and configuration
files for Sparemint.

Attention: If you already have initscripts and configuration stuff
           for example copied from old KGMD distribution be careful
           if you install this rpm. It's your own responsibility
           that you don't get into trouble or conflicts.


%prep
%setup -q


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc
cp -ar * ${RPM_BUILD_ROOT}/etc

mkdir -p ${RPM_BUILD_ROOT}/sbin
mv ${RPM_BUILD_ROOT}/etc/initlog ${RPM_BUILD_ROOT}/sbin


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)

# symbolic links for backward compatibility
/etc/rc
/etc/rc.single

# non config stuff
/etc/sparemint-release
/sbin/initlog

# sysV stuff
/etc/rc.d/init.d/*
/etc/init.d

# simple startup scripts
/etc/rc.d/rc
/etc/rc.d/rc.local
/etc/rc.d/rc.net
/etc/rc.d/rc.nfs
/etc/rc.d/rc.single

# configuration files
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/add.services
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/clock
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/config.if
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/defaultroute
                                               /etc/sysconfig/init
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/net.services
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/network
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/std.services


%changelog
* Wed Aug 11 2004 Frank Naumann <fnaumann@freemint.de>
- setting up owner/group/permissions specified in /etc/fstab

* Tue Dec 16 2003 Frank Naumann <fnaumann@freemint.de>
- Corrected wrong english

* Wed Nov 14 2001 Frank Naumann <fnaumann@freemint.de>
- first release for sparemint
