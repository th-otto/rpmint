Summary       : Displays who is logged in to local network machines.
Name          : rwho
Version       : 0.17
Release       : 4
License       : BSD
Group         : System Environment/Daemons

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/

Requires      : /sbin/chkconfig freemint-net netbase
BuildRequires : mintlib-devel >= 0.57.1

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rwho-%{version}.tar.gz
Source1: rwhod.init
Patch0:  netkit-rwho-0.15-alpha.patch
Patch1:  netkit-rwho-0.17-mint.patch
Patch2:  netkit-rwho-0.17-install.patch


%description
The rwho command displays output similar to the output of the who
command (it shows who is logged in) for all machines on the local
network running the rwho daemon.

Install the rwho command if you need to keep track of the users who
are logged in to your local network.


%prep
%setup -q -n netkit-rwho-%{version}
%patch0 -p1 -b .alpha
%patch1 -p1 -b .mint
%patch2 -p1 -b .install


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
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}/var/spool/rwho

make INSTALLROOT=${RPM_BUILD_ROOT} install
make INSTALLROOT=${RPM_BUILD_ROOT} install -C ruptime

install -m 755 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/rwhod

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


%post
/sbin/chkconfig --add rwhod

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del rwhod
fi


%files
%defattr(-,root,root)
%config /etc/rc.d/init.d/rwhod
%{_prefix}/bin/ruptime
%{_prefix}/bin/rwho
%{_prefix}/sbin/rwhod
%{_prefix}/share/man/man1/ruptime.1*
%{_prefix}/share/man/man1/rwho.1*
%{_prefix}/share/man/man8/rwhod.8*
/var/spool/rwho


%changelog
* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
