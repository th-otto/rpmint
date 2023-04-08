%define pkgname ca-certificates

%rpmint_header

Summary:        Utilities for system wide CA certificate installation
Name:           %{crossmint}%{pkgname}
Version:        10b2785
Release:        1
License:        GPL-2.0-or-later
Group:          Productivity/Networking/Security

Packager:       %{packager}
URL:            https://github.com/openSUSE/ca-certificates

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz
Source1: http://anduin.linuxfromscratch.org/BLFS/other/make-ca.sh
Source2: http://anduin.linuxfromscratch.org/BLFS/other/certdata.txt


BuildArch:      noarch
%if "%{buildtype}" != "cross"
%define _arch noarch
%endif

%description
Update-ca-certificates is intended to keep the certificate stores of
SSL libraries like OpenSSL or GnuTLS in sync with the system&apos;s CA
certificate store that is managed by p11-kit.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%build

%rpmint_cflags
TARGET_PREFIX=%{_rpmint_target_prefix}
TARGET_SYSCONFDIR=/etc

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
"

NO_STRIP=true

ssletcdir=${TARGET_SYSCONFDIR#/}/ssl
sslcerts=${ssletcdir}/certs
cabundle=var/lib/ca-certificates/ca-bundle.pem
trustdir_cfg=etc/pki/trust
trustdir_static=usr/share/pki/trust

for CPU in noarch; do
	buildroot="%{buildroot}%{_rpmint_sysroot}"
	make DESTDIR="${buildroot}" install

	# compress manpages
	%rpmint_gzip_docs

	cd "${buildroot}"
	install -d -m 755 ${trustdir_cfg}/{anchors,blacklist}
	install -d -m 755 ${trustdir_static}/{anchors,blacklist}
	install -d -m 755 ${ssletcdir}
	install -d -m 755 ${TARGET_SYSCONFDIR#/}/ca-certificates/update.d
	install -d -m 755 ${TARGET_PREFIX#/}/lib/ca-certificates/update.d
	install -d -m 555 var/lib/ca-certificates/pem
	install -d -m 555 var/lib/ca-certificates/openssl
	install -d -m 755 ${TARGET_PREFIX#/}/lib/systemd/system
	ln -s ../../var/lib/ca-certificates/pem ${sslcerts}
	install -D -m 644 /dev/null ${cabundle}
	ln -s ../../${cabundle} ${ssletcdir}/ca-bundle.pem
	install -D -m 644 /dev/null var/lib/ca-certificates/java-cacerts

	rm -rf ${TARGET_PREFIX#/}/lib/systemd

	# should be done in git.
	mv ${TARGET_PREFIX#/}/lib/ca-certificates/update.d/{,50}java.run
	mv ${TARGET_PREFIX#/}/lib/ca-certificates/update.d/{,70}openssl.run
	mv ${TARGET_PREFIX#/}/lib/ca-certificates/update.d/{,80}etc_ssl.run
	# certbundle.run must be run after etc_ssl.run as it uses a timestamp from it
	mv ${TARGET_PREFIX#/}/lib/ca-certificates/update.d/{,99}certbundle.run

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif
done


%install

%rpmint_cflags

%if "%{buildtype}" == "cross"
%else
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}



%files
%defattr(-,root,root)
%license COPYING
%{_isysroot}%{_rpmint_target_prefix}/sbin/update-ca-certificates
%{_isysroot}/etc
%{_isysroot}/var
%{_isysroot}%{_rpmint_target_prefix}/lib/%{pkgname}
%{_isysroot}%{_rpmint_target_prefix}/share/pki/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*



%changelog
* Wed Apr 05 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
