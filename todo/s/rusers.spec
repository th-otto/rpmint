Summary       : Displays the users logged into machines on the local network.
Name          : rusers
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

Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rusers-%{version}.tar.gz
Source1: rusersd.init
Source2: rstatd.tar.gz
Source3: rstatd.init
Patch0:  netkit-rusers-0.15-numusers.patch
Patch1:  netkit-rusers-0.17-mint.patch
Patch2:  netkit-rusers-0.17-install.patch


%description
The rusers program allows users to find out who is logged into various
machines on the local network.  The rusers command produces output
similar to who, but for the specified list of hosts or for all
machines on the local network.

Install rusers if you need to keep track of who is logged into your
local network.

%package server
Summary       : Server for the rusers protocol.
Group         : System Environment/Daemons
Prereq        : /sbin/chkconfig
Requires      : portmap

%description server
The rusers program allows users to find out who is logged into various
machines on the local network.  The rusers command produces output
similar to who, but for the specified list of hosts or for all
machines on the local network. The rusers-server package contains the
server for responding to rusers requests.

Install rusers-server if you want remote users to be able to see
who is logged into your machine.


%prep
%setup -q -n netkit-rusers-%{version} -a 2
%patch0 -p1 -b .numusers
%patch1 -p1 -b .mint
%patch2 -p1 -b .install


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE -D_NO_UT_TIME" \
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
make -C rpc.rstatd


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

make INSTALLROOT=${RPM_BUILD_ROOT} install
make INSTALLROOT=${RPM_BUILD_ROOT} install -C rpc.rstatd

install -m 755 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/rusersd
install -m 755 %{SOURCE3} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/rstatd

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
/sbin/chkconfig --add rusersd
/sbin/chkconfig --add rstatd

%preun server
if [ $1 = 0 ]; then
    /sbin/chkconfig --del rusersd
    /sbin/chkconfig --del rstatd
fi


%files
%defattr(-,root,root)
%{_prefix}/bin/rup
%{_prefix}/bin/rusers
%{_prefix}/share/man/man1/*

%files server
%defattr(-,root,root)
%config /etc/rc.d/init.d/rusersd
%config /etc/rc.d/init.d/rstatd
%{_prefix}/share/man/man8/*
%{_prefix}/sbin/rpc.rstatd
%{_prefix}/sbin/rpc.rusersd


%changelog
* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
