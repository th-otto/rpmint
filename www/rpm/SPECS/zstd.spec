%define pkgname zstd
%define libname libzstd1

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

%rpmint_header

Summary       : Zstandard compression tools
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 1.5.4
Release       : 1
License       : BSD-3-Clause and GPL-2.0
Group         : Productivity/Archiving/Compression

%rpmint_essential
%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-zlib-devel
%else
BuildRequires : zlib-devel
%endif

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : https://github.com/facebook/zstd/releases

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: https://github.com/facebook/zstd/releases/download/v%{version}/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/%{pkgname}/zstd-compiler.h.patch

%rpmint_build_arch


%description
Zstd, short for Zstandard, is a lossless compression algorithm. Speed
vs. compression trade-off is configurable in small increments.
Decompression speed is preserved and remains roughly the same at all
settings, a property shared by most LZ compression algorithms, such
as zlib or lzma.

At roughly the same ratio, zstd (v1.4.0) achieves ~870% faster
compression than gzip. For roughly the same time, zstd achives a
~12% better ratio than gzip. LZMA outperforms zstd by ~10% faster
compression for the same ratio, or ~1-4% size reduction for same time.

%package devel
Summary       : Development files for the Zstd compression library
Group         : Development/Libraries/C and C++
%if "%{buildtype}" == "cross"
Provides      : cross-mint-lib%{pkgname}-devel = %{version}
Requires      : cross-mint-%{pkgname} = %{version}
%else
Provides      : lib%{pkgname}-devel = %{version}
Requires      : %{pkgname} = %{version}
%endif

%description devel
Zstd, short for Zstandard, is a lossless compression algorithm,
targeting faster compression than zlib at comparable ratios.

Needed for compiling programs that link with the library.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

cp "%{S:1}" config.sub

# conflicts with mintlib header file of the same name
mv lib/common/compiler.h lib/common/zcompiler.h

%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags
STACKSIZE="-Wl,-stack,256k"

export prefix=%{_rpmint_target_prefix}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	export CC=${TARGET}-gcc
	export AR=${TARGET}-ar
	export CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	export LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}"
	export libdir="${prefix}/lib$multilibdir"

	make %{?_smp_mflags} -C lib libzstd.a
	make %{?_smp_mflags} -C programs

	make DESTDIR="%{buildroot}%{_rpmint_sysroot}" -C lib install-static install-pc install-includes
	make DESTDIR="%{buildroot}%{_rpmint_sysroot}" -C programs install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs

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
%{_isysroot}%{_rpmint_target_prefix}/bin/*

%files devel
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%{_isysroot}%{_rpmint_target_prefix}/share/*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}/*.pc
%endif


%changelog
* Fri Mar 24 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
- Update to version 1.5.4
