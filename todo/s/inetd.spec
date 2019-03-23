Summary       : The inetd internet super daemon.
Name          : inetd
Version       : 0.17
Release       : 5
Copyright     : BSD
Group         : System Environment/Daemons

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/

Requires      : freemint-net portmap tcp_wrappers >= 7.6-3
BuildRequires : mintlib-devel >= 0.57.1

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-base-%{version}.tar.gz
Source1: inetd.conf
Source2: inetd.init
Source3: inetd.conf.5
Patch0: netkit-base-0.17-mint.patch


%description
This package include the inetd internet super daemon. All services
are disabled by default. To activate a service install first the
corresponding rpm and then edit /etc/inetd.conf and uncomment the
line for the service you want to run. Then restart your inetd either
by killing/starting or sending a SIGHUP signal.


%prep
%setup -q -n netkit-base-%{version}
%patch0 -p1 -b .mint


%build
chmod 755 configure
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
CXXFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
LIBS="-lsocket -liio" \
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

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

make install \
	INSTALLROOT=${RPM_BUILD_ROOT} \
	BINDIR=%{_prefix}/bin \
	MANDIR=%{_prefix}/share/man

install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/inetd.conf
install -m 755 %{SOURCE2} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/inetd
install -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5/

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
cat <<EOF
=================
!!! IMPORTANT !!!
=================
This inetd make use of user/group nobody. Please make sure that
the uid/gid of nobody is smaller than 32768. uid/gid values
of 32768 and higher are illegal and result in wrong behaviour.
EOF


%files
%defattr(-,root,root)
%config(noreplace) /etc/inetd.conf
/etc/rc.d/init.d/inetd
%{_prefix}/sbin/*
%{_prefix}/share/man/man*/*


%changelog
* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
