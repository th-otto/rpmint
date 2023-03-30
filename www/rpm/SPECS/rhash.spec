%define pkgname rhash

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Recursive Hasher
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.3.8
Release:        1
License:        MIT
Group:          Productivity/File utilities

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/rhash/RHash

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

# https://github.com/rhash/RHash/archive/v%%{version}.tar.gz
Source0: %{pkgname}-%{version}.tar.gz
Patch0:  patches/%{pkgname}/%{pkgname}-%{version}-shared.patch

%rpmint_essential
BuildRequires:  make
%if "%{buildtype}" == "cross"
Provides:       cross-mint-librhash-devel
Provides:       pkgconfig(cross-mint-librhash)
%else
Provides:       librhash-devel
Provides:       pkgconfig(librhash)
%endif

%rpmint_build_arch

%description
RHash (Recursive Hasher) is a console utility for computing and
verifying magnet links and hash sums of files.
It supports CRC32, MD4, MD5, SHA1/SHA2, Tiger, DC++ TTH, BitTorrent
BTIH, AICH, eDonkey hash, GOST R 34.11-94, RIPEMD-160, HAS-160, EDON-R,
Whirlpool and Snefru hash algorithms. Hash sums are used to ensure and
verify integrity of large volumes of data for a long-term storing or
transferring.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n RHash-%{version}
%patch0 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

STACKSIZE="-Wl,-stack,256k"

CONFIGURE_FLAGS="--prefix=%{_rpmint_target_prefix} --disable-lib-shared --enable-lib-static --enable-static --sysconfdir=/etc"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CC="${TARGET}-gcc" \
	AR="{TARGET}-ar" \
	RANLIB={TARGET}-ranlib \
	OPTFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -D_GNU_SOURCE" \
	OPTLDFLAGS="$CPU_CFLAGS ${STACKSIZE}" \
		./configure $CONFIGURE_FLAGS

	# Don't run parallel make $JOBS -- it doesn't work.
	make \
		CC="${TARGET}-gcc" \
		AR="${TARGET}-ar" \
		RANLIB=${TARGET}-ranlib \
		OPTFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -D_GNU_SOURCE" \
		OPTLDFLAGS="$CPU_CFLAGS ${STACKSIZE}" \
		lib-static all

	make \
		PREFIX=%{_rpmint_target_prefix} LIBDIR="%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib${multilibdir}" DESTDIR="%{buildroot}%{_rpmint_sysroot}" \
		install install-lib-static install-man install-conf install-pkg-config
	make -C librhash \
		PREFIX=%{_rpmint_target_prefix} DESTDIR="%{buildroot}%{_rpmint_sysroot}" \
		install-lib-headers
	
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
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
	%endif

	make clean
done


%install

%rpmint_cflags

%rpmint_strip_archives

# create pkg-config file
mkdir -p %{buildroot}%{_rpmint_libdir}/pkgconfig
cat > %{buildroot}%{_rpmint_libdir}/pkgconfig/librhash.pc <<-EOF
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: librhash
Description: RHash is a utility for computing and verifying hash sums of files
Version: %{version}
URL: http://rhash.anz.ru/

Libs: -lrhash
Cflags:
EOF

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
%config(noreplace) %{_isysroot}/etc/rhashrc
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Thu Mar 30 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
