Summary       : A DHCP (Dynamic Host Configuration Protocol) server and relay agent.
Name          : dhcp
Version       : 3.1.ESV
Release       : 1
Copyright     : distributable
Group         : System Environment/Daemons

Packager      : Standa Opichal <opichals@seznam.cz>
Vendor        : Sparemint
URL           : http://isc.org/products/DHCP/

Prereq        : /sbin/chkconfig

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.isc.org/isc/dhcp/dhcp-%{version}.tar.gz
Source1: dhcpd.conf.sample
Source2: dhcpd.init
Source3: dhcrelay.init
Source4: dhclient
Patch0: dhcp-3.1.ESV-freemint.patch


%description
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.  The dhcp package includes the
ISC DHCP service and relay agent.

To use DHCP on your network, install a DHCP service (or relay agent),
and on clients run a DHCP client daemon.  The dhcp package provides
the ISC DHCP service and relay agent.

The -macnb version of the DHCP server has experimental support for Macintosh
netboot clients.

%package -n dhclient
Summary: Development headers and libraries for interfacing to the DHCP server
Group: System Environment/Base

%package devel
Summary: Development headers and libraries for interfacing to the DHCP server
Requires: dhcp = %{version}
Group: Development/Libraries

%description -n dhclient
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.

To use DHCP on your network, install a DHCP service (or relay agent),
and on clients run a DHCP client daemon.  The dhclient package 
provides the ISC DHCP client daemon.

%description devel
Libraries for interfacing with the ISC DHCP server.


%prep
%setup -q
%patch0 -p1

cp %SOURCE1 .
cat <<EOF >site.conf
VARDB=%{_localstatedir}/lib/dhcp
ADMMANDIR=%{_mandir}/man8
ADMMANEXT=.8
FFMANDIR=%{_mandir}/man5
FFMANEXT=.5
LIBMANDIR=%{_mandir}/man3
LIBMANEXT=.3
USRMANDIR=%{_mandir}/man1
USRMANEXT=.1
LIBDIR=%{_libdir}
INCDIR=%{_includedir}
EOF
cat <<EOF >>includes/site.h
#define _PATH_DHCPD_DB          "%{_localstatedir}/lib/dhcp/dhcpd.leases"
#define _PATH_DHCLIENT_DB       "%{_localstatedir}/lib/dhcp/dhclient.leases"
EOF


%build
./configure --copts "$RPM_OPT_FLAGS"
make %{?_smp_mflags} CC="gcc"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
make install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
install -m 0755 %SOURCE2 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/dhcpd

touch ${RPM_BUILD_ROOT}%{_localstatedir}/lib/dhcp/dhcpd.leases

cat <<EOF > ${RPM_BUILD_ROOT}/etc/sysconfig/dhcpd
# Command line options here
DHCPDARGS=
EOF

install -m0755 %SOURCE3 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/dhcrelay
install -m0755 %SOURCE4 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/dhclient

cat <<EOF > ${RPM_BUILD_ROOT}/etc/sysconfig/dhcrelay
# Command line options here
INTERFACES=""
DHCPSERVERS=""
EOF

# Copy sample dhclient.conf file into position
cp client/dhclient.conf dhclient.conf.sample
chmod 755 ${RPM_BUILD_ROOT}/sbin/dhclient-script

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_mandir}/man*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/chkconfig --add dhcpd
/sbin/chkconfig --add dhcrelay
cat <<EOF
=================
!!! IMPORTANT !!!
=================
This dhcp package require a corrected version of MiNTNet to work
properly. Please install the current inet4.xdd for FreeMiNT 1.16
or sockdev.xdd for FreeMiNT 1.15 from cvs.
EOF

%post -n dhclient
cat <<EOF
=================
!!! IMPORTANT !!!
=================
This dhcp package require a corrected version of MiNTNet to work
properly. Please install the current inet4.xdd for FreeMiNT 1.16
or sockdev.xdd for FreeMiNT 1.15 from cvs.
EOF

%preun
if [ $1 = 0 ]; then	# execute this only if we are NOT doing an upgrade
    #service dhcpd stop >/dev/null 2>&1
    #service dhcrelay stop >/dev/null 2>&1
    /sbin/chkconfig --del dhcpd 
    /sbin/chkconfig --del dhcrelay
fi

%postun
if [ "$1" -ge "1" ]; then
    #service dhcpd condrestart >/dev/null 2>&1
    #service dhcrelay condrestart >/dev/null 2>&1
fi


%files
%defattr(-,root,root)
%doc CHANGES README RELNOTES dhcpd.conf.sample
%dir %{_localstatedir}/lib/dhcp
%verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/dhcp/dhcpd.leases
%config(noreplace) /etc/sysconfig/dhcpd
%config(noreplace) /etc/sysconfig/dhcrelay
%config /etc/rc.d/init.d/dhcpd
%config /etc/rc.d/init.d/dhcrelay
%{_bindir}/omshell
%{_sbindir}/dhcpd
%{_sbindir}/dhcrelay
%{_mandir}/man1/omshell.1*
%{_mandir}/man5/dhcp-options.5*
%{_mandir}/man5/dhcp-eval.5*
%{_mandir}/man5/dhcpd.conf.5*
%{_mandir}/man5/dhcpd.leases.5*
%{_mandir}/man8/dhcpd.8*
%{_mandir}/man8/dhcrelay.8*

%files -n dhclient
%defattr(-,root,root)
%doc dhclient.conf.sample
%dir %{_localstatedir}/lib/dhcp
%config /etc/rc.d/init.d/dhclient
/sbin/dhclient
/sbin/dhclient-script
%{_mandir}/man5/dhcp-options.5*
%{_mandir}/man5/dhclient.conf.5*
%{_mandir}/man5/dhclient.leases.5*
%{_mandir}/man8/dhclient.8*
%{_mandir}/man8/dhclient-script.8*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_mandir}/man3/*


%changelog
* Mon Jun 30 2007 Marc-Anton Kehr <makehr@ndh.net>
- added DHCP client startup script for Sparemint

* Thu Feb 12 2006 Standa Opichal <opichals@seznam.cz>
- Updated to 3.0.3
- Removed the symbol information from the binaries (shorter) 

* Thu Dec 25 2003 Standa Opichal <opichals@seznam.cz>
- Ported to FreeMiNT 1.16.x
- Original spec file taken from RedHat Linux distribution

+ Sat Dec 08 2012 Peter Slegg
- Updated to 3.1-ESV
- Simple revision based on work by Standa Opichal