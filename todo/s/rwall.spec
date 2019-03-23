Summary       : Client for sending messages to a host's logged in users.
Name          : rwall
Version       : 0.17
Release       : 2
Copyright     : BSD
Group         : System Environment/Daemons

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/

Requires      : freemint-net netbase
BuildRequires : mintlib-devel >= 0.57.1

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rwall-%{version}.tar.gz
Source1: rwalld.init
Patch1:  netkit-rwalld-0.10-banner.patch
Patch2:  netkit-rwall-0.17-mint.patch
Patch3:  netkit-rwall-0.17-install.patch


%description
The rwall command sends a message to all of the users logged into a
specified host.  Actually, your machine's rwall client sends the
message to the rwall daemon running on the specified host, and the
rwall daemon relays the message to all of the users logged in to that
host.

Install rwall if you'd like the ability to send messages to users
logged in to a specified host machine.

%package server
Summary       : Server for sending messages to a host's logged in users.
Group         : System Environment/Daemons
Prereq        : /sbin/chkconfig
Requires      : portmap

%description server
The rwall command sends a message to all of the users logged into
a specified host.  The rwall-server package contains the daemon for
receiving such messages, and is disabled by default on Red Hat Linux
systems (it can be very annoying to keep getting all those messages
when you're trying to play Quake--I mean, trying to get some work done).

Install rwall-server if you'd like the ability to receive messages
from users on remote hosts.


%prep
%setup -q -n netkit-rwall-%{version}
%patch1 -p1 -b .banner
%patch2 -p1 -b .mint
%patch3 -p1 -b .install


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
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
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d

make INSTALLROOT=${RPM_BUILD_ROOT} install
install -m 755 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/rwalld

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


%post server
/sbin/chkconfig --add rwalld

%preun server
if [ $1 = 0 ]; then
    /sbin/chkconfig --del rwalld
fi


%files
%defattr(-,root,root)
%{_prefix}/bin/rwall
%{_prefix}/share/man/man1/rwall.1*

%files server
%defattr(-,root,root)
%config /etc/rc.d/init.d/rwalld
%{_prefix}/sbin/rpc.rwalld
%{_prefix}/share/man/man8/rpc.rwalld.8*
%{_prefix}/share/man/man8/rwalld.8*


%changelog
* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
