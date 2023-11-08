%define pkgname SDL_gfx

%rpmint_header

Summary:        SDL Graphics Routines for Primitives and Other Support Functions
Name:           %{crossmint}%{pkgname}
Version:        2.0.26
Release:        1
License:        Zlib
Group:          Development/Libraries/X11

Packager:       %{packager}
URL:            http://www.ferzkopp.net/wordpress/2016/01/02/sdl_gfx-sdl2_gfx/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://www.ferzkopp.net/Software/SDL_gfx-2.0/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  automake
BuildRequires:  pkgconfig
BuildRequires:  %{crossmint}SDL-devel
BuildRequires:  make
BuildRequires:  dos2unix
Provides:       %{crossmint}lib%{pkgname}-devel = %{version}

%rpmint_build_arch

%description
The SDL_gfx library evolved out of the SDL_gfxPrimitives code which
provided basic drawing routines such as lines, circles or polygons and
SDL_rotozoom which implemented a interpolating rotozoomer for SDL
surfaces. The current components of the SDL_gfx library are:

- Graphic Primitives (SDL_gfxPrimitves.h)

- Rotozoomer (SDL_rotozoom.h)

- Framerate control (SDL_framerate.h)

- MMX image filters (SDL_imageFilter.h)

The library is backwards compatible to the above mentioned code. It is
written in plain C and can be used in C++ code.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

rm -f aclocal.m4 ltmain.sh ltconfig
libtoolize --force || exit 1
aclocal -I m4 || exit 1
autoconf || exit 1
automake --force --copy --add-missing || exit 1
cp %{S:1} config.sub
dos2unix README
chmod 644 LICENSE AUTHORS ChangeLog NEWS README

%build

%rpmint_cflags
COMMON_CFLAGS+=" -fno-strict-aliasing"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-static
	--disable-shared
	--without-pic
	--disable-mmx
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

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

	make clean >/dev/null
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
%doc AUTHORS ChangeLog NEWS README
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Wed Nov 08 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
