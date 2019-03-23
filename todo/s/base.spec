Summary       : A set of system configuration and setup files.
Name          : base
Version       : 1.4
Release       : 2
License       : public domain
Group         : System Environment/Base

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Provides      : netbase
Requires      : bash >= 2.05-5

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: base-%{version}.tar.gz


%description
The setup package contains a set of important system configuration and
setup files, such as passwd, group, and profile.

%prep
%setup -q


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc
cp -ar * ${RPM_BUILD_ROOT}/etc

mkdir -p ${RPM_BUILD_ROOT}/var/adm
mkdir -p ${RPM_BUILD_ROOT}/var/log

cat /dev/null > ${RPM_BUILD_ROOT}/var/adm/wtmp
cat /dev/null > ${RPM_BUILD_ROOT}/var/log/wtmp
cat /dev/null > ${RPM_BUILD_ROOT}/var/log/lastlog

cat /dev/null > ${RPM_BUILD_ROOT}/etc/mnttab
chmod 644 ${RPM_BUILD_ROOT}/etc/mnttab

#touch ${RPM_BUILD_ROOT}/etc/{shadow,gshadow}
#chmod 0400 ${RPM_BUILD_ROOT}/etc/{shadow,gshadow}


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%pre
mkdir -p /etc/profile.d
mkdir -p /etc/sysconfig


%files
%defattr(-,root,root)

# non config stuff
%config /etc/inputrc
%config /etc/services
%config /etc/protocols
%config /etc/rpc

# user/group stuff
%verify(not md5 size mtime) %config(noreplace) /etc/passwd
%verify(not md5 size mtime) %config(noreplace) /etc/group
#%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/shadow
#%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/gshadow
#%attr(0600,root,root) %config(missingok) /etc/securetty

# network
%config(noreplace) %verify(not md5 size mtime) /etc/exports
%config(noreplace)                             /etc/host.conf
%config(noreplace) %verify(not md5 size mtime) /etc/hosts
%config(noreplace) %verify(not md5 size mtime) /etc/hosts.allow
%config(noreplace) %verify(not md5 size mtime) /etc/hosts.deny
%config            %verify(not md5 size mtime) /etc/motd
%config(noreplace) %verify(not md5 size mtime) /etc/networks
%config(noreplace) %verify(not md5 size mtime) /etc/resolv.conf
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/hostname
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/domainname
# symbolic links for backward compatibility
/etc/hostname
/etc/domainname

# shell configuration
%config /etc/bashrc
%config /etc/profile
%config /etc/csh.cshrc
%config /etc/csh.login
%config /etc/csh.logout
%config /etc/skel/.[A-Za-z0-9]*

# misc
%config(noreplace)                             /etc/filesystems
%config(noreplace) %verify(not md5 size mtime) /etc/fstab
                                               /etc/fstab.sample
%config(noreplace)                             /etc/printcap
%config(noreplace) %verify(not md5 size mtime) /etc/mnttab
%config(noreplace) %verify(not md5 size mtime) /etc/rpmrc
%config(noreplace) %verify(not md5 size mtime) /etc/shells
%config(noreplace) %verify(not md5 size mtime) /var/adm/wtmp
%config(noreplace) %verify(not md5 size mtime) /var/log/wtmp
%config(noreplace) %verify(not md5 size mtime) /var/log/lastlog


%changelog
* Mon Apr 28 2003 Marc-Anton Kehr <m.kehr@ndh.net>
- removed nameserver in r/etc/resolv.conf

* Tue Mar 05 2002 Frank Naumann <fnaumann@freemint.de>
- updated to 1.4

* Wed Nov 14 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.3

* Fri Nov 02 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.2
- new /etc/skel subdir, new /etc/networks

* Fri Oct 12 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.1; fixed /etc/profile (missing default $PATH)
- requires now rpm 3.0.6 (old rpm version is doesn't recognize provides option)

* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
