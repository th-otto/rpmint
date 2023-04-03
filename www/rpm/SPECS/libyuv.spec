%define pkgname libyuv

%rpmint_header

Summary:        Open source project that includes YUV scaling and conversion functionality
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1837
Release:        1
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://chromium.googlesource.com/libyuv/libyuv/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz
Patch0:  patches/%{pkgname}/%{pkgname}-1837-mint.patch

%rpmint_essential
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-gcc-c++
Provides:       cross-mint-libyuv-devel
%else
BuildRequires:  gcc-c++
Provides:       libyuv-devel
%endif

%rpmint_build_arch

%description
libyuv is an open source project that includes YUV scaling and conversion functionality.

You need to use g++ to link against this library.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CC="${TARGET}-gcc" \
	CXX="${TARGET}-g++" \
	AR="${TARGET}-ar" \
	ARFLAGS=rcs \
	RANLIB=${TARGET}-ranlib \
	NM=${TARGET}-nm \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	make -f linux.mk V=1 %{?_smp_mflags}

	# there is no install target :/
	DESTDIR=%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}
	mkdir -p "$DESTDIR/bin" "$DESTDIR/include" "$DESTDIR/lib$multilibdir"
	cp -pr include/. "$DESTDIR/include"
	cp libyuv.a "$DESTDIR/lib$multilibdir"
	for i in i444tonv12_eg cpuid yuvconvert yuvconstants psnr; do
		cp $i "$DESTDIR/bin"
	done

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

	make -f linux.mk clean
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
%{_isysroot}%{_rpmint_target_prefix}/bin
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib



%changelog
* Sat Apr 01 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
