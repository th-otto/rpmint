%define pkgname ncurses

%rpmint_header

Summary:        Terminal control library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        6.0
Release:        1
License:        MIT
Group:          System/Base

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://invisible-island.net/ncurses/ncurses.html

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: ftp://ftp.gnu.org/pub/gnu/%{pkgname}/%{pkgname}-%{version}.tar.gz
Source1: patches/ncurses/ncurses-6.0-patches.tar.bz2
Source2: patches/automake/mintelf-config.sub
Patch1: patches/ncurses/ncurses-6.0.dif
Patch2: patches/ncurses/ncurses-5.9-ibm327x.dif
Patch3: patches/ncurses/ncurses-6.0-0003-overwrite.patch
Patch4: patches/ncurses/ncurses-6.0-0005-environment.patch
Patch5: patches/ncurses/ncurses-6.0-0010-source.patch
Patch6: patches/ncurses/ncurses-6.0-0011-termcap.patch
Patch7: patches/ncurses/ncurses-6.0-0020-configure.patch
Patch9: patches/ncurses/ncurses-6.0-0022-dynamic.patch
Patch10: patches/ncurses/ncurses-no-include.patch


%rpmint_essential
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-gcc-c++
BuildRequires:  gcc-c++
Provides:       cross-mint-terminfo-base
Provides:       cross-mint-libncurses5
Provides:       cross-mint-libncurses6
Provides:       cross-mint-ncurses-devel
%else
BuildRequires:  gcc-c++
Provides:       terminfo-base
Provides:       libncurses5
Provides:       libncurses6
Provides:       ncurses-devel
%endif

%rpmint_build_arch

%description
Ncurses is a library which allows building full-screen text mode programs,
such as <code>vim</code>, <code>less</code>, or the GDB text UI.

%prep
%setup -q -n %{pkgname}-%{version}

mkdir -p "%{pkgname}-patches"
tar -C "%{pkgname}-patches" --strip-components=1 -xjf "%{S:1}"
for patch in %{pkgname}-patches/%{pkgname}*.patch
do
    patch -f -T -p1 -s --read-only=ignore < $patch
done
rm -rf "%{pkgname}-patches"
find -name '*.orig' -delete

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1
%patch10 -p1

cp %{S:2} config.sub

%define MINT_BUILD_DIR %{_builddir}/%{?buildsubdir}/build-target
%define HOST_BUILD_DIR %{_builddir}/%{?buildsubdir}/build-host

rm -fr tack
rm -f Ada95/src/terminal_interface-curses.adb
rm -f mkinstalldirs
# rm -vf include/ncurses_dll.h
rm -vf mkdirs.sh
rm -vf tar-copy.sh
rm -vf mk-dlls.sh
# do not run aclocal here, ncurses uses
# its own package of macros which are not
# delivered in the tarball
: aclocal || exit 2
: autoconf || exit 2
: autoheader || exit 2
rm -rf autom4te.cache config.h.in.orig

%build

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer -D_REENTRANT -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"

CC_FOR_BUILD=gcc
CXX_FOR_BUILD=g++

CC_FOR_TARGET="%{_rpmint_target}-gcc"
CXX_FOR_TARGET="%{_rpmint_target}-g++"

ENABLE_SHARED_TARGET=no

TARGET_CONFIGURE_ARGS="--prefix=%{_rpmint_target_prefix} --host=${TARGET}"
BUILD_CONFIGURE_ARGS="--prefix=%{_prefix}"

configure_ncurses_for_build()
{
	local speed_t with_gpm dlsym shared without_cxx termcap disable_root mixedcase

	CC="$CC_FOR_BUILD"
	CXX="$CXX_FOR_BUILD"
	CFLAGS=
	LDFLAGS=

	speed_t=
	with_gpm=--without-gpm
	dlsym=--without-dlsym
	disable_root=--disable-root-environ
	shared=
	without_cxx=
	termcap=
	mixedcase=
	case $BUILD in
		*-*-mingw*) CFLAGS="$CFLAGS -DWINVER=0x0501"; ;;
		*) speed_t=--with-ospeed=speed_t ;;
	esac
	shared="--without-shared --without-cxx-shared"
	without_cxx="--without-cxx --without-cxx-bindings"
	CXXFLAGS="$CFLAGS"

	# the program we build here is used to generate
	# the terminfo database for the TARGET, not the BUILD system
	case $TARGET in
		*-os2-emx*|*-msdosdjgpp*|*-cygwin*|*-msys*|*-mingw*|*-uwin*)
			mixedcase=--enable-mixed-case=no
			;;
		*-atari-mint*)
			mixedcase=--enable-mixed-case=yes
			;;
	esac
	export CC CXX CFLAGS CXXFLAGS LDFLAGS TERM GZIP PATH TMPDIR

	cd "%{HOST_BUILD_DIR}" || exit 1
	if true
	then
		test -f Makefile && make clean
		echo "configure $NAME for $BUILD:"
			${srcdir}/configure \
			$BUILD_CONFIGURE_ARGS \
			CFLAGS="$CFLAGS" \
			CXXFLAGS="$CXXFLAGS" \
			LDFLAGS="$LDFLAGS" \
			--without-ada \
			--without-debug \
			--without-profile \
			--without-manpage-tbl \
			--with-manpage-format=gzip \
			--with-manpage-renames=${srcdir}/man/man_db.renames \
			--with-manpage-aliases	\
			--enable-term-driver \
			--enable-pc-files \
			--with-pkg-config-libdir="${prefix}/lib/pkgconfig" \
			--disable-rpath \
			--disable-rpath-hack \
			--with-normal \
			--disable-tic-depends \
			--with-xterm-kbs=del \
			--disable-leaks \
			--disable-xmc-glitch \
			--enable-symlinks \
			--enable-big-core \
			--enable-const \
			--enable-hashmap \
			--enable-no-padding	\
			--enable-sigwinch \
			--enable-colorfgbg	\
			--enable-sp-funcs \
			--enable-interop \
			--enable-weak-symbols \
			--enable-wgetch-events \
			--enable-pthreads-eintr \
			--disable-string-hacks \
			$(test $abi -ge 6 && echo $abi6_conf_args || echo $abi5_conf_args) \
			$withchtype \
			$speed_t \
			$with_gpm \
			$shared \
			$without_cxx \
			$termcap \
			$disable_root \
			$mixedcase \
			"$@" \
			|| exit $?
	fi
}


configure_ncurses()
{
	cd "%{MINT_BUILD_DIR}"
	if true
	then
		test -f Makefile && make clean
		echo "configure $NAME:"
			${srcdir}/configure \
			$TARGET_CONFIGURE_ARGS \
			CFLAGS="$COMMON_CFLAGS $CPU_CFLAGS" \
			CXXFLAGS="$COMMON_CFLAGS $CPU_CFLAGS" \
			LDFLAGS="$LDFLAGS" \
			--without-ada \
			--without-debug \
			--without-profile \
			--without-manpage-tbl \
			--with-manpage-format=gzip \
			--with-manpage-renames=${srcdir}/man/man_db.renames \
			--with-manpage-aliases	\
			--enable-term-driver \
			--enable-pc-files \
			--with-pkg-config-libdir="%{_rpmint_target_prefix}/lib/pkgconfig" \
			--disable-rpath \
			--disable-rpath-hack \
			--with-normal \
			--disable-tic-depends \
			--with-xterm-kbs=del \
			--disable-leaks \
			--disable-xmc-glitch \
			--enable-symlinks \
			--enable-big-core \
			--enable-const \
			--enable-hashmap \
			--enable-no-padding	\
			--enable-sigwinch \
			--enable-colorfgbg \
			--enable-sp-funcs \
			--enable-interop \
			--disable-weak-symbols \
			--enable-wgetch-events \
			--enable-pthreads-eintr \
			--disable-string-hacks \
			$(test $abi -ge 6 && echo $abi6_conf_args || echo $abi5_conf_args) \
			$withchtype \
			$speed_t \
			$with_gpm \
			$shared \
			$without_cxx \
			$termcap \
			$disable_root \
			$mixedcase \
			"$@" \
			|| exit $?
		: hack_lto_cflags
	fi
}


build_ncurses()
{
	local TERM="$TERM"
	local SCREENDIR SCREENRC SCREENLOG TMPDIR
	local NAME
	local CC CXX CFLAGS CXXFLAGS LDFLAGS
	local withchtype
	local screen="screen -L -D -m"
	local PATH="$PATH"
	local FALLBK="xterm,linux,vt100,vt102,cygwin"
	local GZIP="-9"
	local speed_t with_gpm dlsym shared without_cxx termcap disable_root mixedcase
	local abi
	local abi5_conf_args="--without-pthread --disable-reentrant --disable-ext-mouse --disable-widec --disable-ext-colors"
	local abi6_conf_args="--with-pthread    --enable-reentrant  --enable-ext-mouse  --enable-widec  --enable-ext-colors"
	local BUILD_TIC BUILD_INFOCMP
	
	srcdir=`pwd`

	NAME=%{pkgname}-%{version}
	abi=5

	if true; then
		withchtype=--with-chtype=long
		configure_ncurses_for_build
		make %{?_smp_mflags} -C include &&
		make %{?_smp_mflags} -C ncurses fallback.c FALLBACK_LIST="" &&
		make %{?_smp_mflags} -C progs termsort.c &&
		make %{?_smp_mflags} -C progs transform.h &&
		make %{?_smp_mflags} -C progs infocmp$BUILD_EXEEXT &&
		make %{?_smp_mflags} -C progs tic$BUILD_EXEEXT \
		|| exit $?
		BUILD_TIC=%{HOST_BUILD_DIR}/progs/tic$BUILD_EXEEXT
		BUILD_INFOCMP=%{HOST_BUILD_DIR}/progs/infocmp$BUILD_EXEEXT
		PATH="%{HOST_BUILD_DIR}/progs:$PATH"
	else
		BUILD_TIC=tic
		BUILD_INFOCMP=infocmp
	fi
	cd "%{MINT_BUILD_DIR}"
	
	CC="$CC_FOR_TARGET"
	CXX="$CXX_FOR_TARGET"
	LDFLAGS="-Wl,-stack,256k"
	: cflags -Wl,-O2                  LDFLAGS
	: cflags -Wl,-Bsymbolic-functions LDFLAGS
	: cflags -Wl,--hash-size=8599     LDFLAGS
	: cflags -Wl,--as-needed          LDFLAGS
	
	# be sure that we use an unsigned long for chtype to be
	# backward compatible with ncurses 5.4
	withchtype=--with-chtype=long
	
	# No --enable-tcap-names because we may have to recompile
	# programs or foreign programs won't work
	#
	# No --enable-safe-sprintf because this seems to
	# crash on some architectures
	#
	# No --enable-xmc-glitch because this seems to break yast2
	# on console/konsole (no magic cookie support on those?)
	#
	# No --with-termlib=tinfo because libncurses depend on
	# libtinfo (is linked with) and therefore there is no
	# advantage about splitting of a libtinfo (IMHO).
	#
	# No --enable-hard-tabs for users which have disabled
	# the use of tabs
	#
	speed_t=
	with_gpm=
	dlsym=
	disable_root=
	shared=
	without_cxx=
	termcap=
	mixedcase=
	case $TARGET in
		*-*-mingw*) COMMON_CFLAGS="$COMMON_CFLAGS -DWINVER=0x501"; ;;
		*-atari-mint*) disable_root=--disable-root-environ ;;
		*) speed_t=--with-ospeed=speed_t with_gpm=--with-gpm dlsym=--with-dlsym disable_root=--disable-root-environ ;;
	esac
	case $TARGET in
		*-os2-emx*|*-msdosdjgpp*|*-cygwin*|*-msys*|*-mingw*|*-uwin*)
			mixedcase=--enable-mixed-case=no
			;;
		*-atari-mint*)
			mixedcase=--enable-mixed-case=yes
			;;
	esac
	case $ENABLE_SHARED_TARGET in
		*--enable-shared*) shared="--with-shared --with-cxx-shared" ;;
	esac
	if test "$CXX_FOR_TARGET" = "" ; then
		without_cxx="--without-cxx --without-cxx-bindings"
	fi

	cd "%{MINT_BUILD_DIR}"

	SCREENDIR=$(mktemp -d ${PWD}/screen.XXXXXX) || exit 1
	SCREENRC=${SCREENDIR}/ncurses
	export SCREENRC SCREENDIR
	SCREENLOG=${SCREENDIR}/log
	cat > $SCREENRC <<-EOF
	deflogin off
	logfile $SCREENLOG
	logfile flush 1
	logtstamp off
	log on
	setsid on
	scrollback 0
	silence on
	utf8 on
EOF
	
	TMPDIR=$(mktemp -d /tmp/ncurses.XXXXXXXX) || exit 1
	export CC CXX CFLAGS CXXFLAGS LDFLAGS TERM GZIP PATH TMPDIR
	
	for CPU in ${ALL_CPUS}; do
		eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
		eval multilibdir=\${CPU_LIBDIR_$CPU}
		configure_ncurses
		pwd
		ls -l
		test -z "$CXX_FOR_TARGET" || make -C c++ etip.h || exit 1
		make %{?_smp_mflags} || exit $?
		make DESTDIR="%{buildroot}%{_rpmint_sysroot}" includesubdir=/ncurses libdir=%{_rpmint_target_prefix}/lib/$multilibdir install || exit $?
		( cd "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/include"; $LN_S -f ncurses/{curses,ncurses,term,termcap}.h . )
	
		# remove obsolete config script
		rm -f %{buildroot}%{_rpmint_bindir}/ncurses*-config
		%if "%{buildtype}" != "cross"
		if test "%{buildtype}" != "$CPU"; then
			rm -f %{buildroot}%{_rpmint_bindir}/*
		fi
		%rpmint_make_bin_archive $CPU
		%endif

	done
		
	# Now use --enable-widec for UTF8/wide character support.
	# The libs with 16 bit wide characters are binary incompatible
	# to the normal 8bit wide character libs.
	#
	if true; then
		for CPU in ${ALL_CPUS}; do
			eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
			eval multilibdir=\${CPU_LIBDIR_$CPU}
			configure_ncurses --enable-widec --without-progs
			test -z "$CXX_FOR_TARGET" || make -C c++ etip.h || exit 1
			make %{?_smp_mflags} || exit $?
			make DESTDIR="%{buildroot}%{_rpmint_sysroot}" includesubdir=/ncursesw libdir=%{_rpmint_target_prefix}/lib/$multilibdir install.libs install.includes || exit $?
			# remove obsolete config script
			rm -f %{buildroot}%{_rpmint_bindir}/ncurses*-config
		done
	fi

}


mkdir -p "%{MINT_BUILD_DIR}"
mkdir -p "%{HOST_BUILD_DIR}"

build_ncurses


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
* Thu Mar 02 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
- updated to 6.0

* Thu Dec 14 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 5.1

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- correct Packager and Vendor
