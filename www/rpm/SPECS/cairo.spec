%define pkgname cairo

%rpmint_header

Summary:        Vector Graphics Library with Cross-Device Output Support
Name:           %{crossmint}%{pkgname}
Version:        1.18.0
Release:        1
License:        LGPL-2.1-or-later OR MPL-1.1
Group:          Development/Libraries/C and C++

Packager:       %{packager}
URL:            https://cairographics.org

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://cairographics.org/releases/%{pkgname}-%{version}.tar.xz
Source1: patches/meson/m68k-atari-mint.txt
Source2: patches/meson/m68k-atari-mintelf.txt

Patch0: patches/cairo/cairo-get_bitmap_surface-bsc1036789-CVE-2017-7475.diff
Patch1: patches/cairo/cairo-xlib-endianness.patch
Patch2: patches/cairo/cairo-mint.patch

%rpmint_essential
BuildRequires:  meson
BuildRequires:  pkgconfig
BuildRequires:  %{crossmint}freetype2
BuildRequires:  %{crossmint}libpng
BuildRequires:  %{crossmint}zlib
BuildRequires:  %{crossmint}libpixman-devel
Provides:       %{crossmint}%{pkgname}-devel = %{version}

%rpmint_build_arch

%description
Cairo is a vector graphics library with cross-device output support.
Currently supported output targets include the X Window System,
in-memory image buffers, and PostScript. Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

cp %{S:1} .
cp %{S:2} .

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%rpmint_cflags
COMMON_CFLAGS+=" -fno-strict-aliasing"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

export PKG_CONFIG=${TARGET}-pkg-config

CONFIGURE_FLAGS="--cross-file ${TARGET}.txt --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	-D xcb=disabled
	-D freetype=enabled
	-D fontconfig=disabled
	-D glib=disabled
	-D gtk_doc=false
	-D spectre=disabled
	-D symbol-lookup=disabled
	-D tee=enabled
	-D tests=disabled
	-D xlib=disabled
	-D default_library=static
	-D buildtype=release
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	rm -rf build
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	meson setup ${CONFIGURE_FLAGS} --libdir="%{_rpmint_target_prefix}/lib$multilibdir" build || exit 1
	sed -i 's/-fPIC//g' build/meson-info/intro-targets.json build/build.ninja build/compile_commands.json
	echo "#undef CAIRO_HAS_PTHREAD" >> build/config.h
	echo "#undef CAIRO_HAS_REAL_PTHREAD" >> build/config.h
	echo "#define CAIRO_NO_MUTEX 1" >> build/config.h

	meson compile -C build || exit 1
	DESTDIR=%{buildroot}%{_rpmint_sysroot} meson install -C build || exit 1

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
%defattr(-,root,root)
%license COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1
%doc AUTHORS NEWS README.md
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Mon Nov 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
