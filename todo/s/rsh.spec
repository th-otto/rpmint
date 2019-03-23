Summary       : Clients for remote access commands (rsh, rlogin, rcp).
Name          : rsh
Version       : 0.17
Release       : 2
Copyright     : BSD
Group         : Applications/Internet

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/

Requires      : freemint-net netbase
BuildRequires : mintlib-devel >= 0.57.1

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rsh-%{version}.tar.gz
Patch0: netkit-rsh-0.10-sectty.patch
Patch1: netkit-rsh-0.10-stdarg.patch
Patch2: netkit-rsh-0.16-jbj.patch
Patch3: netkit-rsh-0.16-jbj4.patch
Patch4: netkit-rsh-0.16-rlogin=rsh.patch
Patch5: netkit-rsh-0.16-nokrb.patch
Patch6: netkit-rsh-0.17-pre20000412-jbj5.patch
Patch7: netkit-rsh-0.17-mint.patch


%description
The rsh package contains a set of programs which allow users to run
commmands on remote machines, login to other machines and copy files
between machines (rsh, rlogin and rcp).  All three of these commands
use rhosts style authentication.  This package contains the clients
needed for all of these services.
The rsh package should be installed to enable remote access to other
machines.

%package server
Summary       : Servers for remote access commands (rsh, rlogin, rcp).
Group         : System Environment/Daemons
Requires      : inetd

%description server
The rsh-server package contains a set of programs which allow users
to run commmands on remote machines, login to other machines and copy
files between machines (rsh, rlogin and rcp).  All three of these
commands use rhosts style authentication.  This package contains the
servers needed for all of these services.  It also contains a server
for rexec, an alternate method of executing remote commands.
All of these servers are run by inetd and configured using
/etc/inetd.conf. All services are disabled by default.

The rsh-server package should be installed to enable remote access
from other machines.


%prep
%setup -q -n netkit-rsh-%{version}
%patch0 -p1 -b .sectty
%patch1 -p1 -b .stdarg
%patch2 -p1 -b .jbj
%patch3 -p1 -b .jbj4
%patch4 -p1 -b .rsh
%patch5 -p1 -b .rsh.nokrb
%patch6 -p1 -b .jbj5
%patch7 -p1 -b .mint


%build
chmod 755 configure
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
CXXFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
LIBS="-lsocket" \
./configure

perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS),;
    s,^BINDIR=.*$,BINDIR=%{_prefix}/bin,;
    s,^MANDIR=.*$,MANDIR=%{_prefix}/share/man,;
    s,^SBINDIR=.*$,SBINDIR=%{_prefix}/sbin,;
    ' MCONFIG

make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

make install \
	INSTALLROOT=${RPM_BUILD_ROOT} \
	BINDIR=%{_prefix}/bin \
	MANDIR=%{_prefix}/share/man

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:

# fix symlinks
( cd ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8;
  for file in *.8; do \
    echo "processing $file ..."; \
    target=`readlink $file`; \
    ln -s $target.gz $file.gz; \
    rm $file; \
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%attr(4755,root,root) %{_prefix}/bin/rcp
#%{_prefix}/bin/rexec
%attr(4755,root,root) %{_prefix}/bin/rlogin
%attr(4755,root,root) %{_prefix}/bin/rsh
%{_prefix}/share/man/man1/*.1*

%files server
%defattr(-,root,root)
%{_prefix}/sbin/in.rexecd
#%{_prefix}/sbin/in.rlogind
%{_prefix}/sbin/in.rshd
%{_prefix}/share/man/man8/*.8*


%changelog
* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
