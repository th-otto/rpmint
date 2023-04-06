%define pkgname dhcp

%rpmint_header

Summary:        A DHCP (Dynamic Host Configuration Protocol) server and relay agent.
Name:           %{crossmint}%{pkgname}
Version:        3.1.ESV
Release:        1
License:        BSD-3-Clause
Group:          Productivity/Networking/Boot/Servers

Packager:       %{packager}
URL:            http://www.isc.org/software/dhcp

Prereq        : /sbin/chkconfig

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://ftp.isc.org/isc/dhcp/%{version}/%{pkgname}-%{version}.tar.gz
Source1: patches/dhcp/dhcp-dhcpd.conf.sample
Source2: patches/dhcp/dhcp-dhcpd.init
Source3: patches/dhcp/dhcp-dhcrelay.init
Source4: patches/dhcp/dhcp-dhclient.init

Patch0:  patches/dhcp/dhcp-3.1.ESV-freemint.patch

%rpmint_essential
BuildRequires:  make

%rpmint_build_arch

%description
The Dynamic Host Configuration Protocol (DHCP) is a network protocol
used to assign IP addresses and provide configuration information to
devices such as servers, desktops, or mobile devices, so they can
communicate on a network using the Internet Protocol (IP). ISC DHCP is
a collection of software that implements all aspects of the DHCP
(Dynamic Host Configuration Protocol) suite.

%package -n %{crossmint}dhclient
Summary: Development headers and libraries for interfacing to the DHCP server
Group: System Environment/Base

%description -n %{crossmint}dhclient
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.

To use DHCP on your network, install a DHCP service (or relay agent),
and on clients run a DHCP client daemon.  The dhclient package 
provides the ISC DHCP client daemon.

%package devel
Summary: Development headers and libraries for interfacing to the DHCP server
Group: Development/Libraries
Requires: dhcp = %{version}

%description devel
Libraries for interfacing with the DHCP server.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

sed -i 's:^#sysname=\$1$:sysname=freemint:g' configure
sed -i 's:^\tar :\t$(AR) :g' */Makefile.dist
sed -i 's:^CROSSPREFIX=\(.*\):CROSSPREFIX='%{_rpmint_target}-':' Makefile.conf

cp %{S:1} dhcpd.conf.sample

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS+=" -fno-strict-aliasing"

%define with_ldap 0
%define with_ldapcase 0
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-dhcpv6
	--enable-failover
	--enable-paranoia
	--enable-early-chroot
	--with-cli-pid-file=/var/run/dhclient.pid
	--with-cli-lease-file=/var/lib/dhcp/dhclient.leases
	--with-cli6-pid-file=/var/run/dhclient6.pid
	--with-cli6-lease-file=/var/lib/dhcp6/dhclient.leases
	--with-srv-pid-file=/var/run/dhcpd.pid
	--with-srv-lease-file=/var/lib/dhcp/db/dhcpd.leases
	--with-srv6-pid-file=/var/run/dhcpd6.pid
	--with-srv6-lease-file=/var/lib/dhcp6/db/dhcpd6.leases
"
%if %{with_ldap}
	CONFIGURE_FLAGS+=" --with-ldap --with-ldapcrypto"
	%if %{with_ldapcase}
		CONFIGURE_FLAGS+=" --with-ldapcasa"
	%endif
%endif

for CPU in ${ALL_CPUS}
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

cat <<EOF >> site.conf
USERBINDIR=%{_rpmint_target_prefix}/bin
BINDIR=%{_rpmint_target_prefix}/sbin
LIBDIR = %{_rpmint_target_prefix}/lib$multilibdir
INCDIR = %{_rpmint_target_prefix}/include
CLIENTBINDIR=/sbin
ADMMANDIR = %{_rpmint_target_prefix}/share/man/man8
ADMMANEXT = .8
FFMANDIR = %{_rpmint_target_prefix}/share/man/man5
FFMANEXT = .5
LIBMANDIR = %{_rpmint_target_prefix}/share/man/man3
LIBMANEXT = .3
USRMANDIR = %{_rpmint_target_prefix}/share/man/man1
USRMANEXT = .1
EOF
cat <<EOF >>includes/site.h
#define _PATH_DHCPD_DB          "%{_localstatedir}/lib/dhcp/dhcpd.leases"
#define _PATH_DHCLIENT_DB       "%{_localstatedir}/lib/dhcp/dhclient.leases"
EOF

	"./configure" ${CONFIGURE_FLAGS}

	M68K_ATARI_MINT_CFLAGS="${CPU_CFLAGS} $COMMON_CFLAGS ${LTO_CFLAGS} ${STACKSIZE}" \
	CROSSPREFIX="${TARGET}-" \
	make

	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib$multilibdir
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install
	chmod 755 %{buildroot}%{_rpmint_sysroot}/sbin/dhclient-script

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	mkdir -p %{buildroot}%{_rpmint_sysroot}/sbin
	install -m 755 work.freemint/server/dhcpd %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/sbin
	install -m 755 work.freemint/relay/dhcrelay %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/sbin
	mkdir -p %{buildroot}%{_rpmint_sysroot}/var/lib/dhcp
	touch %{buildroot}%{_rpmint_sysroot}/var/lib/dhcp/dhcpd.leases
	rm -f %{buildroot}%{_rpmint_sysroot}/var/db/dhcpd.leases
	rmdir %{buildroot}%{_rpmint_sysroot}/var/db || :

	# Copy sample dhclient.conf file into position
	cp client/dhclient.conf dhclient.conf.sample

	# install init scripts
	mkdir -p %{buildroot}%{_rpmint_sysroot}/etc/rc.d/init.d
	install -m 0755 %SOURCE2 %{buildroot}%{_rpmint_sysroot}/etc/rc.d/init.d/dhcpd
	install -m 0755 %SOURCE3 %{buildroot}%{_rpmint_sysroot}/etc/rc.d/init.d/dhcrelay
	install -m 0755 %SOURCE4 %{buildroot}%{_rpmint_sysroot}/etc/rc.d/init.d/dhclient

mkdir -p %{buildroot}%{_rpmint_sysroot}/etc/sysconfig
cat <<EOF > %{buildroot}%{_rpmint_sysroot}/etc/sysconfig/dhcpd
# Command line options here
DHCPDARGS=
EOF

cat <<EOF > %{buildroot}%{_rpmint_sysroot}/etc/sysconfig/dhcrelay
# Command line options here
INTERFACES=""
DHCPSERVERS=""
EOF

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
		rm -f %{buildroot}%{_rpmint_sysroot}/sbin/*
		rm -f %{buildroot}%{_rpmint_sysroot}/%{_rpmint_target_prefix}/sbin/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make clean >/dev/null
done


%install

%rpmint_cflags

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%license LICENSE
%doc README RELNOTES dhcpd.conf.sample
%dir %{_isysroot}/var/lib/dhcp
%verify(not size md5 mtime) %config(noreplace) %{_isysroot}/var/lib/dhcp/dhcpd.leases
%config(noreplace) %{_isysroot}/etc/sysconfig/dhcpd
%config(noreplace) %{_isysroot}/etc/sysconfig/dhcrelay
%config %{_isysroot}/etc/rc.d/init.d/dhcpd
%config %{_isysroot}/etc/rc.d/init.d/dhcrelay
%{_isysroot}%{_rpmint_target_prefix}/bin/omshell
%{_isysroot}%{_rpmint_target_prefix}/sbin/dhcpd
%{_isysroot}%{_rpmint_target_prefix}/sbin/dhcrelay
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/omshell.1*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/dhcp-options.5*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/dhcp-eval.5*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/dhcpd.conf.5*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/dhcpd.leases.5*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man8/dhcpd.8*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man8/dhcrelay.8*


%files -n %{crossmint}dhclient
%defattr(-,root,root)
%doc dhclient.conf.sample
%dir %{_isysroot}/var/lib/dhcp
%config %{_isysroot}/etc/rc.d/init.d/dhclient
%{_isysroot}/sbin/dhclient
%{_isysroot}/sbin/dhclient-script
%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/dhclient.conf.5*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/dhclient.leases.5*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man8/dhclient.8*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man8/dhclient-script.8*

%files devel
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/share/man/man3/*


%if "%{buildtype}" != "cross"
%post
/sbin/chkconfig --add dhcpd
/sbin/chkconfig --add dhcrelay

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
%endif


%changelog
* Wed Mar 29 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Sat Dec 08 2012 Peter Slegg
- Updated to 3.1-ESV
- Simple revision based on work by Standa Opichal

* Sat Jun 30 2007 Marc-Anton Kehr <makehr@ndh.net>
- added DHCP client startup script for Sparemint

* Sun Feb 12 2006 Standa Opichal <opichals@seznam.cz>
- Updated to 3.0.3
- Removed the symbol information from the binaries (shorter) 

* Thu Dec 25 2003 Standa Opichal <opichals@seznam.cz>
- Ported to FreeMiNT 1.16.x
- Original spec file taken from RedHat Linux distribution
