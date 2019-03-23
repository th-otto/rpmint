Summary       : The finger client.
Name          : finger
Version       : 0.17
Release       : 1
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

Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/bsd-finger-%{version}.tar.gz
Source1: finger-strftime.c
Patch0:  bsd-finger-0.16-pts.patch
Patch1:  bsd-finger-0.17-exact.patch
Patch2:  bsd-finger-0.16-allocbroken.patch
Patch3:  bsd-finger-0.17-rfc742.patch
Patch4:  bsd-finger-0.17-mint.patch
Patch5:  bsd-finger-0.17-install.patch
Patch6:  bsd-finger-0.17-strftime.patch


%description
Finger is a utility which allows users to see information about system
users (login name, home directory, name, how long they've been logged
in to the system, etc.).  The finger package includes a standard
finger client.

You should install finger if you'd like to retrieve finger information
from other systems.

%package server
Summary       : The finger daemon.
Group         : System Environment/Daemons
Requires      : inetd

%description server
Finger is a utility which allows users to see information about system
users (login name, home directory, name, how long they've been logged
in to the system, etc.).  The finger-server package includes a standard
finger server. The server daemon (fingerd) runs from /etc/inetd.conf,
which must be modified to disable finger requests.

You should install finger-server if your system is used by multiple users
and you'd like finger information to be available.


%prep
%setup -q -n bsd-finger-%{version}
%patch0 -p1 -b .pts
%patch1 -p1 -b .exact
%patch2 -p1 -b .allocbroken
%patch3 -p1 -b .rfc742
%patch4 -p1 -b .mint
%patch5 -p1 -b .install
%patch6 -p1 -b .strftime
cp %{SOURCE1} finger/


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
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin

make INSTALLROOT=${RPM_BUILD_ROOT} install

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%attr(0711,root,root) %{_prefix}/bin/finger
%{_prefix}/share/man/man1/finger.1*

%files server
%defattr(-,root,root)
%attr(0711,root,root) %{_prefix}/sbin/in.fingerd
%{_prefix}/share/man/man8/in.fingerd.8*
%{_prefix}/share/man/man8/fingerd.8*


%changelog
* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
