%define pkgname curl

%rpmint_header

%bcond_without openssl

Summary:        A Tool for Transferring Data from URLs
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        7.56.0
Release:        1
License:        curl
Group:          Productivity/Networking/Web/Utilities

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://curl.haxx.se/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://curl.haxx.se/download/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/curl-dont-mess-with-rpmoptflags.diff
Patch1: patches/%{pkgname}/curl-mint-build.patch
Patch2: patches/%{pkgname}/curl-secure-getenv.patch
Patch3: patches/%{pkgname}/curl-staticlibs.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  groff
BuildRequires:  perl
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-zlib
BuildRequires:  cross-mint-libiconv
%if %{with openssl}
BuildRequires:  cross-mint-openssl
%endif
BuildRequires:  cross-mint-libxml2
BuildRequires:  cross-mint-libidn2
BuildRequires:  cross-mint-libmetalink
BuildRequires:  cross-mint-nghttp2
BuildRequires:  cross-mint-libssh2
BuildRequires:  cross-mint-libpsl
%else
BuildRequires:  pkgconfig(libnghttp2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libssh2)
BuildRequires:  pkgconfig(libpsl)
%if %{with openssl}
BuildRequires:  pkgconfig(libssl)
%endif
BuildRequires:  libiconv
%endif

%rpmint_build_arch

%description
Curl is a client to get documents and files from or send documents to a
server using any of the supported protocols (HTTP, HTTPS, FTP, FTPS,
TFTP, DICT, TELNET, LDAP, or FILE). The command is designed to work
without user interaction or any kind of interactivity.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp %{S:1} config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname}
	--disable-ipv6
	--with-gssapi=%{_rpmint_target_prefix}/lib/mit
	--with-libidn2
	--with-libssh2
	--with-libmetalink
	--disable-shared
	--enable-static
	--disable-threaded-resolver
"

%if %{with openssl}
	CONFIGURE_FLAGS+="
	--with-ssl
	--with-ca-fallback
	--without-ca-path
	--without-ca-bundle"
%else
	CONFIGURE_FLAGS+=" --without-ssl"
%endif

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs

	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias
	rm -f %{buildroot}%{_rpmint_bindir}/curl-config

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make clean
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
%if "%{buildtype}" == "cross"
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}
%{_rpmint_datadir}
%else
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%endif



%changelog
* Mon Mar 6 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
