#
# spec file for package openldap2
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define run_test_suite 0
%define version_main 2.4.45

%if %{suse_version} >= 1310 && %{suse_version} != 1315
%define  _rundir /run/slapd
%else
%define  _rundir /var/run/slapd
%endif

%define name_ppolicy_check_module ppolicy-check-password
%define version_ppolicy_check_module 1.2
%define ppolicy_docdir %{_docdir}/openldap-%{name_ppolicy_check_module}-%{version_ppolicy_check_module}

Name:           openldap2
Summary:        An open source implementation of the Lightweight Directory Access Protocol
License:        OLDAP-2.8
Group:          Productivity/Networking/LDAP/Servers
Version:        %{version_main}
Release:        27.2
Url:            http://www.openldap.org
Source:         ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/openldap-%{version_main}.tgz
Source1:        slapd.conf
Source2:        slapd.conf.olctemplate
Source3:        DB_CONFIG
Source4:        sasl-slapd.conf
Source5:        README.module-loading
Source6:        schema2ldif
Source7:        baselibs.conf
Source9:        addonschema.tar.gz
Source12:       slapd.conf.example
Source13:       start
Source14:       slapd.service
Source15:       SuSEfirewall2.openldap
Source16:       sysconfig.openldap
Patch3:         0003-LDAPI-socket-location.dif
Patch5:         0005-pie-compile.dif
Patch6:         0006-No-Build-date-and-time-in-binaries.dif
Patch7:         0007-Recover-on-DB-version-change.dif
Patch8:         0008-In-monitor-backend-do-not-return-Connection0-entries.patch
Patch9:         0009-Fix-ldap-host-lookup-ipv6.patch
Patch11:        0011-openldap-re24-its7796.patch
Patch12:        0012-ITS8051-sockdnpat.patch
Patch13:        0013-ITS-8692-let-back-sock-generate-increment-line.patch
Patch14:        0014-ITS-8714-Send-out-EXTENDED-operation-message-from-back-sock.patch
Patch15:        openldap-r-only.dif
Source200:      %{name_ppolicy_check_module}-%{version_ppolicy_check_module}.tar.gz
Source201:      %{name_ppolicy_check_module}.Makefile
Source202:      %{name_ppolicy_check_module}.conf
Source203:      %{name_ppolicy_check_module}.5
Patch200:       0200-Fix-incorrect-calculation-of-consecutive-number-of-c.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  cyrus-sasl-devel
BuildRequires:  db-devel
BuildRequires:  groff
BuildRequires:  libopenssl-devel
BuildRequires:  libtool
BuildRequires:  openslp-devel
BuildRequires:  unixODBC-devel
%if %{suse_version} >= 1310 && %{suse_version} != 1315
# avoid cycle with krb5
BuildRequires:  krb5-mini
BuildRequires:  pkgconfig(systemd)
%{?systemd_requires}
%endif
Requires:       libldap-2_4-2 = %{version_main}
Recommends:     cyrus-sasl
Conflicts:      openldap
PreReq:         %fillup_prereq /usr/sbin/useradd /usr/sbin/groupadd /usr/bin/grep

%description
OpenLDAP is a client and server reference implementation of the
Lightweight Directory Access Protocol v3 (LDAPv3).

The server provides several database backends and overlays.

%package back-perl
Summary:        OpenLDAP Perl Back-End
Group:          Productivity/Networking/LDAP/Servers
Requires:       openldap2 = %{version_main}
Requires:       perl = %{perl_version}

%description back-perl
The OpenLDAP Perl back-end allows you to execute Perl code specific to
different LDAP operations.

%package back-sock
Summary:        OpenLDAP Socket Back-End
Group:          Productivity/Networking/LDAP/Servers
Requires:       openldap2 = %{version_main}
Provides:       openldap2:/usr/share/man/man5/slapd-sock.5.gz

%description back-sock
The OpenLDAP socket back-end allows you to handle LDAP requests and
results with an external process listening on a Unix domain socket.

%package back-meta
Summary:        OpenLDAP Meta Back-End
Group:          Productivity/Networking/LDAP/Servers
Requires:       openldap2 = %{version_main}
Provides:       openldap2:/usr/share/man/man5/slapd-meta.5.gz

%description back-meta
The OpenLDAP Meta back-end is able to perform basic LDAP proxying with
respect to a set of remote LDAP servers. The information contained in
these servers can be presented as belonging to a single Directory
Information Tree (DIT).

%package back-sql
Summary:        OpenLDAP SQL Back-End
Group:          Productivity/Networking/LDAP/Servers
Requires:       openldap2 = %{version_main}

%description back-sql
The primary purpose of this OpenLDAP backend is to present information
stored in a Relational (SQL) Database as an LDAP subtree without the need
to do any programming.

%package -n libldap-data
Summary:        Configuration file for system-wide defaults for all uses of libldap
Group:          Productivity/Networking/LDAP/Clients
%if 0%{?suse_version} != 1110
BuildArch:      noarch
%endif

%description -n libldap-data
The subpackage contains a configuration file used to set system-wide defaults
to be applied with all usages of libldap.

%package contrib
Summary:        OpenLDAP Contrib Modules
Group:          Productivity/Networking/LDAP/Servers
Requires:       openldap2 = %{version_main}

%description contrib
Various overlays found in contrib/:
addpartial    Intercepts ADD requests, applies changes to existing entries
allop
allowed       Generates attributes indicating access rights
autogroup
cloak
denyop
lastbind      writes last bind timestamp to entry
noopsrch      handles no-op search control
nops
pw-sha2       generates/validates SHA-2 password hashes
pw-pbkdf2     generates/validates PBKDF2 password hashes
smbk5pwd      generates Samba3 password hashes (heimdal krb disabled)
trace         traces overlay invocation

%package doc
Summary:        OpenLDAP Documentation
Group:          Documentation/Other
Provides:       openldap2:/usr/share/doc/packages/openldap2/drafts/README
%if 0%{?suse_version} > 1110
BuildArch:      noarch
%endif

%description doc
The OpenLDAP Admin Guide plus a set of OpenLDAP related IETF internet drafts.

%package client
Summary:        OpenLDAP client utilities
Group:          Productivity/Networking/LDAP/Clients
Requires:       libldap-2_4-2 = %{version_main}

%description client
OpenLDAP client utilities such as ldapadd, ldapsearch, ldapmodify.

%package devel
Summary:        Libraries, Header Files and Documentation for OpenLDAP
# bug437293
Group:          Development/Libraries/C and C++
%ifarch ppc64
Obsoletes:      openldap2-devel-64bit
%endif
#
Conflicts:      openldap-devel
Requires:       libldap-2_4-2 = %{version_main}
Recommends:     cyrus-sasl-devel

%description devel
This package provides the OpenLDAP libraries, header files, and
documentation.

%package devel-static
Summary:        Static libraries for the OpenLDAP libraries
Group:          Development/Libraries/C and C++
Requires:       cyrus-sasl-devel
Requires:       libopenssl-devel
Requires:       openldap2-devel = %version

%description devel-static
This package provides the static versions of the OpenLDAP libraries
for development.

%package      -n libldap-2_4-2
Summary:        OpenLDAP Client Libraries
Group:          Productivity/Networking/LDAP/Clients
Recommends:     libldap-data >= %{version_main}

%description -n libldap-2_4-2
This package contains the OpenLDAP client libraries.

%package ppolicy-check-password
Version:        %{version_ppolicy_check_module}
Release:        27.2
Summary:        Password quality check module for OpenLDAP
Group:          Productivity/Networking/LDAP/Servers
Url:            https://github.com/onyxpoint/ppolicy-check-password
BuildRequires:  cracklib-devel
Requires:       openldap2 = %version_main
Recommends:     cracklib cracklib-dict-full

%description ppolicy-check-password
An implementation of password quality check module, based on the original
work done by LDAP Toolbox Project (https://ltd-project.org), that works
together with OpenLDAP password policy overlay (ppolicy), to enforce
password strength policies.

%prep
# Unpack ppolicy check module
%setup -b 200 -q -n %{name_ppolicy_check_module}-%{version_ppolicy_check_module}
%patch200 -p1
cd ..
# Compress the manual page of ppolicy check module
gzip -k %{S:203}

# Unpack and patch OpenLDAP 2.4
%setup -q -a 9 -n openldap-%{version_main}
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
cp %{SOURCE5} .

# Move ppolicy check module and its Makefile into openldap-2.4/contrib/slapd-modules/
mv ../%{name_ppolicy_check_module}-%{version_ppolicy_check_module} contrib/slapd-modules/%{name_ppolicy_check_module}
cp %{S:201} contrib/slapd-modules/%{name_ppolicy_check_module}/Makefile

%build
export CFLAGS="%{optflags} -Wno-format-extra-args -fno-strict-aliasing -DNDEBUG -DSLAP_CONFIG_DELETE -DSLAP_SCHEMA_EXPOSE -DLDAP_COLLECTIVE_ATTRIBUTES -DLDAP_USE_NON_BLOCKING_TLS"
export STRIP=""
./configure \
        --prefix=/usr \
        --sysconfdir=%{_sysconfdir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libdir} \
        --localstatedir=%{_rundir} \
        --enable-wrappers=no \
        --enable-spasswd \
        --enable-modules \
        --enable-shared \
        --enable-dynamic \
        --with-tls=openssl \
        --with-cyrus-sasl \
        --enable-crypt \
        --enable-ipv6=yes \
        --enable-aci \
        --enable-bdb=mod \
        --enable-hdb=mod \
        --enable-rewrite \
        --enable-ldap=mod \
        --enable-meta=mod \
        --enable-monitor=mod \
        --enable-perl=mod \
        --enable-sock=mod \
        --enable-sql=mod \
        --enable-mdb=mod \
        --enable-relay=mod \
        --enable-slp \
        --enable-overlays=mod \
        --enable-syncprov=mod \
        --enable-ppolicy=mod \
        --enable-lmpasswd \
        --with-yielding-select \
  || cat config.log
make depend
make %{?_smp_mflags}
# Build selected contrib overlays
for SLAPO_NAME in addpartial allowed allop autogroup lastbind nops denyop cloak noopsrch passwd/sha2 passwd/pbkdf2 trace
do
  make -C contrib/slapd-modules/${SLAPO_NAME} %{?_smp_mflags} "sysconfdir=%{_sysconfdir}/openldap" "libdir=%{_libdir}" "libexecdir=%{_libdir}"
done
# slapo-smbk5pwd only for Samba password hashes
make -C contrib/slapd-modules/smbk5pwd %{?_smp_mflags} "sysconfdir=%{_sysconfdir}/openldap" "libdir=%{_libdir}" "libexecdir=%{_libdir}" DEFS="-DDO_SAMBA" HEIMDAL_LIB=""

# Build ppolicy-check-password module
make -C contrib/slapd-modules/%{name_ppolicy_check_module} %{?_smp_mflags} "sysconfdir=%{_sysconfdir}/openldap" "libdir=%{_libdir}" "libexecdir=%{_libdir}"

%check
%if %run_test_suite
# calculate the base port to be use in the test-suite
SLAPD_BASEPORT=10000
if [ -f /.buildenv ] ; then
    . /.buildenv
    SLAPD_BASEPORT=$(($SLAPD_BASEPORT + ${BUILD_INCARNATION:-0} * 10))
fi
export SLAPD_BASEPORT
%ifnarch %arm alpha
rm -f tests/scripts/test019-syncreplication-cascade
rm -f tests/scripts/test022-ppolicy
rm -f tests/scripts/test023-refint
rm -f tests/scripts/test033-glue-syncrepl
#rm -f tests/scripts/test036-meta-concurrency
#rm -f tests/scripts/test039-glue-ldap-concurrency
rm -f tests/scripts/test043-delta-syncrepl
#rm -f tests/scripts/test045-syncreplication-proxied
rm -f tests/scripts/test048-syncrepl-multiproxy
rm -f tests/scripts/test050-syncrepl-multimaster
rm -f tests/scripts/test058-syncrepl-asymmetric
make SLAPD_DEBUG=0 test
%endif
%endif

%install
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}/openldap
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/openldap
mkdir -p ${RPM_BUILD_ROOT}/usr/sbin
mkdir -p ${RPM_BUILD_ROOT}/%{_unitdir}
make STRIP="" "DESTDIR=${RPM_BUILD_ROOT}" "sysconfdir=%{_sysconfdir}/openldap" "libdir=%{_libdir}" "libexecdir=%{_libdir}" install
# Additional symbolic link to slapd executable in /usr/sbin/
ln -s %{_libdir}/slapd ${RPM_BUILD_ROOT}/usr/sbin/slapd
# Install selected contrib overlays
for SLAPO_NAME in addpartial allowed allop autogroup lastbind nops denyop cloak noopsrch passwd/sha2 passwd/pbkdf2 trace
do
  make -C contrib/slapd-modules/${SLAPO_NAME} STRIP="" "DESTDIR=${RPM_BUILD_ROOT}" "sysconfdir=%{_sysconfdir}/openldap" "libdir=%{_libdir}" "libexecdir=%{_libdir}" install
done
# slapo-smbk5pwd only for Samba password hashes
make -C contrib/slapd-modules/smbk5pwd STRIP="" "DESTDIR=${RPM_BUILD_ROOT}" "sysconfdir=%{_sysconfdir}/openldap" "libdir=%{_libdir}" "libexecdir=%{_libdir}" install
install -m 755 %{SOURCE13} ${RPM_BUILD_ROOT}/usr/lib/openldap/start
install -m 644 %{SOURCE14} ${RPM_BUILD_ROOT}/%{_unitdir}
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/openldap/slapd.d
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/sasl2
install -m 644 %{SOURCE4} ${RPM_BUILD_ROOT}/%{_sysconfdir}/sasl2/slapd.conf
install -m 755 -d ${RPM_BUILD_ROOT}/var/lib/ldap
chmod a+x ${RPM_BUILD_ROOT}/%{_libdir}/liblber.so*
chmod a+x ${RPM_BUILD_ROOT}/%{_libdir}/libldap_r.so*
install -m 755 %{SOURCE6} ${RPM_BUILD_ROOT}/usr/sbin/schema2ldif

# Install ppolicy check module
make -C contrib/slapd-modules/ppolicy-check-password STRIP="" "DESTDIR=${RPM_BUILD_ROOT}" "sysconfdir=%{_sysconfdir}/openldap" "libdir=%{_libdir}" "libexecdir=%{_libexecdir}" install
install -m 0644 %{S:202}  %{buildroot}%{_sysconfdir}/openldap/check_password.conf
# Install ppolicy check module's doc files
pushd contrib/slapd-modules/%{name_ppolicy_check_module}
mkdir -p "%{buildroot}%ppolicy_docdir"
install -m 0644 README "%{buildroot}%ppolicy_docdir"
install -m 0644 LICENSE "%{buildroot}%ppolicy_docdir"
popd
# Install ppolicy check module's manual page
install -m 0644 %{S:203}.gz %{buildroot}%{_mandir}/man5/

mkdir -p ${RPM_BUILD_ROOT}/var/adm/fillup-templates
install -m 644 %{SOURCE16} ${RPM_BUILD_ROOT}/var/adm/fillup-templates/sysconfig.openldap
install -m 644 *.ldif ${RPM_BUILD_ROOT}%{_sysconfdir}/openldap/schema
install -m 644 *.schema ${RPM_BUILD_ROOT}%{_sysconfdir}/openldap/schema
# Install default and sample configuration files
install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/openldap
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/openldap
install -m 644 %{SOURCE12} ${RPM_BUILD_ROOT}%{_sysconfdir}/openldap
# Install default database optimisations
install -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}/var/lib/ldap/DB_CONFIG
install -m 644 ${RPM_BUILD_ROOT}/etc/openldap/DB_CONFIG.example ${RPM_BUILD_ROOT}/var/lib/ldap/DB_CONFIG.example
install -d ${RPM_BUILD_ROOT}/etc/sysconfig/SuSEfirewall2.d/services/
install -m 644 %{SOURCE15} ${RPM_BUILD_ROOT}/etc/sysconfig/SuSEfirewall2.d/services/openldap
find doc/guide '(' ! -name *.html -a ! -name *.gif -a ! -name *.png -a ! -type d ')' -delete
rm -rf doc/guide/release

%define DOCDIR %{_defaultdocdir}/%{name}
install -d ${RPM_BUILD_ROOT}/%{DOCDIR}/adminguide \
           ${RPM_BUILD_ROOT}/%{DOCDIR}/images \
           ${RPM_BUILD_ROOT}/%{DOCDIR}/drafts
install -m 644 doc/guide/admin/* ${RPM_BUILD_ROOT}/%{DOCDIR}/adminguide
install -m 644 doc/guide/images/*.gif ${RPM_BUILD_ROOT}/%{DOCDIR}/images
install -m 644 doc/drafts/* ${RPM_BUILD_ROOT}/%{DOCDIR}/drafts
install -m 644 ANNOUNCEMENT \
               COPYRIGHT \
               LICENSE \
               README \
               CHANGES \
               %{SOURCE5} \
               ${RPM_BUILD_ROOT}/%{DOCDIR}
install -m 644 servers/slapd/slapd.ldif \
               ${RPM_BUILD_ROOT}/%{DOCDIR}/slapd.ldif.default
rm -f ${RPM_BUILD_ROOT}/etc/openldap/DB_CONFIG.example
rm -f ${RPM_BUILD_ROOT}/etc/openldap/schema/README
rm -f ${RPM_BUILD_ROOT}/etc/openldap/slapd.ldif*
rm -f ${RPM_BUILD_ROOT}/%{_rundir}/openldap-data/DB_CONFIG.example
mv servers/slapd/back-sql/rdbms_depend servers/slapd/back-sql/examples

ln -s %{_sbindir}/service %{buildroot}%{_sbindir}/rcslapd

rm -f ${RPM_BUILD_ROOT}/%{_libdir}/openldap/*.a
rm -f ${RPM_BUILD_ROOT}/usr/share/man/man5/slapd-dnssrv.5
rm -f ${RPM_BUILD_ROOT}/usr/share/man/man5/slapd-ndb.5
rm -f ${RPM_BUILD_ROOT}/usr/share/man/man5/slapd-null.5
rm -f ${RPM_BUILD_ROOT}/usr/share/man/man5/slapd-passwd.5
rm -f ${RPM_BUILD_ROOT}/usr/share/man/man5/slapd-shell.5
rm -f ${RPM_BUILD_ROOT}/usr/share/man/man5/slapd-tcl.5
# Remove *.la files, libtool does not handle this correct
rm -f  ${RPM_BUILD_ROOT}%{_libdir}/lib*.la

# Make ldap_r the only copy in the system [rh#1370065].
# libldap.so is only for `gcc/ld -lldap`. Make no libldap-2.4.so.2.
rm -f "%{buildroot}/%{_libdir}"/libldap-2.4.so*
ln -fs libldap_r.so "%{buildroot}/%{_libdir}/libldap.so"

%pre
getent group ldap >/dev/null || /usr/sbin/groupadd -g 70 -o -r ldap
getent passwd ldap >/dev/null || /usr/sbin/useradd -r -o -g ldap -u 76 -s /bin/false -c "User for OpenLDAP" -d /var/lib/ldap ldap
%service_add_pre slapd.service

%post
if [ ${1:-0} -gt 1 ] && [ -f %{_libdir}/sasl2/slapd.conf ] ; then
  cp /etc/sasl2/slapd.conf /etc/sasl2/slapd.conf.rpmnew
  cp %{_libdir}/sasl2/slapd.conf /etc/sasl2/slapd.conf
fi
%{fillup_only -n openldap ldap}
%service_add_post slapd.service

%post -n libldap-2_4-2 -p /sbin/ldconfig

%postun -n libldap-2_4-2 -p /sbin/ldconfig

%preun
%service_del_preun slapd.service

%postun
%service_del_postun slapd.service

%files
%defattr(-,root,root)
%config %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/openldap
%config %{_sysconfdir}/openldap/schema/*.schema
%config %{_sysconfdir}/openldap/schema/*.ldif
%config(noreplace) /etc/sasl2/slapd.conf
%config(noreplace) %attr(640, root, ldap) %{_sysconfdir}/openldap/slapd.conf
%config(noreplace) %attr(640, root, ldap) %{_sysconfdir}/openldap/slapd.conf.olctemplate
%config %attr(640, root, ldap) %{_sysconfdir}/openldap/slapd.conf.default
%config %attr(640, root, ldap) %{_sysconfdir}/openldap/slapd.conf.example
%config(noreplace) %attr(640, ldap, ldap) /var/lib/ldap/DB_CONFIG
%config /var/lib/ldap/DB_CONFIG.example
%dir %{_libdir}/openldap
%dir %{_libexecdir}/openldap
%dir %{_sysconfdir}/sasl2
%dir %{_sysconfdir}/openldap
%dir %attr(0770, ldap, ldap) %{_sysconfdir}/openldap/slapd.d
%dir %{_sysconfdir}/openldap/schema
/var/adm/fillup-templates/sysconfig.openldap
%{_sbindir}/slap*
%{_sbindir}/rcslapd
%{_libdir}/openldap/back_bdb*
%{_libdir}/openldap/back_hdb*
%{_libdir}/openldap/back_ldap*
%{_libdir}/openldap/back_mdb*
%{_libdir}/openldap/back_monitor*
%{_libdir}/openldap/back_relay*
%{_libdir}/openldap/accesslog*
%{_libdir}/openldap/auditlog*
%{_libdir}/openldap/collect*
%{_libdir}/openldap/constraint*
%{_libdir}/openldap/dds*
%{_libdir}/openldap/deref*
%{_libdir}/openldap/dyngroup*
%{_libdir}/openldap/dynlist*
%{_libdir}/openldap/memberof*
%{_libdir}/openldap/pcache*
%{_libdir}/openldap/ppolicy-2.4.*
%{_libdir}/openldap/ppolicy.*
%{_libdir}/openldap/refint*
%{_libdir}/openldap/retcode*
%{_libdir}/openldap/rwm*
%{_libdir}/openldap/seqmod*
%{_libdir}/openldap/sssvlv*
%{_libdir}/openldap/syncprov*
%{_libdir}/openldap/translucent*
%{_libdir}/openldap/unique*
%{_libdir}/openldap/valsort*
%{_libdir}/slapd
%{_libexecdir}/openldap/start
%{_unitdir}/slapd.service
%dir %attr(0750, ldap, ldap) /var/lib/ldap
%ghost %attr(0750, ldap, ldap) %{_rundir}
%doc %{_mandir}/man8/sl*
%doc %{_mandir}/man5/slapd.*
%doc %{_mandir}/man5/slapd-bdb.*
%doc %{_mandir}/man5/slapd-config.*
%doc %{_mandir}/man5/slapd-hdb.*
%doc %{_mandir}/man5/slapd-ldbm.*
%doc %{_mandir}/man5/slapd-ldap.*
%doc %{_mandir}/man5/slapd-ldif.*
%doc %{_mandir}/man5/slapd-mdb.*
%doc %{_mandir}/man5/slapd-monitor.*
%doc %{_mandir}/man5/slapd-relay.*
%doc %{_mandir}/man5/slapo-*
%dir %{DOCDIR}
%doc %{DOCDIR}/ANNOUNCEMENT
%doc %{DOCDIR}/COPYRIGHT
%doc %{DOCDIR}/LICENSE
%doc %{DOCDIR}/README*
%doc %{DOCDIR}/CHANGES
%doc %{DOCDIR}/slapd.ldif.default

%files back-perl
%defattr(-,root,root)
%{_libdir}/openldap/back_perl*
%doc %{_mandir}/man5/slapd-perl.*

%files back-sock
%defattr(-,root,root)
%{_libdir}/openldap/back_sock*
%doc %{_mandir}/man5/slapd-sock.*

%files back-meta
%defattr(-,root,root)
%{_libdir}/openldap/back_meta*
%doc %{_mandir}/man5/slapd-meta.*

%files back-sql
%defattr(-,root,root)
%{_libdir}/openldap/back_sql*
%doc %{_mandir}/man5/slapd-sql.*
%doc servers/slapd/back-sql/examples
%doc servers/slapd/back-sql/docs/bugs
%doc servers/slapd/back-sql/docs/install

%files -n libldap-data
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/openldap/ldap.conf
%doc %{_mandir}/man5/ldap.conf*
%{_sysconfdir}/openldap/ldap.conf.default

%files doc
%defattr(-,root,root)
%dir %{DOCDIR}
%doc %{DOCDIR}/drafts
%doc %{DOCDIR}/adminguide
%doc %{DOCDIR}/images

%files contrib
%defattr(-,root,root)
%{_libdir}/openldap/addpartial.*
%{_libdir}/openldap/allowed.*
%{_libdir}/openldap/allop.*
%{_libdir}/openldap/autogroup.*
%{_libdir}/openldap/lastbind.*
%{_libdir}/openldap/noopsrch.*
%{_libdir}/openldap/nops.*
%{_libdir}/openldap/pw-sha2.*
%{_libdir}/openldap/pw-pbkdf2.*
%{_libdir}/openldap/denyop.*
%{_libdir}/openldap/cloak.*
%{_libdir}/openldap/smbk5pwd.*
%{_libdir}/openldap/trace.*

%files client
%defattr(-,root,root)
%doc %{_mandir}/man1/ldap*
%doc %{_mandir}/man5/ldif.*
%dir /etc/openldap
/usr/sbin/schema2ldif
/usr/bin/ldapadd
/usr/bin/ldapcompare
/usr/bin/ldapdelete
/usr/bin/ldapexop
/usr/bin/ldapmodify
/usr/bin/ldapmodrdn
/usr/bin/ldapsearch
/usr/bin/ldappasswd
/usr/bin/ldapurl
/usr/bin/ldapwhoami

%files -n libldap-2_4-2
%defattr(-,root,root)
%{_libdir}/liblber*2.4.so.*
%{_libdir}/libldap*2.4.so.*

%files devel
%defattr(-,root,root)
%doc %{_mandir}/man3/ber*
%doc %{_mandir}/man3/lber*
%doc %{_mandir}/man3/ld_errno*
%doc %{_mandir}/man3/ldap*
%{_includedir}/*.h
%{_libdir}/liblber.so
%{_libdir}/libldap*.so

%files devel-static
%defattr(-,root,root)
%_libdir/liblber.a
%_libdir/libldap*.a

%files ppolicy-check-password
%defattr(-,root,root)
%doc %{ppolicy_docdir}/
%config(noreplace) /etc/openldap/check_password.conf
%{_libdir}/openldap/ppolicy-check-password.*
%{_mandir}/man5/ppolicy-check-password.*

%changelog
* Mon Oct  2 2017 jengelh@inai.de
- Add openldap-r-only.dif so that openldap2's own tools also
  link against libldap_r rather than libldap.
- Make libldap equivalent to libldap_r (like Debian) to avoid
  crashes in threaded programs which unknowingly get both
  libraries inserted into their process image.
  [rh#1370065, boo#996551]
* Mon Oct  2 2017 mrueckert@suse.de
- use existing groups instead of inventing new ones
* Mon Sep 18 2017 michael@stroeder.com
- added 0012-ITS8051-sockdnpat.patch
* Wed Sep  6 2017 michael@stroeder.com
- updated 0014-ITS-8714-Send-out-EXTENDED-operation-message-from-back-sock.patch
* Fri Aug 18 2017 michael@stroeder.com
- Added OpenLDAP new feature implementing OpenLDAP ITS#8714
  0014-ITS-8714-Send-out-EXTENDED-operation-message-from-back-sock.patch
* Thu Jul 20 2017 michael@stroeder.com
- added overlay trace to package openldap2-contrib
* Wed Jul 12 2017 michael@stroeder.com
- Upgrade to upstream 2.4.45 release
- removed obsolete 0010-Enforce-minimum-DH-size-of-1024.patch
  and  0012-use-system-wide-cert-dir-by-default.patch
- added 0013-ITS-8692-let-back-sock-generate-increment-line.patch
  for supporting modify increment operations with back-sock
- added overlay addpartial to package openldap2-contrib
* Wed Jun  7 2017 hguo@suse.com
- Remove legacy daemon control that was used to migrate from SLE 11
  to 12. (bsc#1038405)
* Tue Jun  6 2017 hguo@suse.com
- There is no change made about the package itself, this is only
  copying over some changelog texts from SLE package:
- bug#976172 owned by hguo@suse.com: openldap2 - missing
  /usr/share/doc/packages/openldap2/guide/admin/guide.html
- bug#916914 owned by varkoly@suse.com: VUL-0: CVE-2015-1546:
  openldap2: slapd crash in valueReturnFilter cleanup
- [fate#319300](https://fate.suse.com/319300)
- [CVE-2015-1545](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1545)
- bug#905959 owned by hguo@suse.com: L3-Question: Are multiple
  "Connection 0" in a Multi Master setup normal ?
- [CVE-2015-1546](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1546)
- bug#916897 owned by varkoly@suse.com: VUL-0: CVE-2015-1545:
  openldap2: slapd crashes on search with deref control and empty attr list
* Fri Apr  7 2017 jengelh@inai.de
- Drop binutils requirement; the code using /usr/bin/strings has
  been dropped in openSUSE:Factory/openldap2 revision 112.
* Sat Feb 18 2017 kukuk@suse.com
- Remove superfluous insserv PreReq.
* Thu Nov 10 2016 hguo@suse.com
- Introduce patch 0012-use-system-wide-cert-dir-by-default.patch
  to let OpenLDAP read system wide certificate directory by
  default and avoid hiding the error if user specified CA location
  cannot be read (bsc#1009470).
* Fri Oct 14 2016 hguo@suse.com
- Add more details in the comments of slapd.conf concerning
  file permission and StartTLS capability.
* Thu Jun 23 2016 jengelh@inai.de
- Test for user/group existence before trying to add them.
  Summary spello update.
* Thu Jun 16 2016 hguo@suse.com
- Move schema files into tarball addonschema.tar.gz:
  ldapns.ldif ldapns.schema rfc2307bis.ldif rfc2307bis.schema
  yast.ldif yast.schema
- Package previously missing schema files in LDIF format:
  amavisd-new.ldif dhcp.ldif dlz.ldif dnszone.ldif samba3.ldif
  sudo.ldif suse-mailserver.ldif (bsc#984691)
- Fix a minor issue in schema2ldif script that led to missing
  attribute in the generated LDIF.
* Tue May 17 2016 hguo@suse.com
- Enable build flag LDAP_USE_NON_BLOCKING_TLS to fix bsc#978408.
* Thu Feb 25 2016 hguo@suse.com
- Move ldap.conf into libldap-data package, per convention.
* Sun Feb 21 2016 jengelh@inai.de
- Move ldap.conf out of shlib package again, they are not allowed
  there for obvious reasons (conflict with future package).
* Thu Feb 18 2016 hguo@suse.com
- Build password strength enforcer as an implementation of ppolicy
  password checker, introducing:
  ppolicy-check-password-1.2.tar.gz
  ppolicy-check-password.Makefile
  ppolicy-check-password.conf
  ppolicy-check-password.5
  0200-Fix-incorrect-calculation-of-consecutive-number-of-c.patch
  (Implements fate#319461)
* Thu Feb 18 2016 lmuelle@suse.com
- Remove redundant -n openldap2- package name prefix.
* Mon Feb  8 2016 hguo@suse.com
- Remove openldap2-client.spec and openldap2-client.changes
  openldap2.spec now builds client utilities and libraries.
  Thus pre_checkin.sh is removed.
- Move ldap.conf and its manual page from openldap2-client package
  to libldap-2_4-2 package, which is more appropriate.
- Use RPM_OPT_FLAGS in build flags.
- Macros dealing with old/unsupported distributions are removed.
- Remove 0002-slapd.conf.dif and install improved slapd.conf from
  new source file slapd.conf.
- Install slapd.conf.olctemplate to assist in preparing slapd.d
  for OLC.
- Be explicit in sysconfig that by default openldap will use
  static file configuration.
- Add the following schemas in LDIF format:
  * rfc2307bis.ldif
  * ldapns.ldif
  * yast.ldif
- Other minor clean-ups in the spec file.
* Mon Feb  8 2016 mpluskal@suse.com
- Use optflags when building
* Sat Feb  6 2016 michael@stroeder.com
- Upgrade to upstream 2.4.44 release with accumulated bug fixes.
- Specify source with FTP URL
- Removed obsolete 0012-openldap-re24-its8336.patch
* Mon Jan 25 2016 hguo@suse.com
- Relabel patch 0011-Enforce-minimum-DH-size-of-1024.patch
  into 0010-Enforce-minimum-DH-size-of-1024.patch
* Tue Dec  8 2015 michael@stroeder.com
- Upgrade to upstream 2.4.43 release with accumulated bug fixes.
- Still build on SLES12
- Loadable backend and overlay modules are now installed
  into arch-specific path %%{_libdir}/openldap
- All backends and overlays as modules for smaller memory footprint
  on memory constrained systems
- Added extra package for back-sock
- Consequent use of %%{_rundir} everywhere
- Rely on upstream ./configure script instead of any other
  macro foo
- Dropped linking with libwrap
- Dropped 0004-libldap-use-gethostbyname_r.dif because this
  work-around for nss_ldap is obsolete
- New sub-package openldap2-contrib with selected contrib/ overlays
- Replaced addonschema.tar.gz with separate schema sources
- Updated ldapns.schema from recent slapo-nssov source tree
- Added symbolic link to slapd executable in /usr/sbin/
- Added more complex example configuration file
  /etc/openldap/slapd.conf.example
- Set OPENLDAP_START_LDAPI="yes" in /etc/sysconfig/openldap
- Set OPENLDAP_REGISTER_SLP="no" in /etc/sysconfig/openldap
- Added patch for OpenLDAP ITS#7796 to avoid excessive
  "not index" logging:
  0011-openldap-re24-its7796.patch
- Replaced openldap-rc.tgz with single source files
- Added soft dependency (Recommends) to cyrus-sasl
- Added soft dependency (Recommends) to cyrus-sasl-devel
  to openldap2-devel
- Added patch for OpenLDAP ITS#8336 (assert in liblmdb):
  0012-openldap-re24-its8336.patch
- Remove obsolete patch 0001-build-adjustments.dif
* Wed Dec  2 2015 hguo@suse.com
- Introduce patch 0010-Revert-Revert-ITS-8240-remove-obsolete-assert.patch
  to fix CVE-2015-6908. (bsc#945582)
- Introduce patch 0011-Enforce-minimum-DH-size-of-1024.patch
  to address weak DH size vulnerability (bsc#937766)
* Mon Nov 30 2015 hguo@suse.com
- Introduce patch 0009-Fix-ldap-host-lookup-ipv6.patch
  to fix an issue with unresponsive LDAP host lookups in IPv6 environment.
  (bsc#955210)
* Fri Oct  9 2015 hguo@suse.com
- Remove OpenLDAP 2.3 code and patches from build source.
  Compatibility libraries for OpenLDAP 2.3 are built in package:
  compat-libldap-2_3-0
  Removed source files:
    openldap-2.3.37-liblber-length-decoding.dif
    openldap-2.3.37-libldap-ntlm.diff
    openldap-2.3.37-libldap-ssl.dif
    openldap-2.3.37-libldap-sasl-max-buff-size.dif
    openldap-2.3.37-libldap-tls_chkhost-its6239.dif
    openldap-2.3.37-libldap-gethostbyname_r.dif
    openldap-2.3.37-libldap-suid.diff
    openldap-2.3.37.dif
    openldap-2.3.37-libldap-ld_defconn-ldap_free_connection.dif
    openldap-2.3.37-libldap-ldapi_url.dif
    openldap-2.3.37.tgz
    openldap-2.3.37-libldap-utf8-ADcanonical.dif
    README.update
    check-build.sh
* Thu Oct  1 2015 hguo@suse.com
- Upgrade to upstream 2.4.42 release with accumulated bug fixes.
* Tue Jul 21 2015 hguo@suse.com
- Upgrade to upstream 2.4.41 release with accumulcated bug fixes and stability improvements.
  * Add patch 0008-In-monitor-backend-do-not-return-Connection0-entries.patch
  * Remove already applied patch 0008-ITS-7723-fix-reference-counting.patch
  * Remove already applied patch 0009-gcc5.patch
  (Implements fate#319301)
* Thu Feb 19 2015 rguenther@suse.com
- Add 0009-gcc5.patch to pass -P to the preprocessor in configure checks
  for Berkeley DB version
* Wed Nov 26 2014 jengelh@inai.de
- binutils is required for "strings" utility invocation in %%pre
  [bnc#904028]
- Remove SLE10 definitions
* Sun Oct 12 2014 jengelh@inai.de
- Use %%_smp_mflags for parallel build
* Mon Sep 22 2014 tchvatal@suse.com
- Add baselibs.conf to sources list
* Wed Sep 10 2014 varkoly@suse.com
- Do not bypass output of useradd and groupadd
* Tue Sep  2 2014 ro@suse.de
- sanitize release line in specfile
* Wed Jul 16 2014 ckornacker@suse.com
- segfault on certain queries with rwm overlay (bnc#846389)
  0008-ITS-7723-fix-reference-counting.patch
* Fri Jun  6 2014 ckornacker@suse.com
- enable systemd slapd service if SysV ldap was enabled (bnc#881476)
* Tue May 13 2014 coolo@suse.com
- use %%_rundir if available, otherwise /var/run
* Wed Apr 23 2014 dmueller@suse.com
- move systemd requires to server package
* Tue Feb 18 2014 ckornacker@suse.com
- Fix systemd service installation
* Sun Feb 16 2014 ro@suse.de
- use configure macro also for building the 2.3.37 version
* Wed Feb 12 2014 varkoly@suse.com
- Remove PidFile from service definition
- Update to 2.4.39
  * Fixed libldap MozNSS crash (ITS#7783)
  * Fixed libldap memory leak with SASL (ITS#7757)
  * Fixed libldap assert in parse_passwdpolicy_control (ITS#7759)
  * Fixed libldap shortcut NULL RDNs (ITS#7762)
  * Fixed libldap deref to use correct control
  * Fixed liblmdb keysizes with mdb_update_key (ITS#7756)
  * Fixed slapd cn=config olcDbConfig modification (ITS#7750)
  * Fixed slapd-bdb/hdb to bail out of search if config is paused (ITS#7761)
  * Fixed slapd-bdb/hdb indexing issue with derived attributes (ITS#7778)
  * Fixed slapd-mdb to bail out of search if config is paused (ITS#7761)
  * Fixed slapd-mdb indexing issue with derived attributes (ITS#7778)
  * Fixed slapd-perl to bail out of search if config is paused (ITS#7761)
  * Fixed slapd-sql to bail out of search if config is paused (ITS#7761)
  * Fixed slapo-constraint handling of softadd/softdel (ITS#7773)
  * Fixed slapo-syncprov assert with findbase (ITS#7749)
  * Build Environment
    Test suite: Use $(MAKE) for tests (ITS#7753)
  * Documentation
    admin24 fix TLSDHParamFile to be correct (ITS#7684)
* Tue Feb 11 2014 varkoly@suse.com
- Add systemd style service definition
- FATE#315028 remove memory limit for slapd
- FATE#315415: LDAP compat packages required for older SLES versions
  For this reson following patches were applied:
  openldap-2.3.37-libldap-suid.diff
  openldap-2.3.37-libldap-ldapi_url.dif
  openldap-2.3.37-libldap-ntlm.diff
  openldap-2.3.37-libldap-gethostbyname_r.dif
  openldap-2.3.37-libldap-sasl-max-buff-size.dif
  openldap-2.3.37-libldap-utf8-ADcanonical.dif
  openldap-2.3.37-liblber-length-decoding.dif
  openldap-2.3.37-libldap-ld_defconn-ldap_free_connection.dif
  openldap-2.3.37-libldap-tls_chkhost-its6239.dif
  openldap-2.3.37-libldap-ssl.dif
* Wed Dec 11 2013 matz@suse.de
- Make /etc/sasl2 owned by openldap2.
* Wed Dec 11 2013 varkoly@suse.com
- Update to 2.4.38
  * Fixed liblmdb nordahead flag (ITS#7734)
  * Fixed liblmdb to check cursor index before cursor_del (ITS#7733)
  * Fixed liblmdb wasted space on split (ITS#7589)
  * Fixed slapd for certs with a NULL issuerDN (ITS#7746)
  * Fixed slapd cn=config with empty nested includes (ITS#7739)
  * Fixed slapd syncrepl memory leak with delta-sync MMR (ITS#7735)
  * Fixed slapd-bdb/hdb to stop processing on dn not found (ITS#7741)
  * Fixed slapd-bdb/hdb with indexed ANDed filters (ITS#7743)
  * Fixed slapd-mdb to stop processing on dn not found (ITS#7741)
  * Fixed slapd-mdb dangling reader (ITS#7662)
  * Fixed slapd-mdb matching rule for OlcDbEnvFlags (ITS#7737)
  * Fixed slapd-mdb with indexed ANDed filters (ITS#7743)
  * Fixed slapd-meta from blocking other threads (ITS#7740)
  * Fixed slapo-syncprov assert with findbase (ITS#7749)
    Changes in 2.4.37
  * Added liblmdb nordahead environment flag (ITS#7725)
  * Fixed client tools CLDAP with IPv6 (ITS#7695)
  * Fixed libldap CLDAP with IPv6 (ITS#7695)
  * Fixed libldap lock ordering with abandon op (ITS#7712)
  * Fixed liblmdb segfault with mdb_cursor_del (ITS#7718)
  * Fixed liblmdb when converting to writemap (ITS#7715)
  * Fixed liblmdb assert on MDB_NEXT with delete (ITS#7722)
  * Fixed liblmdb wasted space on split (ITS#7589)
  * Fixed slapd cn=config with olcTLSProtocolMin (ITS#7685)
  * Fixed slapd-bdb/hdb optimize index updates (ITS#7329)
  * Fixed slapd-ldap chaining with cn=config (ITS#7381, ITS#7434)
  * Fixed slapd-ldap chaning with controls (ITS#7687)
  * Fixed slapd-mdb optimize index updates (ITS#7329)
  * Fixed slapd-meta chaining with cn=config (ITS#7381, ITS#7434)
  * Fixed slapo-constraint to no-op on nonexistent entries (ITS#7692)
  * Fixed slapo-dds assert on startup (ITS#7699)
  * Fixed slapo-memberof to not replicate internal ops (ITS#7710)
  * Fixed slapo-refint to not replicate internal ops (ITS#7710)
    Changes in 2.4.36
  * Added back-meta target filter patterns (ITS#7609)
  * Added liblmdb mdb_txn_env to API (ITS#7660)
  * Fixed libldap CLDAP with uninit'd memory (ITS#7582)
  * Fixed libldap with UDP (ITS#7583)
  * Fixed libldap OpenSSL TLS versions (ITS#7645)
  * Fixed liblmdb MDB_PREV behavior (ITS#7556)
  * Fixed liblmdb transaction issues (ITS#7515)
  * Fixed liblmdb mdb_drop overflow page return (ITS#7561)
  * Fixed liblmdb nested split (ITS#7592)
  * Fixed liblmdb overflow page behavior (ITS#7620)
  * Fixed liblmdb race condition with read and write txns (ITS#7635)
  * Fixed liblmdb mdb_del behavior with MDB_DUPSORT and mdb_del (ITS#7658)
  * Fixed slapd cn=config with unknown schema elements (ITS#7608)
  * Fixed slapd cn=config with loglevel 0 (ITS#7611)
  * Fixed slapd slapi filterlist free behavior (ITS#7636)
  * Fixed slapd slapi control free behavior (ITS#7641)
  * Fixed slapd schema countryString as directoryString (ITS#7659)
  * Fixed slapd schema telephoneNumber as directoryString (ITS#7659)
  * Fixed slapd-bdb/hdb to wait for read locks in tool mode (ITS#6365)
  * Fixed slapd-mdb behavior with alias dereferencing (ITS#7577 )
  * Fixed slapd-mdb modrdn and base-scoped searches (ITS#7604)
  * Fixed slapd-mdb refcount behavior (ITS#7628)
  * Fixed slapd-meta binding flag is set (ITS#7524)
  * Fixed slapd-meta with minimal config (ITS#7581)
  * Fixed slapd-meta missing results messages (ITS#7591)
  * Added slapd-meta TCP keepalive support (ITS#7513)
  * Fixed slapo-sssvlv double free (ITS#7588)
  * Fixed slaptest to list -Q option (ITS#7568)
    Changes in 2.4.35
  * Fixed liblmdb mdb_cursor_put with MDB_MULTIPLE (ITS#7551)
  * Fixed liblmdb page rebalance (ITS#7536)
  * Fixed liblmdb missing parens (ITS#7377)
  * Fixed liblmdb mdb_cursor_del crash (ITS#7553)
  * Fixed slapd syncrepl updateCookie status (ITS#7531)
  * Fixed slapd connection logging (ITS#7543)
  * Fixed slapd segfault on modify (ITS#7542, ITS#7432)
  * Fixed slapd-mdb to reject undefined attrs (ITS#7540)
  * Fixed slapo-pcache with +/- attrsets (ITS#7552)
    Changes in 2.4.34
  * Fixed libldap connections with EINTR (ITS#7476)
  * Fixed libldap lineno overflow in ldif_read_record (ITS#7497)
  * Fixed liblmdb mdb_env_open flag handling (ITS#7453)
  * Fixed liblmdb mdb_midl_sort array optimization (ITS#7432)
  * Fixed liblmdb freelist with large entries (ITS#7455)
  * Fixed liblmdb to check for filled dirty page list (ITS#7491)
  * Fixed liblmdb to validate data limits (ITS#7485)
  * Fixed liblmdb mdb_update_key for large keys (ITS#7505)
  * Fixed ldapmodify to not core dump with invalid LDIF (ITS#7477)
  * Fixed slapd syncrepl for old entries in MMR setup (ITS#7427)
  * Fixed slapd signedness for index_substr_any_* (ITS#7449)
  * Fixed slapd enforce SLAPD_MAX_DAEMON_THREADS (ITS#7450)
  * Fixed slapd mutex in send_ldap_ber (ITS#6164)
  * Added slapd-ldap onerr option (ITS#7492)
  * Added slapd-ldap keepalive support (ITS#7501)
  * Fixed slapd-ldif with empty dir (ITS#7451)
  * Fixed slapd-mdb to reopen attr DBs after env reopen (ITS#7416)
  * Fixed slapd-mdb handling of missing entries (ITS#7483,7496)
  * Fixed slapd-mdb environment flag setting (ITS#7452)
  * Fixed slapd-mdb with sub db slapcat (ITS#7469)
  * Fixed slapd-mdb to correctly work with toolthreads > 2 (ITS#7488,ITS#7527)
  * Fixed slapd-mdb subtree search speed (ITS#7473)
  * Fixed slapd-meta conversion to cn=config (ITS#7525)
  * Fixed slapd-meta segfault when modifying olcDbUri (ITS#7526)
  * Fixed slapd-sql back-config support (ITS#7499)
  * Fixed slapo-constraint handle uri and restrict correctly (ITS#7418)
  * Fixed slapo-constraint with multi-master replication (ITS#7426)
  * Fixed slapo-constraint segfault (ITS#7431)
  * Fixed slapo-deref control initialization (ITS#7436)
  * Fixed slapo-deref control exposure (ITS#7445)
  * Fixed slapo-memberof with internal ops (ITS#7487)
  * Fixed slapo-pcache matching rules for config db (ITS#7459)
  * Fixed slapo-rwm modrdn cleanup (ITS#7414)
  * Fixed slapo-sssvlv maxperconn parameter (ITS#7484)
* Mon Jun 17 2013 jengelh@inai.de
- For now, avoid automatic use of libdb-6_0 by explicitly selecting
  libdb-4_8 as BuildRequire.
* Mon Mar 25 2013 jengelh@inai.de
- Put static libs into openldap2-devel-static and relieve
  openldap2-devel of static-only deps
* Sat Nov 17 2012 ro@suse.de
- fix check-build.sh for kernel > 3.0
* Fri Nov 16 2012 rhafer@suse.com
- Fixed initscript to avoid endless loop when no configuration
  is present in /etc/openldap/slapd.d/ (bnc#767464)
- cleaned up SLES10 buildrequires and dependencies
- removed support for building on SLES9, didn't work anyway anymore
- Don't buildrequire krb5-mini on Distributions where it does not
  exist
* Fri Oct 26 2012 rhafer@suse.com
- enabled mdb backend
- Update to 2.4.33
  * Added slapd-meta cn=config support
  * Fixed slapd alock handling on Windows (ITS#7361)
  * Fixed slapd acl handling with zero-length values (ITS#7350)
  * Fixed slapd syncprov to not reference ops inside a lock (ITS#7172)
  * Fixed slapd delta-syncrepl MMR with large attribute values (ITS#7354)
  * Fixed slapd slapd_rw_destroy function (ITS#7390)
  * Fixed slapd-ldap idassert bind handling (ITS#7403)
  * Fixed slapo-constraint with multiple modifications (ITS#7168)
  Changes in 2.4.32:
  * Added slappasswd loadable module support (ITS#7284)
  * Fixed tools to not clobber SASL_NOCANON (ITS#7271)
  * Fixed libldap function declarations (ITS#7293)
  * Fixed libldap double free (ITS#7270)
  * Fixed libldap debug level setting (ITS#7290)
  * Fixed libldap gettime() regression (ITS#6262)
  * Fixed libldap sasl handling (ITS#7118, ITS#7133)
  * Fixed libldap to correctly free socket with TLS (ITS#7241)
  * Fixed slapd config index renumbering (ITS#6987)
  * Fixed slapd duplicate error response (ITS#7076)
  * Fixed slapd parsing of PermissiveModify control (ITS#7298)
  * Fixed slapd-bdb/hdb cache hang under high load (ITS#7222)
  * Fixed slapd-bdb/hdb alias checking (ITS#7303)
  * Fixed slapd-bdb/hdb olcDbConfig changes work immediately (ITS#7338)
  * Fixed slapd-ldap to encode user DN during password change (ITS#7319)
  * Fixed slapd-ldap assertion when proxying to MS AD (ITS#6851)
  * Fixed slapd-ldap monitoring (ITS#7182, ITS#7225)
  * Fixed slapd-perl panic (ITS#7325)
  * Fixed slapo-accesslog memory leaks with sync replication (ITS#7292)
  * Fixed slapo-syncprov memory leaks with sync replication (ITS#7292)
* Fri Oct 26 2012 coolo@suse.com
- add explicit buildrequire on groff - needed to build manuals
* Tue Oct 16 2012 coolo@suse.com
- buildrequire krb5-mini in openldap2-client to avoid cycle
- move Summary out of the %%if as prepare_spec is confused about
  the license otherwise
* Thu May 10 2012 rhafer@suse.de
- update to 2.4.31
  * Added slapo-accesslog support for reqEntryUUID (ITS#6656)
  * Fixed libldap IPv6 URL detection (ITS#7194)
  * Fixed libldap rebinding on failed connection (ITS#7207)
  * Fixed slapd listener initialization (ITS#7233)
  * Fixed slapd cn=config with olcTLSVerifyClient (ITS#7197)
  * Fixed slapd delta-syncrepl fallback on non-leaf error (ITS#7195)
  * Fixed slapd to reject MMR setups with bad serverID setting
    (ITS#7200)
  * Fixed slapd approxIndexer key generation (ITS#7203)
  * Fixed slapd modification of olcSuffix (ITS#7205)
  * Fixed slapd schema validation with missing definitions
    (ITS#7224)
  * Fixed slapd syncrepl -c with supplied CSN values (ITS#7245)
  * Fixed slapd-bdb/hdb idlcache with only one element (ITS#7231)
  * Fixed slapo-accesslog deadlock with non-logged write ops
    (ITS#7088)
  * Fixed slapo-syncprov sessionlog check (ITS#7218)
  * Fixed slapo-syncprov entry leak (ITS#7234)
  * Fixed slapo-syncprov startup initialization (ITS#7235)
* Mon Apr 23 2012 rhafer@suse.de
- Disabled testsuite for now. Causes problems in the buildserivce
* Tue Mar  6 2012 rhafer@suse.de
- Update to 2.4.30
  * Fixed libldap socket polling for writes (ITS#7167)
  * Fixed liblutil string modifications (ITS#7174)
  * Fixed slapd crash when attrsOnly is true (ITS#7143)
  * Fixed slapd syncrepl delete handling (ITS#7052,ITS#7162)
  * Fixed slapo-pcache time-to-refesh handling (ITS#7178)
  * Fixed slapo-syncprov loop detection (ITS#6024)
* Mon Feb 27 2012 rhafer@suse.de
- Update to 2.4.29
  * Fixed slapd cn=config modification of first schema element
    (ITS#7098)
  * Fixed slapd operation reuse (ITS#7107)
  * Fixed slapd blocked writers to not interfere with pool pause
    (ITS#7115)
  * Fixed slapd connection loop connindex usage (ITS#7131)
  * Fixed slapd double mutex unlock via connection_done (ITS#7125)
  * Fixed slapd check order in connection_write (ITS#7113)
  * Fixed slapd slapadd to exit on failure (ITS#7142)
  * Fixed slapd syncrepl reference to freed memory
    (ITS#7127,ITS#7132)
  * Fixed slapd syncrepl to ignore some errors on delete
    (ITS#7052)
  * Fixed slapd syncrepl to handle missing oldRDN (ITS#7144)
  * Fixed slapd-monitor compare op to update cached entry
    (ITS#7123)
  * Fixed slapo-syncprov with already abandoned operation
    (ITS#7150)
- Included patches from RE24 branch:
  * only poll sockets for write as needed (ITS#7167, bnc#749082)
  * sycnrepl Fixes (ITS#7162)
* Wed Dec  7 2011 cfarrell@suse.com
- license update: OLDAP-2.8
  SPDX format (http://www.spdx.org/licenses)
* Fri Dec  2 2011 rhafer@suse.de
- Update to 2.4.28
  * Fixed back-mdb out of order slapadd (ITS#7090)
  changes in OpenLDAP 2.4.27 Release (2011/11/24):
  * Added slapd delta-syncrepl MMR (ITS#6734,ITS#7029,ITS#7031)
  * Fixed ldapmodify crash with LDIF controls (ITS#7039)
  * Fixed ldapsearch to honor timeout and timelimit (ITS#7009)
  * Fixed libldap endless looping (ITS#7035)
  * Fixed libldap TLS to not check hostname when using 'allow'
    (ITS#7014)
  * Fixed slapadd common code into slapcommon (ITS#6737)
  * Fixed slapd backend connection initialization (ITS#6993)
  * Fixed slapd frontend DB parsing in cn=config (ITS#7016)
  * Fixed slapd hang with {numbered} overlay insertion (ITS#7030)
  * Fixed slapd inet_ntop usage (ITS#6925)
  * Fixed slapd cn=config deletion of bitmasks (ITS#7083)
  * Fixed slapd cn=config modify replace/delete crash (ITS#7065)
  * Fixed slapd schema UTF8StringNormalize with 0 length values
    (ITS#7059)
  * Fixed slapd with dynamic acls for cn=config (ITS#7066)
  * Fixed slapd response callbacks (ITS#6059,ITS#7062)
  * Fixed slapd no_connection warnings with ldapi
    (ITS#6548,ITS#7092)
  * Fixed slapd return code processing (ITS#7060)
  * Fixed slapd sl_malloc various issues (ITS#6437)
  * Fixed slapd startup behavior (ITS#6848)
  * Fixed slapd syncrepl crash with non-replicated ops (ITS#6892)
  * Fixed slapd syncrepl with modrdn (ITS#7000,ITS#6472)
  * Fixed slapd syncrepl timeout when using refreshAndPersist
    (ITS#6999)
  * Fixed slapd syncrepl deletes need a non-empty CSN (ITS#7052)
  * Fixed slapd syncrepl glue for empty suffix (ITS#7037)
  * Fixed slapd results cleanup (ITS#6763,ITS#7053)
  * Fixed slapd validation of args for TLSCertificateFile
    (ITS#7012)
  * Fixed slapd-bdb/hdb to build entry DN based on parent DN
    (ITS#5326)
  * Fixed slapd-hdb with zero-length entries (ITS#7073)
  * Fixed slapd-hdb duplicate entries in subtree IDL cache
    (ITS#6983)
  * Fixed slapo-pcache response cleanup (ITS#6981)
  * Fixed slapo-ppolicy pwdAllowUserChange behavior (ITS#7021)
  * Fixed slapo-sssvlv issue with greaterThanorEqual (ITS#6985)
  * Fixed slapo-sssvlv to only return requested attrs (ITS#7061)
  * Fixed slapo-syncprov DSA attribute filtering for Persist mode
    (ITS#7019)
  * Fixed slapo-syncprov when consumer has newer state of our SID
    (ITS#7040)
  * Fixed slapo-syncprov crash (ITS#7025)
  * Added missing LDIF form of schema files (ITS#7063)
* Fri Nov 25 2011 coolo@suse.com
- add libtool as buildrequire to avoid implicit dependency
* Mon Oct 24 2011 rhafer@suse.de
- ACL changes to the config database only got active after slapd
  restart in certain cases (bnc#716895, ITS#7066).
- Adjusted default DB_CONFIG to increase max values for locks and
  lock objects (bnc#719803)
- Fix UTF8StringNormalize overrun on zero-length string
  (bnc#724201, ITS#7059)
* Thu Jul  7 2011 rhafer@suse.de
- Update to 2.4.26
  * Added libldap LDAP_OPT_X_TLS_PACKAGE (ITS#6969)
  * Fixed libldap descriptor leak (ITS#6929)
  * Fixed libldap socket leak (ITS#6930)
  * Fixed libldap get option crash (ITS#6931)
  * Fixed libldap lockup (ITS#6898)
  * Fixed libldap ASYNC TLS setup (ITS#6828)
  * Fixed libldap with missing \n terminations (ITS#6947)
  * Fixed tools double free (ITS#6946)
  * Fixed tools verbose output (ITS#6977)
  * Fixed ldapmodify SEGV on invalid LDIF (ITS#6978)
  * Added slapd extra_attrs database option (ITS#6513)
  * Fixed slapd asserts (ITS#6932)
  * Fixed slapd configfile param on windows (ITS#6933)
  * Fixed slapd config with global chaining (ITS#6843)
  * Fixed slapd uninitialized variables (ITS#6935)
  * Fixed slapd config objectclass is readonly (ITS#6963)
  * Fixed slapd entry response with control (ITS#6899)
  * Fixed slapd with unknown attrs (ITS#6819)
  * Fixed slapd normalization of schema RDN (ITS#6967)
  * Fixed slapd operations cache to 10 op limit (ITS#6944)
  * Fixed slapd syncrepl crash with non-replicated ops (ITS#6892)
  * Fixed slapd-bdb/hdb with sparse index ranges (ITS#6961)
  * Fixed back-ldap ppolicy updates (ITS#6711)
  * Fixed back-ldap with id-assert (ITS#6817)
  * Fixed various slapo-pcache issues (ITS#6823, ITS#6950,
    ITS#6951, ITS#6953, ITS#6954)
  * Fixed slapo-pcache database corruption (ITS#6831)
  * Fixed slapo-syncprov with replicated subtrees (ITS#6872)
- backported delete support for child entries of overlays from
  master (bnc#704398)
* Tue Mar 29 2011 rhafer@suse.de
- Updated to 2.4.25, important changes:
  * Fixed ldapsearch pagedresults loop (ITS#6755)
  * Fixed tools for incompatible args (ITS#6849)
  * Fixed libldap MozNSS crash (ITS#6863)
  * Fixed slapd add objectclasses in order (ITS#6837)
  * Added slapd ordering for uidNumber and gidNumber (ITS#6852)
  * Fixed slapd segfault when adding values out of order (ITS#6858)
  * Fixed slapd sortval handling (ITS#6845)
  * Fixed slapd-bdb with slapadd/index quick option (ITS#6853)
  * Fixed slapd-ldap chain cn=config support (ITS#6837)
  * Fixed slapd-ldap chain with slapd.conf (ITS#6857)
  * Fixed slapd-meta deadlock (ITS#6846)
  * Fixed slapo-sssvlv with multiple requests (ITS#6850)
  * Fixed contrib/lastbind install rules (ITS#6238)
  * Fixed contrib/cloak install rules (ITS#6877)
* Tue Feb 22 2011 rhafer@suse.de
- Surpress gcc warnings about extra format string arguments for 2.3.x
  built as well.
* Mon Feb 14 2011 rhafer@suse.de
- Updated to 2.4.24, important changes:
  * Added libldap_r,libldap formal concurrency API (ITS#6625,ITS#5421)
  * Added slapadd attribute value checking (ITS#6592)
  * Added slapcat continue mode for problematic DBs (ITS#6482)
  * Added slapd syncrepl suffixmassage support (ITS#6781)
  * Fixed liblber to not close invalid sockets (ITS#6585)
  * Fixed libldap referral chasing (ITS#6602)
  * Fixed libldap leak when chasing referrals (ITS#6744)
  * Fixed slapd acl parsing overflow (ITS#6611)
  * Fixed slapd acl when resuming parsing (ITS#6804)
  * Fixed slapd default config acls with overlays (ITS#6822)
  * Fixed slapd config leak with olcDbDirectory (ITS#6634)
  * Fixed slapd when first acl is value dependent (ITS#6693)
  * Fixed slapd-bdb slapadd -q with glued dbs (ITS#6794)
  * Fixed slapo-ppolicy don't update opattrs on consumers (ITS#6608)
  * Fixed slapo-ppolicy to allow userPassword deletion (ITS#6620)
  * Fixed slapo-syncprov to send error if consumer is newer (ITS#6606)
  * Fixed slapo-syncprov filter race condition (ITS#6708)
  * Fixed slapo-syncprov active mod race (ITS#6709)
  * Fixed slapo-syncprov to refresh if context is dirty (ITS#6710)
  * Fixed slapo-syncprov CSN updates to all replicas (ITS#6718)
  * Fixed slapo-syncprov sessionlog ordering (ITS#6716)
  * Fixed slapo-syncprov sessionlog with adds (ITS#6503)
  * Fixed slapo-syncprov mutex (ITS#6438)
  * Fixed slapo-syncprov mincsn check with MMR (ITS#6717)
  * Fixed slapo-syncprov control leak (ITS#6795)
  * Fixed slapo-syncprov error codes (ITS#6812)
  * For a comprehensive list of changes please consult the CHANGES
    file
- removed unneeded openSUSE 11.0 specifc patch
* Tue Feb  1 2011 rhafer@suse.de
- slapadd -q could crash for glued bdb/hdb databases
* Wed Jan 19 2011 rhafer@suse.de
- Install the correct schema2ldif script (bnc#665530)
* Wed Jan  5 2011 rhafer@novell.com
- Fixed quotation in init-script to avoid errors when calling it
  from within /etc/openldap/slapd.d/cn=config/ (bnc#660492).
* Fri Nov 12 2010 rhafer@novell.com
- Surpress gcc warnings about extra format string arguments.
- Split-off openldap2-doc (noarch) package (Admin Guide and IDs)
- Backported -VVV commandline switch for slapd from HEAD
  (to list enabled static overlays)
- Build all overlays except syncprov and ppolicy as dynamic modules
  (Fixes bnc#648479, FATE#307837)
- Added README.dynamic-overlays to point out some details about
  dynamic overlays
- simplified pie-compile patch and adjusted it to work with
  dynamic overlays
* Tue Oct  5 2010 rhafer@novell.com
- Handle the libdb-4_5 -> libdb-4_8 Version update by opening the
  Databases with DB_RECOVER if a version mismatch is detected.
* Sun Oct  3 2010 cristian.rodriguez@opensuse.org
- Do not include Build date and time in binaries, this
  avoids build-compare failures and unhelpful rebuilds/republishes
* Wed Sep 29 2010 rhafer@novell.com
- Don't build 2.3 slapcat anymore for 11.3 and newer. We switch to
  2.4 long ago.
- Removed automatic 2.3->2.4 migration in %%post
- moved back-sql examples to make rpmlint happy
* Thu Aug 26 2010 rhafer@novell.com
- Fix listener URIs in init script to make SLP registration work
  again (bnc#620389)
* Fri Jul 23 2010 rhafer@novell.com
- Fixed RPM Group and Summary Tags (bnc#624980)
* Thu Jul  1 2010 rhafer@novell.com
- Updated to 2.4.23:
  * Fixed libldap to return server's error code (ITS#6569)
  * Fixed libldap memleaks (ITS#6568)
  * Fixed liblutil off-by-one with delta (ITS#6541)
  * Fixed slapd acls with glued databases (ITS#6468)
  * Fixed slapd syncrepl rid logging (ITS#6533)
  * Fixed slapd modrdn handling of invalid values (bnc#612430,
    ITS#6570)
  * Fixed slapd-bdb hasSubordinates computation (ITS#6549)
  * Fixed slapd-bdb to use memcpy instead for strcpy (ITS#6474)
  * Fixed slapd-bdb entry cache delete failure (ITS#6577)
  * Fixed slapd-ldap to return control responses (ITS#6530)
  * Fixed slapo-ppolicy to use Debug (ITS#6566)
  * Fixed slapo-refint to zero out freed DN vals (ITS#6572)
  * Fixed slapo-rwm to use Debug (ITS#6566)
  * Fixed slapo-sssvlv to use Debug (ITS#6566)
  * Fixed slapo-syncprov lost deletes in refresh phase (bnc#606294,
    ITS#6555)
  * Fixed slapo-valsort to use Debug (ITS#6566)
  * Fixed contrib/nssov network.c missing patch (ITS#6562)
- New subpackage openldap2-back-sql. Contains the SQL backend
  module plus some documentation (bnc#395719)
- generate Patches from git tree (resulted in all patches being
  renamed)
- installing binaries without stripping them is done by setting
  the STRIP enviroment variable instead for patching the Makefile
  now
- Fixed a bug in the syncprov overlay which could lead to not
  replicate delete Operations (ITS#6555, bnc#606294)
- BuildRequires cleanup
* Thu Jul  1 2010 rhafer@novell.com
- LDAP clients could crash the server by submitting a specially
  crafted LDAP ModRDN operation.  (bnc#612430, ITS#6570)
- Delete Operations happening during the "Refresh" phase of
  "refreshAndPersist" replication failed to replicate under
  certain circumstances (bnc#606294, ITS#6555)
* Mon May 10 2010 rhafer@novell.com
- Create /var/run/slapd on demand. /var/run might be mounted on
  tmpfs.
* Thu Apr 15 2010 adrian@suse.de
- fix build dependency cycle for -client package with openslp
* Wed Mar 17 2010 rhafer@novell.com
- Fixed quotation in sed expression to escape ldapi path in init
  script
* Tue Mar 16 2010 rhafer@novell.com
- Removed obsolete hunk from openldap2.dif
- Remove ldap.conf patch to use saner default for Certificate
  verification (bnc#575146)
* Sat Feb 13 2010 rguenther@suse.de
- Add fix for stricter fortification checks of GCC 4.5.
* Thu Jan  7 2010 rhafer@novell.com
- Updated to 2.4.21:
  * Fixed liblutil for negative microsecond offsets (ITS#6405)
  * Fixed slapd global settings to work without restart (ITS#6428)
  * Fixed slapd looping with SSL/TLS connections (ITS#6412)
  * Fixed slapd syncrepl freeing tasks from queue (ITS#6413)
  * Fixed slapd syncrepl parsing of tls defaults (ITS#6419)
  * Fixed slapd syncrepl uninitialized variables (ITS#6425)
  * Fixed slapd-config Adds with Abstract classes (ITS#6408)
  * Fixed slapo-dynlist behavior with simple filters (ITS#6421)
  * Fixed slapd-ldif access outside database directory (ITS#6414)
  * Fixed slapo-translucent with back-null (ITS#6403)
  * Fixed slapo-unique criteria checking (ITS#6270)
- removed some obsolete RPM dependencies
- Added missing tags to init script to silence rpmlint warnings
* Thu Dec 10 2009 rhafer@novell.com
- Fixed an issue in back-config's objectclass inheritence code that
  could cause the server to fail to start or to spin in an endless
  loop (bnc#558059,ITS#6408)
- default the tls_reqcert parameter of a syncrepl config to
  "demand" as documented even if other tls_ options are absent
  (bnc#558397, ITS#6319)
- apply changes to the global size and timelimits to all database
  that don't specify limits themself. (bnc#562184, ITS#6428)
* Mon Nov 30 2009 rhafer@novell.com
- Update to 2.4.20 (fate#306593), most important fixes since 2.4.19
  * Fixed liblber embedded NUL values in BerValues (ITS#6353)
  * Fixed libldap sasl buffer sizing (ITS#6327,ITS#6334)
  * Fixed libldap uninitialized return value (ITS#6355)
  * Fixed libldap unlimited timeout (ITS#6388)
  * Added slapd handling of hex server IDs (ITS#6297)
  * Fixed slapd checks of str2filter (ITS#6391)
  * Fixed slapd configArgs initialization (ITS#6363)
  * Fixed slapd db_open with connection_fake_init (ITS#6381)
  * Fixed slapd with embedded \0 in bervals (ITS#6378,ITS#6379)
  * Fixed slapd inclusion of ac/unistd.h (ITS#6342)
  * Fixed slapd sl_free to better reclaim memory (ITS#6380)
  * Fixed slapd syncrepl deletes in MirrorMode (ITS#6368)
  * Fixed slapd syncrepl to use correct SID (ITS#6367)
  * Fixed slapd tls_accept to retry in certain cases (ITS#6304)
  * Fixed slapd-bdb/hdb cache corruption (ITS#6341)
  * Fixed slapd-bdb/hdb entry cache (ITS#6360)
  * Fixed slapo-syncprov checkpoint conversion (ITS#6370)
  * Fixed slapo-syncprov deadlock (ITS#6335)
  * Fixed slapo-syncprov out of order changes (ITS#6346)
- Added switch to enable/disable testsuite (%%run_test_suite)
* Tue Nov  3 2009 coolo@novell.com
- updated patches to apply with fuzz=0
* Mon Sep 28 2009 rhafer@novell.com
- Added schema2ldif tool to openldap2-client subpackage
  (bnc#541819)
* Wed Sep 23 2009 rhafer@novell.com
- Changed permissions on /var/run/slapd to a saner default for
  ldapi:/// (bnc#536729)
* Wed Sep  9 2009 rhafer@novell.com
- libldap's check of the hostname against the TLS Certificate's CN
  Attribute did not handle possible NUL bytes in the CN correctly
  and was vulnerable against attacks with spoofed Certificates.
  (bnc#537143, ITS#6239)
* Tue Jul 14 2009 rhafer@novell.com
- Update to 2.4.17. Most important changes:
  * Fixed liblber to use ber_strnlen (ITS#6080)
  * Fixed libldap openssl digest initialization (ITS#6192)
  * Fixed libldap tls NULL error messages (ITS#6079)
  * Added slapd sasl auxprop support (ITS#6147)
  * Added slapd schema checking tool (ITS#6150)
  * Added slapd writetimeout keyword (ITS#5836)
  * Fixed slapd abandon/cancel handling for some ops (ITS#6157)
  * Fixed slapd access setstyle to expand (ITS#6179)
  * Fixed slapd assert with closing connections (ITS#6111)
  * Fixed slapd bind race condition (ITS#6189)
  * Fixed slapd cert validation (ITS#6098)
  * Fixed slapd connection_destroy assert (ITS#6089)
  * Fixed slapd csn normalization (ITS#6195)
  * Fixed slapd errno handling (ITS#6037)
  * Fixed slapd hung writers (ITS#5836)
  * Fixed slapd ldapi issues (ITS#6056)
  * Fixed slapd normalization of updated schema attributes (ITS#5540)
  * Fixed slapd olcLimits handling (ITS#6159)
  * Fixed slapd olcLogLevel with hex levels (ITS#6162)
  * Fixed slapd sending cancelled operations results (ITS#6103)
  * Fixed slapd slapi_entry_has_children (ITS#6132)
  * Fixed slapd sockets usage on windows (ITS#6039)
  * Fixed slapd some abandon and cancel race conditions (ITS#6104)
  * Fixed slapd tls context after changes (ITS#6135)
  * Fixed slapd-bdb/hdb adjust dncachesize if too low (ITS#6176)
  * Fixed slapd-bdb/hdb crashes during delete (ITS#6177)
  * Fixed slapd-bdb/hdb multiple olcIndex for same attr (ITS#6196)
  * Fixed slapd-hdb freeing of already freed entries (ITS#6074)
  * Fixed slapd-hdb entryinfo cleanup (ITS#6088)
  * Fixed slapd-hdb dncache lockups (ITS#6095)
  * Fixed slapd-ldap deadlock with non-responsive TLS URIs (ITS#6167)
  * Fixed slapo-ppolicy to honor pwdLockout (ITS#6168)
  * Fixed slapo-ppolicy to return check modules error message (ITS#6082)
  * Added slapo-rwm rwm-drop-unrequested-attrs config option (ITS#6057)
  * Fixed slapo-rwm dn passing (ITS#6070)
  * Fixed slapo-rwm entry free/release (ITS#6058, ITS#6081)
  * Fixed tools returning ldif errors (ITS#5892)
- Backported fix for failing back-monitor test from HEAD
- re-enabled some formerly disabled tests from the testsuite
* Mon Jun 29 2009 rhafer@novell.com
- Fixed Summary/Description for -client subpackage
* Thu Jun 25 2009 rhafer@novell.com
- Improved connection check in init script (bnc#510295)
* Mon Jun 15 2009 rhafer@novell.com
- Fixed complilation with newer glibc (2.3.X release needs
  GNU_SOURCE defined as well in getpeerid.c)
* Wed Apr 29 2009 rhafer@novell.com
- gcc 4.4 fixes
* Mon Apr  6 2009 rhafer@suse.de
- Update to 2.4.16. Most important fixes:
  * Fixed libldap segfault in checking cert/DN (ITS#5976)
  * Fixed libldap peer cert double free (ITS#5849)
  * Fixed libldap referral chasing (ITS#5980)
  * Fixed slapd backglue with empty DBs (ITS#5986)
  * Fixed slapd ctxcsn race condition (ITS#6001)
  * Fixed slapd debug message (ITS#6027)
  * Fixed slapd redundant module loading (ITS#6030)
  * Fixed slapd schema_init freed value (ITS#6036)
  * Fixed slapd syncrepl newCookie sync messages (ITS#5972)
  * Fixed slapd syncrepl hang during shutdown (ITS#6011)
  * Fixed slapd syncrepl too many MMR messages (ITS#6020)
  * Fixed slapd syncrepl skipped entries with MMR (ITS#5988)
  * Fixed slapd-bdb/hdb cachesize handling (ITS#5860)
  * Fixed slapd-bdb/hdb with slapcat with empty dn (ITS#6006)
  * Fixed slapd-bdb/hdb with NULL transactions (ITS#6012)
  * Fixed slapd-ldap incorrect referral handling (ITS#6003,ITS#5916)
  * Fixed slapd-ldap/meta with broken AD results (ITS#5977)
  * Fixed slapd-ldap/meta with invalid attrs again (ITS#5959)
  * Fixed slapo-accesslog interaction with ppolicy (ITS#5979)
  * Fixed slapo-dynlist conversion to cn=config (ITS#6002)
  * Fixed various slapo-syncprov issues (ITS#5972, ITS#6020,
    ITS#5985, ITS#5999, ITS#5973, ITS#6045, ITS#6024, ITS#5988)
- Fix building on older openSUSE releases
* Fri Mar 20 2009 rhafer@suse.de
- Update to 2.4.15. Most important changes:
  * Fixed slapd bconfig conversion again (ITS#5346)
  * Fixed slapd behavior with superior objectClasses again (ITS#5517)
  * Fixed slapd RFC4512 behavior with same attr in RDN (ITS#5968)
  * Fixed slapd corrupt contextCSN (ITS#5947)
  * Fixed slapd syncrepl order to match on add/delete (ITS#5954)
  * Fixed slapd adding rdn with other values (ITS#5965)
  * Fixed slapd-bdb/hdb behavior with unallocatable shm (ITS#5956)
  * Fixed slapd-ldap/meta with entries with invalid attrs (ITS#5959)
  * Fixed slapo-pcache caching invalid entries (ITS#5927)
  * Fixed slapo-syncprov csn updates (ITS#5969)
  * Added libldap option to disable SASL host canonicalization (ITS#5812)
  * Fixed libldap chasing multiple referrals (ITS#5853)
  * Fixed libldap setuid usage with .ldaprc (ITS#4750)
  * Fixed libldap deref handling (ITS#5768)
  * Fixed libldap NULL pointer deref (ITS#5934)
  * Fixed libldap peer cert memory leak (ITS#5849)
  * Fixed libldap intermediate response behavior (ITS#5896)
  * Fixed libldap IPv6 address handling (ITS#5937)
  * Fixed libldap_r deref building (ITS#5768)
  * Fixed libldap_r slapd lockup when paused during shutdown (ITS#5841)
  * Fixed slapd acl checks on ADD (ITS#4556,ITS#5723)
  * Fixed slapd acl application to newly created backends (ITS#5572)
  * Fixed slapd bconfig to return error codes (ITS#5867)
  * Fixed slapd bconfig encoding incorrectly (ITS#5897)
  * Fixed slapd bconfig dangling pointers (ITS#5924)
  * Fixed slapd epoll handling (ITS#5886)
  * Fixed slapd glue with MMR (ITS#5925)
  * Fixed slapd listener comparison (ITS#5613)
  * Fixed various syncrepl issues (ITS#5809,ITS#5850, ITS#5843,
    ITS#5866, ITS#5901, ITS#5881, ITS#5935, ITS#5710,
    ITS#5781, ITS#5809, ITS#5798, ITS#5826)
  * Fixed slapd-bdb/hdb dncachesize handling (ITS#5860)
  * Fixed slapd-bdb/hdb trickle task usage (ITS#5864)
  * Fixed slapd-hdb idlcache with empty suffix (ITS#5859)
* Wed Jan  7 2009 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)
* Fri Dec 12 2008 rhafer@suse.de
- Fixed openldap2-devel dependencies (bnc#457989)
* Tue Dec  9 2008 rhafer@suse.de
- Fixed a bug in the threadpool implementation that could cause
  slapd to lockup when shutting down while the pool is paused.
  (bnc#450457, ITS#5841)
* Fri Nov 28 2008 rhafer@suse.de
- Disable the slapadd trickle-task it cause performance issues
  when using libdb-4.5 (bnc#449641)
- removed obsolete configure option (ldbm backend does not exist
  in OpenLDAP 2.4)
* Fri Nov 21 2008 ro@suse.de
- update check-build.sh
* Wed Nov  5 2008 rhafer@suse.de
- Fixed database shutdown sequence (bnc#441774, ITS#5745)
* Tue Nov  4 2008 rhafer@suse.de
- Handle ldbm databases in updates from 2.3 release (bnc#440589)
* Thu Oct 23 2008 rhafer@suse.de
- the helper function to create various LDAP controls returned
  wrong error codes under certain circumstances
  (bnc#429064, ITS#5762)
- Fixed referral chasing in chain-overlay (bnc#438088, ITS#5742)
- Fixed back-config integration of overlays with private instances
  of databases (translucent, chain, ...) (bnc#438094, ITS#5736)
* Mon Oct 13 2008 rhafer@suse.de
- Added missing #include to slapo-collect
* Sun Oct 12 2008 rhafer@suse.de
- Update to 2.4.12. Most important changes:
  * Fixed libldap ldap_utf8_strchar arguments (ITS#5720)
  * Fixed libldap TLS_CRLFILE (ITS#5677)
  * Fixed librewrite memory handling (ITS#5691)
  * Fixed slapd attribute leak (ITS#5683)
  * Fixed slapd config backend with index greater than sibs (ITS#5684)
  * Fixed slapd custom attribute inheritance (ITS#5642)
  * Fixed slapd firstComponentMatch normalization (ITS#5634)
  * Fixed slapd connection events enabled twice (ITS#5725)
  * Fixed slapd memory handling (ITS#5691)
  * Fixed slapd objectClass canonicalization (ITS#5681)
  * Fixed slapd objectClass termination (ITS#5682)
  * Fixed slapd overlay control registration (ITS#5649)
  * Fixed slapd runqueue checking (ITS#5726)
  * Fixed slapd sortvals comparison (ITS#5578)
  * Fixed slapd syncrepl contextCSN detection (ITS#5675)
  * Fixed slapd syncrepl error logging (ITS#5618)
  * Fixed slapd syncrepl runqueue interval (ITS#5719)
  * Fixed slapd-bdb entry return if attr not present (ITS#5650)
  * Fixed slapd-bdb/hdb release search entries earlier (ITS#5728,ITS#5730)
  * Fixed slapd-bdb/hdb subtree search with empty suffix (ITS#5729)
  * Fixed slapo-memberof internal operations DN (ITS#5622)
  * Fixed slapo-pcache attrset crash (ITS#5665)
  * Fixed slapo-pcache caching with invalid schema (ITS#5680)
  * Fixed slapo-ppolicy control return on password modify exop (ITS#5711)
- removed obsolete patches
* Mon Oct  6 2008 rhafer@suse.de
- remove some problematic test-cases, that cause a lot of
  unreproducable buildfailures
- check for exisitence of /etc/openldap/slapd.conf in init-script
  assume back-config usage if it isn't present (bnc#428168)
* Wed Sep 24 2008 rhafer@suse.de
- Mark Schema and SuSEfirewall files as %%config
- openldap2-back-perl requires perl
- Give more meaningful error messages when index configuration
  fails (bnc#429150)
* Fri Sep 19 2008 rhafer@suse.de
- Reduced debug-level during "make test" to reduce required disk
  space and buildtime
* Thu Sep 18 2008 rhafer@suse.de
- Fixed init-script dependencies (bnc#426214)
* Fri Sep 12 2008 rhafer@suse.de
- Backported fix for a crash in back-config when adding entries with
  a too large index (ITS#5684)
- Backported fix for a crash when adding an invalid olcBdbConfig
  Entry to back-config (ITS#5698)
* Tue Sep  9 2008 rhafer@suse.de
- Removed getaddrinfo workaround. Recent glibc doesn't need it
  anymore (bnc#288879, ITS#5251)
- Server requires libldap of the same version.
* Mon Sep  8 2008 rhafer@suse.de
- Import back-config support for deleting databases from CVS HEAD
* Tue Sep  2 2008 rhafer@suse.de
- Dropped evolution specific ntlm-bind Patch (Fate#303480)
* Thu Aug 28 2008 rhafer@suse.de
- added ldapns.schema , to allow to use pam_ldap's "check_host_attr"
  and "check_service_attr" features (bnc#419984)
- backport overlay_register_control fix from HEAD (bnc#420016,
  ITS#5649)
* Mon Aug 18 2008 mrueckert@suse.de
- remove outdated options in the fillup_and_insserv call
* Mon Aug 18 2008 rhafer@suse.de
- fixed LSB-Headers in init-script
* Wed Aug 13 2008 ro@suse.de
- try to fix build for buildservice
  (BUILD_INCARNATION can be empty)
* Mon Aug 11 2008 rhafer@suse.de
- /usr/lib/sasl2/slapd.conf was moved to /etc/sasl2/slapd.conf
  (bnc#412652)
- adjust ownerships of database directories even when using
  back-config
* Thu Jul 31 2008 rhafer@suse.de
- Enable back-config delete support
* Tue Jul 29 2008 rhafer@suse.de
- Update to Version 2.4.11. Most important changes:
  * Fixed liblber ber_get_next length decoding (ITS#5580)
  * Added libldap assertion control (ITS#5560)
  * Fixed liblutil missing return code (ITS#5615)
  * Fixed slapd cert serial number parsing (ITS#5588)
  * Fixed slapd check for structural_class failures (ITS#5540)
  * Fixed slapd config backend renumbering (ITS#5571)
  * Fixed slapd configContext OID (ITS#5383)
  * Fixed slapd crash with no listeners (ITS#5563)
  * Fixed slapd sets memory leak (ITS#5557)
  * Fixed slapd sortvals binary search (ITS#5578)
  * Fixed slapd syncrepl updates with multiple masters (ITS#5597)
  * Fixed slapd syncrepl superior objectClass delete/add (ITS#5600)
  * Fixed slapd syncrepl/slapo-syncprov contextCSN updates as internal ops (ITS#5596)
  * Fixed slapo-memberof replace handling (ITS#5584)
  * Added slapo-nssov contrib module
  * Fixed slapo-pcache handling of negative search caches (ITS#5546)
  * Fixed slapo-ppolicy DNs with whitespaces (ITS#5552)
  * Fixed slapo-ppolicy modify with internal ops (ITS#5569)
  * Fixed slapo-syncprov ACL evaluation (ITS#5548)
  * Fixed slapo-syncprov crash with delcsn (ITS#5589)
  * Fixed slapo-syncprov full reload (ITS#5564)
  * Fixed slapo-syncprov missing olcSpReloadHint attr(ITS#5591)
  * Fixed slapo-unique filter normalization (ITS#5581)
* Mon Jun 30 2008 rhafer@suse.de
- Only apply -fPIE patch to recent Distributions
- removed -fPIE from the slapcat-2.3 build
- Adjust BuildRequires for older Distributions
* Fri Jun 27 2008 coolo@suse.de
- make sure the subpacks are only in one spec file declared
* Tue Jun 24 2008 rhafer@suse.de
- branched off libldap-2_4-2 package to support the shared library
  packaging policy
* Wed Jun 11 2008 rhafer@suse.de
- Update to Version 2.4.10. Most important changes:
  * Fixed libldap ld_defconn cleanup if it was freed (ITS#5518,
    ITS#5525)
  * Fixed libldap msgid handling (ITS#5318)
  * Fixed libldap t61 infinite loop (ITS#5542)
  * Fixed libldap_r missing stubs (ITS#5519)
  * Fixed slapd initialization of sr_msgid, rs->sr_tag (ITS#5461)
  * Fixed slapd missing termination of integerFilter keys
    (ITS#5503)
  * Fixed slapd multiple attrs in URI (ITS#5516)
  * Fixed slapd sasl_ssf retrieval (ITS#5403)
  * Fixed slapd socket assert (ITS#5489)
  * Fixed slapd syncrepl cookie (ITS#5536)
  * Fixed slapd-bdb/hdb MAXPATHLEN (ITS#5531)
  * Fixed slapd-bdb indexing in single ADD/MOD (ITS#5521)
  * Fixed slapd-ldap entry_get() op-dependent behavior (ITS#5513)
  * Fixed slapd-meta quarantine crasher (ITS#5522)
  * Fixed slapo-refint to allow setting modifiers name (ITS#5505)
  * Fixed slapo-syncprov contextCSN passing on syncprov consumers
    (ITS#5488)
  * Fixed slapo-syncprov csn update with delta-syncrepl (ITS#5493)
  * Fixed slapo-syncprov op2.o_extra reset (ITS#5501, #5506)
  * Fixed slapo-syncprov searching wrong backend (ITS#5487)
  * Fixed slapo-syncprov sending ops without queued CSNs (ITS#5465)
  * Fixed slapo-syncprov max csn search on startup (ITS#5537)
  * Fixed slapo-unique config structs (ITS#5526)
  * Fixed slapo-unique filter terminator (ITS#5511)
* Fri May 16 2008 rhafer@suse.de
- Support update from 2.3 releases (bnc#390247)
* Thu May  8 2008 rhafer@suse.de
- Update to Version 2.4.9. Most important changes:
  * Fixed libldap to use unsigned port (ITS#5436)
  * Fixed libldap error message for missing close paren (ITS#5458)
  * Fixed libldap_r tpool pause checks (ITS#5364, #5407)
  * Fixed slapcat error checking (ITS#5387)
  * Fixed slapd abstract objectClass inheritance check (ITS#5474)
  * Fixed slapd add operations requiring naming attrs (ITS#5412)
  * Fixed slapd connection handling (ITS#5469)
  * Fixed slapd frontendDB backend selection (ITS#5419)
  * Fixed slapd pagedresults stale state (ITS#5409)
  * Fixed slapd pointer dereference (ITS#5388)
  * Fixed slapd null argument dereference (ITS#5435)
  * Fixed slapd REP_ENTRY flags (ITS#5340)
  * Fixed slapd value list termination (ITS#5450)
  * Fixed slapd-bdb ID_NOCACHE handling (ITS#5439)
  * Fixed slapd-bdb entryinfo state if db_lock fails (ITS#5455)
  * Fixed slapd-bdb referral rewrite (ITS#5339)
  * Fixed slapd-config overlay stacking (ITS#5346)
  * Fixed slapd-config attribute publishing (ITS#5383)
  * Fixed slapd-ldap connection handler (ITS#5404)
  * Fixed slapd-ldif file name handling & multi-suffix/dir catch
    (ITS#5408)
  * Fixed slapd-meta connections on error (ITS#5440)
  * Fixed slapd-meta crash on search (ITS#5481)
  * Various syncrepl fixes (ITS#5407, ITS#5413, ITS#5426, ITS#5430,
    ITS#5432, ITS#5454, ITS#5397, ITS#5470)
  * Various slapo-syncprov fixes (ITS#5401, ITS#5405, ITS#5418,
    ITS#5486, ITS#5433, ITS#5434, ITS#5437, ITS#5444, ITS#5445,
    ITS#5484, ITS#5451)
* Fri Apr 25 2008 rhafer@suse.de
- Adjust ownership of DB_CONFIG to ldap:ldap (bnc#376204)
* Thu Apr 10 2008 matz@suse.de
- Compile with glibc 2.8.
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Thu Apr  3 2008 rhafer@suse.de
- removed apparmor profile
* Mon Mar  3 2008 rhafer@suse.de
- revert last change and make libldap_r available again as some
  packages seem to directly rely on libldap_r. Assume they know
  of the libldap_r's limitations.
* Wed Feb 27 2008 rhafer@suse.de
- Moved libldap_r from -client subpackage to the main server
  package as it is only meant to be used by slapd.
- Removed static libldap_r.a library and libldap_r.so link from
  - devel subpackage. External programs should only use the "normal"
  libldap library.
* Wed Feb 20 2008 rhafer@suse.de
- Update to Version 2.4.8. Most important changes:
  * Fixed libldap extended decoding (ITS#5304)
  * Fixed libldap filter abort (ITS#5300)
  * Fixed libldap ldap_parse_sasl_bind_result (ITS#5263)
  * Fixed libldap result codes for open (ITS#5338)
  * Fixed libldap search timeout crash (ITS#5291)
  * Fixed libldap paged results crash (ITS#5315)
  * Fixed slapd support for 2.1 CSN (ITS#5348)
  * Fixed slapd include handling (ITS#5276)
  * Fixed slapd modrdn check for valid new DN (ITS#5344)
  * Fixed slapd multi-step SASL binds (ITS#5298)
  * Fixed slapd overlay ordering when moving to slapd.d (ITS#5284)
  * Fixed slapd NULL printf (ITS#5264)
  * Fixed slapd NULL set values (ITS#5286)
  * Fixed slapd timestamp race condition (ITS#5370)
  * Fixed slapd cn=config crash on delete (ITS#5343)
  * Fixed slapd cn=config global acls (ITS#5352)
  * Fixed slapd truncated cookie (ITS#5362)
  * Fixed slapd str2entry with no attrs (ITS#5308)
  * Fixed slapd TLSVerifyClient default (ITS#5360)
  * Fixed slapd delta-syncrepl refresh mode (ITS#5376)
  * Fixed slapd ACL sets URI attrs (ITS#5384)
  * Fixed slapd invalid entryUUID filter (ITS#5386)
  * Fixed slapd-bdb idlcache on adds (ITS#5086)
  * Fixed slapd-bdb crash with modrdn (ITS#5358)
  * Fixed slapd-bdb modrdn to same dn (ITS#5319)
  * Fixed slapd-bdb MMR (ITS#5332)
  * Fixed slapd-meta setting of sm_nvalues (ITS#5375)
  * Fixed slapd-monitor crash (ITS#5311)
  * Fixed slapo-ppolicy only password check with policy (ITS#5285)
  * Fixed slapo-ppolicy del/replace password without new one (ITS#5373)
  * Fixed slapo-syncprov hang on checkpoint (ITS#5261)
* Thu Jan 10 2008 rhafer@suse.de
- Removed bogus debugging output from slapd_getaddrinfo_dupl.dif
* Wed Jan  9 2008 rhafer@suse.de
- Fixed allocation for paged results cookie (Bug #352255, ITS#5315)
* Fri Dec 14 2007 rhafer@suse.de
- Update to Version 2.4.7. Most important changes:
  * Added slapd ordered indexing of integer attributes (ITS#5239)
  * Fixed slapd paged results control handling (ITS#5191)
  * Fixed slapd sasl-host parsing (ITS#5209)
  * Fixed slapd filter normalization (ITS#5212)
  * Fixed slapd multiple suffix checking (ITS#5186)
  * Fixed slapd paged results handling when using rootdn (ITS#5230)
  * Fixed slapd syncrepl presentlist handling (ITS#5231)
  * Fixed slapd core schema 'c' definition for RFC4519 (ITS#5236)
  * Fixed slapd 3-way Multi-Master Replication (ITS#5238)
  * Fixed slapd hash collisions in index slots (ITS#5183)
  * Fixed slapd replication of dSAOperation attributes (ITS#5268)
  * Fixed slapadd contextCSN updating (ITS#5225)
  * Fixed slapd-bdb/hdb to report and fail on internal errors (ITS#5232)
  * Fixed slapd-bdb/hdb dn2entry lock bug (ITS#5257)
  * Fixed slapd-bdb/hdb dn2id lock bug (ITS#5262)
  * Fixed slapd-hdb caching on rename ops (ITS#5221)
  * Fixed slapo-accesslog abandoned op cleanup (ITS#5161)
  * Fixed slapo-dds deleting from nonexistent db (ITS#5267)
  * Fixed slapo-memberOf deleted values saving (ITS#5258)
  * Fixed slapo-pcache op->o_abandon handling (ITS#5187)
  * Fixed slapo-ppolicy single password check on modify (ITS#5146)
  * Fixed slapo-ppolicy internal search (ITS#5235)
  * Fixed slapo-syncprov refresh and persist cookie sending (ITS#5210)
  * Fixed slapo-syncprov ignore invalid cookies (ITS#5211)
  * Fixed slapo-translucent interaction with slapo-rwm (ITS#4889)
* Thu Nov 29 2007 rhafer@suse.de
- check for duplicates in getaddrinfo results and ignore them.
  (Bug #288879)
* Tue Nov 27 2007 rhafer@suse.de
- The init-script removed directory access on /etc/openldap/slapd.d
  (Bug #344091)
* Mon Nov 26 2007 rhafer@suse.de
- Update to Version 2.4.6. Initial 2.4 release for "general use".
  New features:
  * Usability/Manageability:
  - More complete Documentation (manual pages and Admin Guide)
  - dynamic configuration and monitoring improvments
  * More functionality
  - New overlays (dds, memberof, constraint)
  - Multimaster syncrepl replication
  * Performance improvments:
  - Further optimized frontend
  - Reduced locking contention in backend
- back-config support through new sysconfig option
  "OPENLDAP_CONFIG_BACKEND"
- Install admin guide from the main tarball, to get rid of the
  admin-guide tarball
- New sysconfig options:
  * OPENLDAP_START_LDAP to allow to disable the ldap:// listener
  * OPENLDAP_LDAPI_INTERFACES to specify the paths for the ldapi:///
    listeners
* Mon Oct 29 2007 rhafer@suse.de
- Update to Version 2.3.39. Most important changes:
  * Fixed slapd database/overlay config conflict (ITS#4848)
  * Fixed slapd password_hash config order (ITS#5082)
  * Fixed slapd slap_mods_check bug (ITS#5119)
  * Fixed slapd ACL sets memory handling (ITS#4860,ITS#4873)
  * Fixed slapd ordered values add normalization issue (ITS#5136)
  * Fixed slapd-bdb DB_CONFIG conversion bug (ITS#5118)
  * Fixed slapd-ldap search control parsing (ITS#5138)
  * Fixed slapd-ldap SASL idassert w/o authcId
  * Fixed slapd-ldif directory separators in DN (ITS#5172)
  * Fixed slapd-meta conn caching on bind failure (ITS#5154)
  * Fixed slapd-meta bind timeout assertion (ITS#5185)
  * Fixed slapd-sql concurrency issue (ITS#5095)
  * Fixed slapo-chain double-free (ITS#5137)
  * Fixed slapo-pcache and -rwm interaction fix (ITS#4991)
  * Fixed slapo-pcache non-null terminated array crasher (ITS#5163)
  * Fixed slapo-rwm modlist handling (ITS#5124)
  * Fixed slapo-rwm UUID in filter (ITS#5168)
  * Fixed sasl SASL_SSF_EXTERNAL type (ITS#3864)
  * Fixed liblber Windows x64 portability (ITS#5105)
  * Fixed libldap ppolicy control creation (ITS#5103)
- Silenced some rpmlint warnings
* Wed Aug 22 2007 rhafer@suse.de
- Call "ldconfig" from %%post and %%postun in openldap2-client
  (Bug #298297)
* Tue Jul 24 2007 rhafer@suse.de
- Update to Version 2.3.37. Most important changes:
  * Fixed slapd-glue/syncprov interaction (ITS#4623)
  * Fixed slapd-ldap search reference crash (ITS#5025)
  * Fixed slapd-ldbm crash on Compare op (ITS#5044)
  * Fixed slapo-rwm searchFilter double free (ITS#5043)
- Most important changes in 2.3.36:
  * Fixed slapd mutex bug after failed startup (ITS#4957)
  * Fixed slapd sasl failed Bind bug (ITS#4954)
  * Fixed slapd sasl ssf logging (ITS#5001)
  * Fixed slapd tool op init (ITS#4911)
  * Fixed slapd-bdb no-op crasher (ITS#4925)
  * Fixed slapd-relay crash when no database can be selected (ITS#4958)
  * Fixed slapo-chain RFC3062 passwd exop handling (ITS#4964)
  * Fixed slapo-dynlist multiple group/url[/member] config (ITS#4989)
  * Fixed slapo-pcache handling of abandoned Operations (#5015)
  * Fixed slapo-pcache and -rwm interaction (ITS#4991)
  * Fixed slapo-ppolicy pwdReset/pwdMinAge (ITS#4970)
  * Fixed slapo-ppolicy control cleanup from ITS#4665
  * Fixed slapo-syncprov cookie parsing error (ITS#4977)
  * Fixed slapo-valsort crash on delete op (ITS#4966)
  * Fixed libldap referral chasing loop (ITS#4955)
  * Fixed libldap response code handling on rebind (ITS#4924)
  * Fixed libldap SASL_MAX_BUFF_SIZE (ITS#4935)
* Wed Jun 13 2007 dmueller@suse.de
- remove binutils prereq
* Mon May 21 2007 dmueller@suse.de
- reduce duplicated buildrequires against db42 and db45
* Tue May 15 2007 rhafer@suse.de
- imported apparmor profile from apparmor (this profile is not
  enabled by default)
* Fri May  4 2007 rhafer@suse.de
- Update to Version 2.3.35. Most important changes:
  * Fixed ldapmodify to use correct memory free functions (ITS#4901)
  * Fixed slapd acl set minor typo (ITS#4874)
  * Fixed slapd entry consistency check in str2entry2 (ITS#4852)
  * Fixed slapd ldapi:// credential issue (ITS#4893)
  * Fixed slapd str2anlist handling of undefined attrs/OCs (ITS#4854)
  * Fixed slapd syncrepl delta-sync modlist free (ITS#4904)
  * Added slapd syncrepl retry logging (ITS#4915)
  * Fixed slapd zero-length IA5string handling (ITS#4823)
  * Fixed slapd-bdb/hdb startup with missing shm env (ITS#4851)
  * Fixed slapd-ldap/meta consistency in referral proxying (ITS#4861)
  * Fixed slapd-ldap bind cleanup in case of unauthorized idassert
  * Fixed slapd-meta search cleanup
  * Fixed slapd-meta/slapo-rwm filter mapping
  * Fixed slapd-sql subtree shortcut (ITS#4856)
  * Fixed slapo-dynlist crasher (ITS#4891)
  * Fixed slapo-refint config message (ITS#4853)
  * Fixed libldap time_t signedness (ITS#4872)
  * Fixed libldap_r tpool reset (ITS#4855,#4899)
* Wed May  2 2007 dmueller@suse.de
- Fix comparison with string literal
* Wed Apr 18 2007 schwab@suse.de
- Fix generation of debuginfo packages.
* Tue Mar 20 2007 rguenther@suse.de
- removed krb5-devel BuildRequires (support via cyrus-sasl)
* Thu Mar 15 2007 rhafer@suse.de
- added Service definitions for SuSEfirewall2 (Bug #251654)
* Thu Feb 22 2007 rhafer@suse.de
- Updated to Version 2.3.34. Most important changes:
  * Fixed libldap missing get_option(TLS CipherSuite) (ITS#4815)
  * Fixed ldapmodify printing error from ldap_result() (ITS#4812)
  * Fixed slapadd LDIF parsing (ITS#4817)
  * Fixed slapd libltdl link ordering (ITS#4830)
  * Fixed slapd syncrepl memory leaks (ITS#4805)
  * Fixed slapd dynacl/ACI compatibility with 2.1
  * Fixed slapd-bdb/hdb be_entry_get with aliases/referrals
    (ITS#4810)
  * Fixed slapd-ldap more response handling bugs (ITS#4782)
  * Fixed slapd-ldap C-API code tests (ITS#4808)
  * Fixed slapd-monitor NULL printf (ITS#4811)
  * Fixed slapo-chain spurious additional info in response
    (ITS#4828)
  * Fixed slapo-syncprov presence list (ITS#4813)
  * Fixed slapo-syncprov contextCSN checkpoint again (ITS#4720)
  * Added slapo-ppolicy cn=config support (ITS#4836)
  * Added slapo-auditlog cn=config support
* Fri Jan 26 2007 rhafer@suse.de
- Updated to Version 2.3.33. Most important changes:
  * Fixed slapd-ldap chase-referrals switch (ITS#4557)
  * Fixed slapd-ldap bind behavior when idassert is always used
    (ITS#4781)
  * Fixed slapd-ldap response handling bugs (ITS#4782)
  * Fixed slapd-ldap idassert mode=self anonymous ops (ITS#4798)
  * Fixed slapd-ldap/meta privileged connections handling
    (ITS#4791)
  * Fixed slapd-meta retrying (ITS#4594, 4762)
  * Fixed slapo-chain referral DN use (ITS#4776)
  * Fixed slapo-dynlist dangling pointer after entry free
    (ITS#4801)
  * Fixed libldap ldap_pvt_put_filter syntax checks (ITS#4648)
* Fri Jan 12 2007 rhafer@suse.de
- Updated to Version 2.3.32. Most important changes:
  * Fixed libldap unchased referral leak (ITS#4545)
  * Fixed libldap tls callback (ITS#4723)
  * Fixed slapd memleak on failed bind (ITS#4771)
  * Fixed slapd connections_shutdown assert
  * Fixed slapd add redundant duplicate value check (ITS#4600)
  * Fixed slapd ACL set memleak (ITS#4780)
  * Fixed slapd syncrepl shutdown hang (ITS#4790)
* Fri Nov 17 2006 rhafer@suse.de
- Fix for a flaw in libldap's strval2strlen() function when processing the
  authcid string of certain Bind Requests, which could allow attackers to
  cause an affected application to crash (especially the OpenLDAP Server),
  creating a denial of service condition (Bug#221154,ITS#4740)
* Tue Nov 14 2006 rhafer@suse.de
- Additional back-perl fixes from CVS. The first revision of the
  patch did not fix the problem completely  (Bug#207618, ITS#4751)
* Fri Oct 27 2006 rhafer@suse.de
- cyrus-sasl configuration moved from %%{_libdir}/sasl2 to
  /etc/sasl2/ (Bug: #206414)
* Wed Oct  4 2006 rhafer@suse.de
- Add $network to Should-Start/Should-Stop in init scripts
  (Bug: #206823)
- Imported latest back-perl changes from CVS, to fix back-perl
  initialization (Bug: #207618)
* Tue Aug 22 2006 rhafer@suse.de
- Updated to Version 2.3.27
  * Fixed libldap dnssrv bug with "not present" positive statement
    (ITS#4610)
  * Fixed libldap dangling pointer issue (ITS#4405)
  * Fixed slapd incorrect rebuilding of replica URI (ITS#4633)
  * Fixed slapd DN X.509 normalization crash (ITS#4644)
  * Fixed slapd-monitor operations order via callbacks (ITS#4631)
  * Fixed slapo-accesslog purge task during shutdown
  * Fixed slapo-ppolicy handling of default policy (ITS#4634)
  * Fixed slapo-ppolicy logging verbosity when using default policy
  * Fixed slapo-syncprov incomplete sync on restart issues (ITS#4622)
* Wed Aug  2 2006 rhafer@suse.de
- Updated to Version 2.3.25
  * Add libldap_r TLS concurrency workaround (ITS#4583)
  * Fixed slapd acl selfwrite bug (ITS#4587)
  * Fixed various syncrepl and slapo-syncprov bugs (ITS#4582, 4622,
    4534,4613, 4589)
  * Fixed slapd-bdb/hdb lock bug with virtual root (ITS#4572)
  * Fixed slapd-bdb/hdb modrdn new entry disappearing bug (ITS#4616)
  * Fixed slapd-bdb/hdb cache job issue
  * Fixed slapo-ppolicy password hashing bug (ITS#4575)
  * Fixed slapo-ppolicy password modify pwdMustChange reset bug (ITS#4576)
  * Fixed slapo-ppolicy control can be critical (ITS#4596)
- Enabled CLDAP (LDAP over UDP) support
* Mon Jun 26 2006 rhafer@suse.de
- Updated to Version 2.3.24
  * Fixed slapd syncrepl timestamp bug (delta-sync/cascade)
    (ITS#4567)
  * Fixed slapd-bdb/hdb non-root users adding suffix/root entries
    (ITS#4552)
  * Re-fixed slapd-ldap improper free bug in exop (ITS#4550)
  * Fixed slapd-ldif assert bug (ITS#4568)
  * Fixed slapo-syncprov crash under glued database (ITS#4562)
- cleaned up SLES10 update specific stuff
- added "chain-return-error" feature from HEAD to chain overlay
  (ITS#4570)
* Thu Jun 22 2006 schwab@suse.de
- Don't use automake macros without using automake.
* Wed May 24 2006 rhafer@suse.de
- Updated to Version 2.3.23
  * obsoletes the patches: libldap_ads-sasl-gssapi.dif,
    slapd-epollerr.dif
  * Fixed slapd-ldap improper free bug (ITS#4550)
  * Fixed libldap referral input destroy issue (ITS#4533)
  * Fixed libldap ldap_sort_entries tail bug (ITS#4536)
  * Fixed slapd runqueue use of freed memory (ITS#4517)
  * Fixed slapd thread pool init issue (ITS#4513)
  * Fixed slapd-bdb/hdb pre/post-read freeing (ITS#4532)
  * Fixed slapd-bdb/hdb pre/post-read unavailable issue (ITS#4538)
  * Fixed slapd-bdb/hdb referral issue (ITS#4548)
  * Fixed slapo-ppolicy BER tags issue (ITS#4528)
  * Fixed slapo-ppolicy rebind bug (ITS#4516)
  * For more details see the CHANGES file
- Install CHANGES file to /usr/share/doc/packages/openldap2
* Wed May 10 2006 rhafer@suse.de
- Really apply the patch for Bug#160566
- slapd could crash while processing queries with pre-/postread
  controls (Bug#173877, ITS#4532)
* Fri Mar 24 2006 rhafer@suse.de
- Backported fix from CVS for occasional crashes in referral
  chasing code (as used in e.g. back-meta/back-ldap).
  (Bug: #160566, ITS: #4448)
* Mon Mar 13 2006 rhafer@suse.de
- openldap2 must obsolete -back-monitor and -back-ldap to have them
  removed during update (Bug: #157576)
* Fri Feb 17 2006 rhafer@suse.de
- Add "external" to the list of supported SASL mechanisms
  (Bug: #151771)
* Thu Feb 16 2006 rhafer@suse.de
- Error out when conversion from old configfile to config database
  fails (Bug: #135484,#135490 ITS: #4407)
* Mon Feb 13 2006 rhafer@suse.de
- Don't ignore non-read/write epoll events (Bug: #149993,
  ITS: #4395)
- Added update message to /usr/share/update-messages/en/ and enable
  it, when update did not succeed.
* Thu Feb  9 2006 rhafer@suse.de
- OPENLDAP_CHOWN_DIRS honors databases defined in include files
  (Bug: #135473)
- Fixed version numbers in README.update
- Fixed GSSAPI binds against Active Directory (Bug: #149390)
* Fri Feb  3 2006 rhafer@suse.de
- Cleaned up update procedure
- man-pages updates and fixes (Fate: #6365)
* Fri Jan 27 2006 rhafer@suse.de
- Updated to 2.3.19 (Bug #144371)
* Fri Jan 27 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Jan 25 2006 rhafer@suse.de
- Updated Admin Guide to latest version
- build slapcat from openldap-2.2.24 and install it to
  /usr/sbin/openldap-2.2-slapcat to be able to migrate from
  OpenLDAP 2.2.
- removed slapd-backbdb-dbupgrade which is no longer needed
- attempt to dump/reload bdb databases in %%{post}
- Update notes in README.update
* Fri Jan 13 2006 rhafer@suse.de
- New sysconfig variable OPENLDAP_KRB5_KEYTAB
- Cleanup in default configuration and init scripts
* Wed Jan 11 2006 rhafer@suse.de
- Updated to 2.3.17
- Remove OPENLDAP_RUN_DB_RECOVER from sysconfig file in %%post
  slapd does now automatically recover the database if needed
- Removed unneeded README.SuSE
- Small adjustments to the default DB_CONFIG file
* Mon Jan  9 2006 rhafer@suse.de
- Updated to 2.3.16
* Mon Dec 19 2005 rhafer@suse.de
- Fixed filelist (slapd-hdb man-page was missing)
* Fri Dec  9 2005 rhafer@suse.de
- Fixed build on x86_64
* Wed Dec  7 2005 rhafer@suse.de
- Merged -back-ldap and -back-monitor subpackages into the main
  package and don't build them as dynamic modules anymore.
- updated to OpenLDAP 2.3.13
* Mon Nov 28 2005 rhafer@suse.de
- updated to OpenLDAP 2.3.12
* Wed Oct 26 2005 rhafer@suse.de
- updated to OpenLDAP 2.3.11
- removed the "LDAP_DEPRECATED" workaround
* Mon Sep 26 2005 rhafer@suse.de
- Add "LDAP_DEPRECATED" to ldap.h for now
* Fri Sep 23 2005 rhafer@suse.de
- updated to OpenLDAP 2.3.7
* Tue Aug 16 2005 rhafer@suse.de
- allow start_tls while chasing referrals (Bug #94355, ITS #3791)
* Mon Jul  4 2005 rhafer@suse.de
- devel-subpackage requires openldap2-client of the same version
  (Bugzilla: #93579)
* Thu Jun 30 2005 uli@suse.de
- build with -fPIE (not -fpie) to avoid GOT overflow on s390*
* Wed Jun 22 2005 rhafer@suse.de
- build the server packages with -fpie/-pie
* Wed Jun 15 2005 rhafer@suse.de
- updated to 2.2.27
* Wed May 25 2005 rhafer@suse.de
- libldap-gethostbyname_r.dif: Use gethostbyname_r instead of
  gethostbyname in libldap. Should fix host lookups through
  nss_ldap (Bugzilla: #76173)
* Fri May 13 2005 rhafer@suse.de
- Updated to 2.2.26
- made /%%{_libdir}]/sasl2/slapd.conf %%config(noreplace)
* Thu Apr 28 2005 rhafer@suse.de
- Added /%%{_libdir}]/sasl2/slapd.conf to avoid warnings about
  unconfigured OTP mechanism (Bugzilla: #80588)
* Tue Apr 12 2005 rhafer@suse.de
- added minimal timeout to startproc in init-script to let it
  report the "failed" status correctly in case of misconfiguration
  (Bugzilla: #76393)
* Mon Apr  4 2005 rhafer@suse.de
- crl-check.dif: Implements CRL checking on client and server side
- use different base ports for differnt values of BUILD_INCARNATION
  (/.buildenv) to allow parallel runs of the test-suite on a single
  machine
* Mon Apr  4 2005 uli@suse.de
- force yielding-select test to yes (test occasionally hangs QEMU)
* Fri Apr  1 2005 uli@suse.de
- disable test suite on ARM (hangs QEMU)
* Tue Mar 29 2005 rhafer@suse.de
- updated to 2.2.24
- enabled back-hdb
* Wed Mar  2 2005 rhafer@suse.de
- syncrepl.dif: merged latest syncrepl fixes (Bugzilla: #65928)
- libldap-reinit-fdset.dif: Re-init fd_sets when select is
  interupted (Bugzilla #50076, ITS: #3524)
* Thu Feb 17 2005 rhafer@suse.de
- checkproc_before_recover.dif: Check if slapd is stopped before
  running db_recover from the init script. (Bugzilla: #50962)
* Tue Feb  1 2005 rhafer@suse.de
- Cleanup back-bdb databases in %%post, db-4.3 changed the
  transaction log format again.
- cosmetic fixes in init script
* Tue Jan 25 2005 rhafer@suse.de
- updated to 2.2.23
- cleaned up #neededforbuild
- package should also build on older SuSE Linux releases now
- increased killproc timeout in init-script (Bugzilla: #47227)
* Thu Jan 13 2005 rhafer@suse.de
- updated to 2.2.20
- Removed unneeded dependencies
* Fri Dec 10 2004 kukuk@suse.de
- don't install *.la files
* Wed Nov 10 2004 rhafer@suse.de
- updated to 2.2.18
- use kerberos-devel-packages in neededforbuild
* Fri Sep 24 2004 ro@suse.de
- re-arranged specfile to sequence (header (package/descr)* rest)
  so the checking parser is not confused ...
* Fri Sep 24 2004 rhafer@suse.de
- Added pre_checkin.sh to generate a separate openldap2-client
  spec-file from which the openldap2-client and openldap2-devel
  subpackages are built. Should reduce build time for libldap as
  the test-suite is only executed in openldap2.spec.
* Fri Sep 10 2004 rhafer@suse.de
- libldap-result.dif: ldapsearch was hanging in select() when
  retrieving results from eDirectory through a StartTLS protected
  connection (Bugzilla #44942)
* Mon Aug  9 2004 dobey@suse.de
- added ntlm support
* Tue Aug  3 2004 rhafer@suse.de
- updated to 2.2.16
- Updated ACLs in slapd_conf.dif to disable default read access
  to the "userPKCS12" Attribute
- rc-check-conn.diff: When starting slapd wait until is accepts
  connections, or 10 seconds at maximum (Bugzilla #41354)
- Backported -o slp={on|off} feature from OpenLDAP Head and added
  new sysconfig variable (OPENLDAP_REGISTER_SLP) to be able
  to switch SLP registration on and off. (Bugzilla #39865)
- removed unneeded README.update
* Fri Apr 30 2004 rhafer@suse.de
- updated to 2.2.11
- remove SLES8 update specific stuff
- Bugzilla #39652: Updated slapd_conf.dif to contain basic access
  control
- Bugzilla #39468: Added missing items to yast.schema
- fixed strict-aliasing compiler warnings (strict-aliasing.dif)
* Thu Apr 29 2004 coolo@suse.de
- build with several jobs if available
* Mon Apr 19 2004 rhafer@suse.de
- ldapi_url.dif: Fixed paths for LDAPI-socket, pid-file and
  args-file (Bugzilla #38790)
- ldbm_modrdn.dif: Fixed back-ldbm modrdn indexing bug (ITS #3059,
  Bugzilla #38915)
- modify_check_duplicates.dif: check for duplicate attribute
  values in modify requests (ITS #3066/#3097, Bugzilla #38607)
- updated and renamed yast2userconfig.schema to yast.schema as it
  contains more that only user configuration now
- syncrepl.dif: addtional fixes for syncrepl (ITS #3055, #3056)
- test_syncrepl_timeout: increased sleep timeout in syncrepl
  testsuite
* Thu Apr  1 2004 rhafer@suse.de
- added "TLS_REQCERT allow" to /etc/openldap/ldap.conf, to make
  START_TLS work without access to the CA Certificate.
  (Bugzilla: #37393)
* Fri Mar 26 2004 rhafer@suse.de
- fixed filelist
- check-build.sh (build on kernel >= 2.6.4 hosts only)
- yast2user.schema / slapd.conf fixed (#37076)
- don't check for TLS-options is init-script anymore (#33560)
- fixed various typos in README.update
* Wed Mar 17 2004 rhafer@suse.de
- fixed build of openldap-2.1-slapcat (using correct db41 include
  files, build backends as on sles8)
- attempt to update bdb database and reindex ldbm database in %%{post}
- Update notes in README.update
- better default configuration (including default DB_CONFIG file)
- misc updates for the YaST schema
- fixed crasher in syncrepl-code (syncrepl.dif)
* Tue Mar 16 2004 schwab@suse.de
- Fix type mismatch.
* Tue Mar  2 2004 rhafer@suse.de
- updated to 2.2.6
- build a openldap-2.1-slapcat from 2.1.25 sources  to be able to
  migrate from SLES8 and SL 9.0
* Thu Feb 19 2004 ro@suse.de
- added check-build.sh (build on 2.6 hosts only)
* Thu Feb  5 2004 rhafer@suse.de
- updated to 2.2.5
- adjusted rfc2307bis.schema to support UTF-8 values in most
  attributes
- enabled proxycache-overlay (wiht fix to work with back-ldbm)
* Tue Jan 13 2004 rhafer@suse.de
- updated to 2.2.4
- updated Admin Guide to most recent version
* Sat Jan 10 2004 adrian@suse.de
- add %%defattr
- fix build as user
* Mon Dec  8 2003 rhafer@suse.de
- updated to 2.1.25
- small fixes for the YaST user schema
* Tue Nov 11 2003 rhafer@suse.de
- enabled SLP-support
* Fri Oct 17 2003 kukuk@suse.de
- Remove unused des from neededforbuild
* Tue Sep  2 2003 mt@suse.de
- Bugzilla #29859: fixed typo in sysconfig metadata,
  usage of OPENLDAP_LDAPS_INTERFACES in init script
- added /usr/lib/sasl2/slapd.conf permissions handling
- added sysconfig variable OPENLDAP_SLAPD_PARAMS=""
  to support additional slapd start parameters
- added sysconfig variable OPENLDAP_START_LDAPI=NO/yes
  for ldapi:/// (LDAP over IPC) URLs
* Thu Aug 14 2003 rhafer@suse.de
- added activation metadata to sysconfig template (Bugzilla #28911)
- removed lint from specfile
* Thu Aug  7 2003 rhafer@suse.de
- added %%stop_on_removal and %%restart_on_update calls
- bdb_addcnt.dif fixes a possible endless loop in id2entry()
- addonschema.tar.gz: some extra Schema files (YaST, RFC2307bis)
* Wed Jul 16 2003 rhafer@suse.de
- removed fillup_only and call fillup_and_insserv correctly
- new Options in sysconfig.openldap: OPENLDAP_LDAP_INTERFACES,
  OPENLDAP_LDAPS_INTERFACES and OPENLDAP_RUN_DB_RECOVER
* Tue Jul  1 2003 rhafer@suse.de
- updated to 2.1.22
- updated Admin Guide to most recent version
- build librewrite with -fPIC
* Mon Jun 16 2003 rhafer@suse.de
- updated to 2.1.21
* Wed Jun 11 2003 ro@suse.de
- fixed requires lines
* Mon May 26 2003 rhafer@suse.de
- don't link back-ldap against librewrite.a, it's already linked
  into slapd (package should build on non-i386 Archs again)
* Fri May 23 2003 rhafer@suse.de
- fixed dynamic build of back-ldap
- new subpackage back-ldap
* Tue May 20 2003 rhafer@suse.de
- updated to version 2.1.20
- enabled dynamic backend modules
- new subpackages back-perl, back-meta and back-monitor
- remove unpacked files from BuildRoot
* Fri May  9 2003 rhafer@suse.de
- updated to version 2.1.19
* Tue Apr 15 2003 ro@suse.de
- fixed requires for devel-package ...
* Tue Apr 15 2003 ro@suse.de
- fixed neededforbuild
* Thu Feb 13 2003 kukuk@suse.de
- Enable IPv6 again
* Tue Feb 11 2003 rhafer@suse.de
- added /etc/openldap to filelist
* Mon Feb  3 2003 rhafer@suse.de
- switch default backend to ldbm
* Sun Feb  2 2003 ro@suse.de
- fixed requires for devel package (cyrus-sasl2-devel)
* Fri Jan 31 2003 rhafer@suse.de
- liblber.dif: Fixes two bugs in liblber by which remote attackers
  could crash the LDAP server (Bugzilla #22469, OpenLDAP ITS #2275
  and #2280)
* Tue Jan 14 2003 choeger@suse.de
- build using sasl2
* Mon Jan 13 2003 rhafer@suse.de
- updated to version 2.1.12
- added metadata to sysconfig template (Bug: #22666)
* Thu Nov 28 2002 rhafer@suse.de
- updated to version 2.1.8
- added additional fix of 64bit archs
- added secpatch.dif to fix setuid issues in libldap
* Fri Sep  6 2002 rhafer@suse.de
- fix for Bugzilla ID #18981, chown to OPENLDAP_USER didn't work
  with multiple database backend directories
* Mon Sep  2 2002 rhafer@suse.de
- removed damoenstart_ipv6.diff and disabled IPv6 support due to
  massive problems with nss_ldap
* Mon Aug 26 2002 rhafer@suse.de
- ldap_user.dif: slapd is now run a the user/group ldap (Bugzilla
  ID#17697)
* Fri Aug 23 2002 rhafer@suse.de
- updated to version 2.1.4, which fixes tons of bugs
- added damoenstart_ipv6.diff (slapd was not starting when
  configured to listen on IPv4 and IPv6 interfaces, as done by the
  start script)
- added README.SuSE with some hints about the bdb-backend
- updated filelist to include only the man pages of the backends,
  that were built
* Thu Aug 15 2002 rhafer@suse.de
- removed termcap and readline from neededforbuild
* Thu Aug  8 2002 rhafer@suse.de
- enabled {CRYPT} passwords
- update filelist (added new manpages)
* Thu Jul 25 2002 rhafer@suse.de
- patches for 64 bit architectures
* Fri Jul 19 2002 rhafer@suse.de
- update to 2.1.3
* Fri Jul  5 2002 kukuk@suse.de
- fix openldap2-devel requires
* Thu Jul  4 2002 rhafer@suse.de
- switched back from cyrus-sasl2 to cyrus-sasl
* Wed Jul  3 2002 rhafer@suse.de
- updated to OpenLDAP 2.1.2
- added the OpenLDAP Administration Guide
- enabled additional backends (ldap, meta, monitor)
* Mon Jun 10 2002 olh@suse.de
- hack build/ltconfig to build shared libs on ppc64
* Wed Jun  5 2002 rhafer@suse.de
- created /etc/sysconfig/openldap and OPENLDAP_START_LDAPS variable
  to enable ldap over ssl support
* Thu Mar  7 2002 rhafer@suse.de
- Fix for Bugzilla ID#14569 (added cyrus-sasl-devel openssl-devel
  to the "Requires" Section of the -devel subpackage)
* Mon Feb 18 2002 rhafer@suse.de
- updated to the latest STABLE release (2.0.23) which fixes some
  nasty bugs see ITS #1562,#1582,#1577,#1578
* Thu Feb  7 2002 rhafer@suse.de
- updated to the latest release (which fixes a index corruption
  bug)
- cleanup in neededforbuild
- small fixes for the init-scripts
* Thu Jan 17 2002 rhafer@suse.de
- updated to the latest stable release (2.0.21)
* Wed Jan 16 2002 egmont@suselinux.hu
- removed periods and colons from startup/shutdown messages
* Tue Jan 15 2002 rhafer@suse.de
- updated to v2.0.20 (which fixes a security hole in ACL
  processing)
* Fri Jan 11 2002 rhafer@suse.de
- converted archive to bzip2
- makes use of %%{_libdir} now
- set CFLAGS to -O0 for archs ia64, s390(x) and alpha otherwise
  the test suite fails on these archs
- changed slapd.conf to store the database under /var/lib/ldap
  (this patch was missing in the last versions by accident)
* Mon Jan  7 2002 rhafer@suse.de
- update to v2.0.19
* Thu Dec  6 2001 rhafer@suse.de
- eliminated START_LDAP, START_SLURPD variables in rc.config
- created separate init script for slurpd
- moved init scripts from dif to separate source tgz
* Fri Oct 26 2001 choeger@suse.de
- update to v2.0.18
* Mon Oct 15 2001 choeger@suse.de
- update to v2.0.17
  added a sleep to the restart section
  moved some manpages to the client package
* Mon Oct  1 2001 choeger@suse.de
- update to v2.0.15
* Wed Sep 12 2001 choeger@suse.de
- backported the full bugfix from openldap-2.0.14
* Tue Sep 11 2001 choeger@suse.de
- Bugfix for slurpd millionth second bug (ITS#1323)
* Mon Sep 10 2001 choeger@suse.de
- moved ldapfilter.conf ldaptemplates.conf ldapsearchprefs.conf
  to openldap2-client package
* Mon Sep  3 2001 choeger@suse.de
- update to version 2.0.12
* Mon Jul  2 2001 choeger@suse.de
- bugfix: init script was not LSB compliant, Bugzilla ID#9072
* Tue Jun 19 2001 ro@suse.de
- fixed for autoconf again
* Fri Jun 15 2001 choeger@suse.de
- update to 2.0.11
- removed autoconf in specfile, because it doesn't work
* Wed May 23 2001 choeger@suse.de
- update to version 2.0.10 (minor fixes)
* Tue May 22 2001 choeger@suse.de
- update to version 2.0.9
* Mon Apr 23 2001 choeger@suse.de
- removed kerberos support
- added aci support
* Fri Apr 20 2001 choeger@suse.de
- added kerberos support
* Thu Apr  5 2001 choeger@suse.de
- moved section 5 and 8 manpages to the server part of package
* Wed Mar 14 2001 kukuk@suse.de
- Move *.so links into -devel package
- -devel requires -client
* Thu Mar  8 2001 choeger@suse.de
- split up into openldap2-client and -devel
* Tue Feb 27 2001 ro@suse.de
- changed neededforbuild <cyrus-sasl> to <cyrus-sasl cyrus-sasl-devel>
* Thu Feb 22 2001 ro@suse.de
- added readline/readline-devel to neededforbuild (split from bash)
* Thu Jan  4 2001 choeger@suse.de
- bugfix: slapd.conf rename /var/lib/openldap-ldbm to
    /var/lib/ldap
    init script: use $remote_fs
* Tue Jan  2 2001 olh@suse.de
- use script name in %%post
* Thu Dec  7 2000 choeger@suse.de
- bugfix from Andreas Jaeger:
  workaround for glibc2.2, detach
* Fri Dec  1 2000 ro@suse.de
- hacked configure for apparently broken pthread
* Fri Dec  1 2000 ro@suse.de
- fixed spec
* Thu Nov 23 2000 choeger@suse.de
- made configs %%config(noreplace) (Bug 4112)
- fixed neededforbuild
* Wed Nov 22 2000 choeger@suse.de
- adopted new init scheme
* Wed Nov 15 2000 choeger@suse.de
- fixed neededforbuild
* Fri Nov 10 2000 choeger@suse.de
- added buildroot
* Tue Nov  7 2000 choeger@suse.de
- long package name
- new version, 2.0.7
* Fri Oct  6 2000 choeger@suse.de
- first package of openldap2 (v2.0.6)
