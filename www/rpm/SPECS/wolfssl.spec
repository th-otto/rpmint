%define pkgname wolfssl

%rpmint_header

Summary:        Embedded TLS Library
Name:           %{crossmint}%{pkgname}
Version:        5.5.1
Release:        1
License:        GPL-2.0-or-later
Group:          Productivity/Networking/Security

Packager:       %{packager}
URL:            https://www.wolfssl.com/
VCS:            https://github.com/wolfssl/wolfssl

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.bz2
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/%{pkgname}/wolfssl-5.5.0-mint.patch
Patch1:  patches/%{pkgname}/wolfssl-single-thread.patch

%rpmint_essential
BuildRequires:  make
Provides:       %{crossmint}libwolfssl-devel

%rpmint_build_arch

%description
The wolfSSL embedded TLS library is a lightweight, portable,
C-language-based SSL/TLS library targeted at IoT, embedded, and RTOS
environments primarily because of its size, speed, and feature set. It
works seamlessly in desktop, enterprise, and cloud environments as
well. wolfSSL supports industry standards up to the current TLS 1.3 and
DTLS 1.3, is up to 20 times smaller than OpenSSL, offers a simple API,
an OpenSSL compatibility layer, OCSP and CRL support, is backed by the
robust wolfCrypt cryptography library, and much more.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

./autogen.sh
cp "%{S:1}" build-aux/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-opensslextra
	--enable-supportedcurves
	--disable-jobserver
	--enable-sp
	--enable-ed25519
	--enable-des3
	--enable-ripemd
	--enable-all-crypto
	--enable-singlethreaded
	--disable-asyncthreads
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CC="${TARGET}-gcc" \
	AR="${TARGET}-ar" \
	RANLIB="${TARGET}-ranlib" \
	NM=${TARGET}-nm \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	make V=1 %{?_smp_mflags}
	make prefix="%{buildroot}%{_rpmint_sysroot}/%{_rpmint_target_prefix}" install
	make distclean
	rm -f "%{buildroot}%{_rpmint_sysroot}/%{_rpmint_target_prefix}/bin/wolfssl-config"

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif
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
%license COPYING
%doc README.md ChangeLog.md
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%{_isysroot}%{_rpmint_target_prefix}/share/doc/wolfssl
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Tue Apr 04 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
