%define pkgname libvpx

%rpmint_header

Summary:        VP8/VP9 codec library
Name:           %{crossmint}%{pkgname}
Version:        1.13.1
Release:        1
License:        BSD-3-Clause AND GPL-2.0-or-later
Group:          Productivity/Multimedia/Other

Packager:       %{packager}
URL:            https://www.webmproject.org/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz

Patch0: patches/libvpx/libvpx-mint.diff

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig
BuildRequires:  make
Provides:       %{crossmint}%{pkgname}-devel = %{version}

%rpmint_build_arch

%description
WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VP8 video codec
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%patch0 -p1

%build

%rpmint_cflags
COMMON_CFLAGS+=" -fno-strict-aliasing"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#
# SDL is only needed for the example
#
CONFIGURE_FLAGS="--prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
	--disable-unit-tests
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CHOST="$TARGET" \
	LD="${TARGET}-gcc" \
	CC="${TARGET}-gcc" \
	CXX="${TARGET}-g++" \
	AR="${ar}" \
	RANLIB=${ranlib} \
	NM=${TARGET}-nm \
	STRIP=${TARGET}-strip \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} --libdir="%{_rpmint_target_prefix}/lib$multilibdir" || exit 1

	# the --size-limit switch is broken atm ...
	echo "#undef CONFIG_SIZE_LIMIT" >> vpx_config.h
	echo "#define CONFIG_SIZE_LIMIT 1" >> vpx_config.h
	echo '#define DECODE_WIDTH_LIMIT 8192'  >> vpx_config.h
	echo '#define DECODE_HEIGHT_LIMIT 8192' >> vpx_config.h

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

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
%license LICENSE
%doc AUTHORS README CHANGELOG
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/bin
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Mon Nov 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
