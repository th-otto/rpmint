%define pkgname SDL_mixer

%rpmint_header

Summary:        SDL sound mixer library
Name:           %{crossmint}%{pkgname}
Version:        1.2.13
Release:        1
License:        Zlib
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://libsdl.org/projects/SDL_mixer/release-1.2.html
VCS:            https://github.com/libsdl-org/SDL_mixer/tree/SDL-1.2

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root


Source0: %{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/sdl_mixer/sdl_mixer-double-free-crash.patch
Patch1: patches/sdl_mixer/sdl_mixer-config.patch
patch2: patches/sdl_mixer/sdl_mixer-amigaos.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  %{crossmint}libSDL-devel >= 1.2.15
BuildRequires:  %{crossmint}libogg-devel
BuildRequires:  %{crossmint}libvorbis-devel
BuildRequires:  %{crossmint}libmikmod-devel
BuildRequires:  %{crossmint}libFLAC-devel
BuildRequires:  %{crossmint}mpg123-devel
Provides:       %{crossmint}libSDL_mixer-devel = %{version}

%rpmint_build_arch

%description
A multichannel audio mixer. It supports four channels of 16-bit stereo
audio, plus a single channel of music, mixed by the popular MikMod MOD,
Timidity MIDI, and SMPEG MP3 libraries.

Cross compiling hint: on modern platforms, it is sufficient to just link
against SDL_mixer, because the other libraries are referenced there as
shared libraries. Since for atari we have only static libraries, you
have to link those explicitly. The correct link command (order is important) is:

-lSDL_mixer -lSDL -lFLAC -lvorbisfile -lvorbis -lmikmod -logg -lmpg123 -lgem -lm

See also other hints about SDL.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
#%%patch0 -p1
%patch1 -p1
%patch2 -p1


rm -f aclocal.m4 build-scripts/ltmain.sh acinclude/libtool.m4 acinclude/lt*
libtoolize --force
aclocal -I acinclude
autoconf
# automake --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} build-scripts/config.sub

#
# check that sdl.pc was installed.
# without it, SDL.m4 uses the sdl-config script from the host
# which does not work when cross-compiling
#
if test "`pkg-config --modversion sdl 2>/dev/null`" = ""; then
	echo "SDL and/or sdl.pc is missing" >&2
	exit 1
fi

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

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	LIBS="-lm" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR="%{buildroot}%{_rpmint_sysroot}" install
	rm -f "%{buildroot}%{_rpmint_bindir}/sdl-config"

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
%license COPYING
%doc README* CHANGES
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Sat Apr 08 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 1.2.13

