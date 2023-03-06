%define pkgname openssl

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

%define _sonum  1_1
Summary:        Secure Sockets and Transport Layer Security
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.1.1p
Release:        1
License:        OpenSSL
Group:          Productivity/Networking/Security

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://www.openssl.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://www.openssl.org/source/%{pkgname}-%{version}.tar.gz
Patch0: patches/openssl/openssl-1.1.1p-mint.patch
Patch1: patches/openssl/openssl-zlib-static.patch

%rpmint_essential
BuildRequires:  pkgconfig
%if "%{buildtype}" == "cross"
Provides:       pkgconfig(cross-mint-libssl) = %{version}
Provides:       pkgconfig(cross-mint-libcrypto) = %{version}
Provides:       pkgconfig(cross-mint-openssl) = %{version}
%else
Provides:       pkgconfig(libssl) = %{version}
Provides:       pkgconfig(libcrypto) = %{version}
Provides:       pkgconfig(openssl) = %{version}
%endif

%if "%{buildtype}" == "cross"
BuildArch:      noarch
%else
%define _target_platform %{_rpmint_target_platform}
%if "%{buildtype}" == "v4e"
%define _arch m5475
%else
%if "%{buildtype}" == "020"
%define _arch m68020
%else
%define _arch m68k
%endif
%endif
%endif

%define SSLETCDIR /etc/ssl

%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, full-featured, and open source toolkit implementing
the Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS
v1) protocols with full-strength cryptography. The project is managed
by a worldwide community of volunteers that use the Internet to
communicate, plan, and develop the OpenSSL toolkit and its related
documentation.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1


%build

%rpmint_cflags

CONFIGURE_FLAGS="--prefix=%{_rpmint_target_prefix} --cross-compile-prefix=${TARGET}- ${CONFIGURE_FLAGS_AMIGAOS}
	 --openssldir=%{SSLETCDIR}
	zlib
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

targetconf_000=mint
targetconf_020=mint020
targetconf_v4e=mintv4e


for CPU in ${ALL_CPUS}; do
	eval targetconf=\${targetconf_$CPU}
	"./Configure" ${CONFIGURE_FLAGS} $targetconf

	make %{?_smp_mflags}
	make MANDIR=%{_rpmint_target_prefix}/share/man DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make distclean
done


%install

%rpmint_cflags

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
rm -rf %{buildroot}/etc
mv %{buildroot}%{_rpmint_sysroot}/etc %{buildroot}/etc
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}/*.pc
%{_rpmint_datadir}
%{_rpmint_sysroot}%{SSLETCDIR}
%else
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%{SSLETCDIR}
%endif




%changelog
* Sun Mar 5 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
