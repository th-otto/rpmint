%define pkgname SDL

%rpmint_header

Summary:        Simple DirectMedia Layer Library
Name:           %{crossmint}%{pkgname}
Version:        1.2.16
Release:        1
License:        LGPL-2.1-or-later
Group:          Development/Libraries/X11

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://www.libsdl.org/
VCS:            https://github.com/SDL-mirror/SDL/tree/SDL-1.2

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root


Source0: %{pkgname}-%{version}-hg.tar.xz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/sdl/sdl-1.2.16-asm.patch
Patch1:  patches/sdl/sdl-gsxb.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  %{crossmint}gemlib
BuildRequires:  %{crossmint}ldg-devel
Provides:       %{crossmint}libSDL-devel = %{version}
Provides:       %{crossmint}SDL-devel = %{version}

%rpmint_build_arch

%description
SDL is the Simple DirectMedia Layer library. It is a low-level and cross-platform
library for building games or similar programs.
Thanks to Patrice Mandin, SDL is available on Atari platforms. SDL programs can
run either in full screen or in a GEM window, depending on the SDL_VIDEODRIVER
environment variable.

Cross compiling hint: in many autoconf/automake based packages, the presence of SDL
is checked for by searching for a sdl-config script. Most likely, the one found will
be the one for your host system. This has the bad effect of adding absolute
search paths like /usr/include/SDL and /usr/lib. If that happens, you have to
manually edit config.status after running configure, and remove those flags.
In some cases, you have to add -I/usr/m68k-atari-mint/sys-root/usr/include/SDL instead.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}-hg
%patch0 -p1
%patch1 -p1

rm -f aclocal.m4 ltmain.sh acinclude/libtool.m4 acinclude/lt*
libtoolize --force
aclocal -I acinclude
autoconf
#automake --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} build-scripts/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-video-opengl
	--disable-threads
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	# ICONV isn't really used
	sed -i 's/ -liconv//' config.status
	./config.status

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
%doc README* BUGS CREDITS TODO WhatsNew
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Sat Apr 08 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 1.2.16-hg

