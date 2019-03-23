Summary:	OpenSSH free Secure Shell (SSH) implementation
Name:		openssh
Version:	5.6p1
Release:	2
Copyright:	BSD
Group:		Applications/Internet
Packager:	Keith Scroggins <kws@radix.net>
Vendor:		Sparemint
URL:		http://www.openssh.com/
Obsoletes:	ssh
Requires:	openssl >= 0.9.8k
Buildrequires:	perl, openssl-devel >= 0.9.8k, mintlib-devel >= 0.57.1-1, sharutils, zlib-devel >= 1.2.3

Prefix:		%{_prefix}
Docdir:		%{_prefix}/doc
BuildRoot:	%{_tmppath}/%{name}-root

Source:		ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Patch0:		openssh-3.7.1p2-mint.patch
Patch1:		openssh-5.6p1-mint.patch

%package clients
Summary:	OpenSSH Secure Shell protocol clients
Requires:	openssh = %{version}-%{release}
Group:		Applications/Internet
Obsoletes:	ssh-clients

%package server
Summary:	OpenSSH Secure Shell protocol server (sshd)
Group:		System Environment/Daemons
Obsoletes:	ssh-server
Requires:	openssh = %{version}-%{release}, chkconfig >= 0.9, initscripts

%description
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package includes the core files necessary for both the OpenSSH
client and server.  To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package includes the clients necessary to make encrypted connections
to SSH servers.

%description server
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package contains the secure shell daemon. The sshd is the server 
part of the secure shell protocol and allows ssh clients to connect to 
your host.

%prep

%setup -q
%patch0 -p1
%patch1 -p1

%build

CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=/etc/ssh \
	--mandir=%{_prefix}/share/man \
	--libexecdir=%{_prefix}/libexec/openssh \
	--with-ipv4-default \
	--with-default-path=/usr/local/bin:/bin:/usr/bin
ln -s /usr/bin/strip .

make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf "${RPM_BUILD_ROOT}"

make install \
	DESTDIR="${RPM_BUILD_ROOT}"

install -m755 -d "${RPM_BUILD_ROOT}"/etc/rc.d/init.d
install -m755 contrib/redhat/sshd.init "${RPM_BUILD_ROOT}"/etc/rc.d/init.d/sshd

find "${RPM_BUILD_ROOT}"%{_prefix}/share/man -type f -print0 | xargs -0 gzip -9
rm -f "${RPM_BUILD_ROOT}"%{_prefix}/share/man/man1/slogin.1 && \
	ln -s ssh.1.gz "${RPM_BUILD_ROOT}"%{_prefix}/share/man/man1/slogin.1.gz

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf "${RPM_BUILD_ROOT}"

%pre server
install -m755 -d /var/chroot/sshd
install -m755 -d /var/empty
grep "^sshd:" /etc/passwd >/dev/null
if [ $? -ne 0 ]
then
	useradd -r -c "& pseudo-user" -d /var/chroot/sshd -M -s /bin/false sshd
fi

%preun server
#userdel sshd

%files
%defattr(-,root,root)
%doc ChangeLog OVERVIEW README* INSTALL 
%doc CREDITS LICENCE TODO RFC.nroff
%attr(0755,root,root) %{_prefix}/bin/ssh-keygen
%attr(0755,root,root) %{_prefix}/bin/ssh-keyscan
%attr(0755,root,root) %{_prefix}/bin/scp
%attr(0644,root,root) %{_prefix}/share/man/man1/ssh-keygen.1*
%attr(0644,root,root) %{_prefix}/share/man/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_prefix}/share/man/man1/scp.1*
%attr(0755,root,root) %dir /etc/ssh
%attr(0600,root,root) %config(noreplace) /etc/ssh/moduli
%attr(0755,root,root) %dir %{_prefix}/libexec/openssh

%files clients
%defattr(-,root,root)
%attr(4755,root,root) %{_prefix}/bin/ssh
%attr(0755,root,root) %{_prefix}/bin/ssh-agent
%attr(0755,root,root) %{_prefix}/bin/ssh-add
%attr(0755,root,root) %{_prefix}/bin/sftp
%attr(0644,root,root) %{_prefix}/share/man/man1/ssh.1*
%attr(0644,root,root) %{_prefix}/share/man/man1/ssh-agent.1*
%attr(0644,root,root) %{_prefix}/share/man/man1/ssh-add.1*
%attr(0644,root,root) %{_prefix}/share/man/man1/sftp.1*
%attr(0644,root,root) %config(noreplace) /etc/ssh/ssh_config
%attr(-,root,root) %{_prefix}/bin/slogin
%attr(-,root,root) %{_prefix}/share/man/man1/slogin.1*

%files server
%defattr(-,root,root)
%attr(0755,root,root) %{_prefix}/sbin/sshd
%attr(0755,root,root) %{_prefix}/libexec/openssh/sftp-server
%attr(0644,root,root) %{_prefix}/share/man/man8/sshd.8*
%attr(0644,root,root) %{_prefix}/share/man/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) /etc/ssh/sshd_config
%attr(0755,root,root) %config /etc/rc.d/init.d/sshd

%changelog
* Thu Dec 09 2010 Keith Scroggins <kws@radix.net>
- Compiled against latest (1.0.0c) OpenSSL

* Mon Dec 06 2010 Keith Scroggins <kws@radix.net>
- Updated to latest version of OpenSSH and fixed problem with pkcs11 in 
- ssh-keygen

* Sun May 13 2010 Keith Scroggins <kws@radix.net>
- Latest version of SSH with latest SSL and MiNTLib

* Mon May 11 2009 Keith Scroggins <kws@radix.net>
- Latest version of SSH with latest SSL and MiNTLib

* Mon Mar 02 2009 Keith Scroggins <kws@radix.net>
- Latest version of SSH with latest SSL and MiNTLib

* Fri Mar 18 2004 Keith Scroggins <kws@radix.net>
- Compiled against latest MintLibs and latest fixed OpenSSL

* Tue Dec 16 2003 Frank Naumann <fnaumann@freemint.de>
- disabled privilege seperation, don't work yet under freemint

* Tue Dec 16 2003 Frank Naumann <fnaumann@freemint.de>
- create sshd user, needed for privilege seperation

* Tue Oct 21 2003 Keith Scroggins <kws@radix.net>
- Updated to version 3.7.1p2

* Sun Jun 9 2002 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- Replaced sockaddr_un-patch with the more suitable AF_UNIX-patch

* Sat Jun 8 2002 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- Removed COPYING.Ylonen from %doc, as it no longer exists

* Sun Jun 2 2002 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- Updated to OpenSSH 3.2.3p1
- Added new patch to avoid strange linker error concerning optind
  (better than using -D_AVOID_GPL)

* Sat Mar 16 2002 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- Updated to OpenSSH 3.1p1
- Re-integrate setrlimit-patch to make ssh-agent work again

* Mon Apr 28 2001 Frank Naumann <fnaumann@freemint.de>
- added ssh-keyscan program, require a fixed MiNTNet to
  run correctly

* Thu Apr 24 2001 Frank Naumann <fnaumann@freemint.de>
- added missing xkeys patch
- fixed recursive copy problem with scp

* Wed Apr 23 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.9p1, compiled with current MiNTLib that include
  the select patch

* Fri Apr 20 2001 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- Updated to OpenSSH 2.5.2p2

* Sat Dec 30 2000 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- Fixed `Buildrequires' to contain mintlib-devel rather than mintlib
- sshd will now pass $UNIXMODE and $PCONVERT to its childs
- sshd now expects login to be /bin/login

* Sun Dec 3 2000 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- Initial release for Sparemint, based on Damien Miller's <djm@ibs.com.au>
  spec-file found in openssh-2.3.0p1/contrib/redhat
