#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ncurses
VERSION=-6.0
#VERSIONPATCH=-20171006
VERSIONPATCH=

. ${scriptdir}/functions.sh

MINT_BUILD_DIR="$srcdir/build-target"
HOST_BUILD_DIR="$srcdir/build-host"

PATCHES="patches/ncurses/ncurses-6.0.dif
patches/ncurses/ncurses-5.9-ibm327x.dif
patches/ncurses/ncurses-6.0-0003-overwrite.patch
patches/ncurses/ncurses-6.0-0005-environment.patch
patches/ncurses/ncurses-6.0-0010-source.patch
patches/ncurses/ncurses-6.0-0011-termcap.patch
patches/ncurses/ncurses-6.0-0020-configure.patch
patches/ncurses/ncurses-6.0-0022-dynamic.patch
patches/ncurses/ncurses-no-include.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"
PATCHARCHIVE=patches/ncurses/ncurses-6.0-patches.tar.bz2

BINFILES="
${TARGET_BINDIR#/}/clear
${TARGET_BINDIR#/}/infocmp
${TARGET_BINDIR#/}/reset
${TARGET_BINDIR#/}/tabs
${TARGET_BINDIR#/}/toe
${TARGET_BINDIR#/}/tput
${TARGET_BINDIR#/}/tset
${TARGET_BINDIR#/}/tic
${TARGET_BINDIR#/}/captoinfo
${TARGET_BINDIR#/}/infotocap
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man3/*
${TARGET_MANDIR#/}/man5/*
${TARGET_MANDIR#/}/man7/*
${TARGET_PREFIX#/}/share/terminfo
${TARGET_PREFIX#/}/share/tabset
"

unpack_archive

COMMON_CFLAGS="-O2 -fomit-frame-pointer -pipe -D_REENTRANT -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"

export CROSS_TOOL=${TARGET}

CC_FOR_BUILD=gcc
CXX_FOR_BUILD=g++

CC_FOR_TARGET="$gcc"
CXX_FOR_TARGET="$cxx"

ENABLE_SHARED_TARGET=no

TARGET_CONFIGURE_ARGS="--prefix=${TARGET_PREFIX} --host=${TARGET}"
BUILD_CONFIGURE_ARGS="--prefix=/usr"

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

	cd "$HOST_BUILD_DIR" || exit 1
	if true
	then
		test -f Makefile && ${MAKE} clean
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
	cd "$MINT_BUILD_DIR"
	if true
	then
		test -f Makefile && ${MAKE} clean
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
			--with-pkg-config-libdir="${TARGET_LIBDIR}/pkgconfig" \
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
	local safe_stdin
	local screen="screen -L -D -m"
	local PATH="$PATH"
	local FALLBK="xterm,linux,vt100,vt102,cygwin"
	local GZIP="-9"
	local speed_t with_gpm dlsym shared without_cxx termcap disable_root mixedcase
	local abi
	local abi5_conf_args="--without-pthread --disable-reentrant --disable-ext-mouse --disable-widec --disable-ext-colors"
	local abi6_conf_args="--with-pthread    --enable-reentrant  --enable-ext-mouse  --enable-widec  --enable-ext-colors"
	local BUILD_TIC BUILD_INFOCMP
	
	NAME=${PACKAGENAME}${VERSION}
	abi=5

	if true; then
		withchtype=--with-chtype=long
		configure_ncurses_for_build
		${MAKE} $JOBS -C include &&
		${MAKE} $JOBS -C ncurses fallback.c FALLBACK_LIST="" &&
		${MAKE} $JOBS -C progs termsort.c &&
		${MAKE} $JOBS -C progs transform.h &&
		${MAKE} $JOBS -C progs infocmp$BUILD_EXEEXT &&
		${MAKE} $JOBS -C progs tic$BUILD_EXEEXT \
		|| exit $?
		BUILD_TIC=$HOST_BUILD_DIR/progs/tic$BUILD_EXEEXT
		BUILD_INFOCMP=$HOST_BUILD_DIR/progs/infocmp$BUILD_EXEEXT
		PATH="$HOST_BUILD_DIR/progs:$PATH"
	else
		BUILD_TIC=tic
		BUILD_INFOCMP=infocmp
	fi
	cd "$MINT_BUILD_DIR"
	
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

	cd "$MINT_BUILD_DIR"

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
	
#	: {safe_stdin}<&0
#	exec 0< /dev/null
	
	for CPU in ${ALL_CPUS}; do
		eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
		eval multilibdir=\${CPU_LIBDIR_$CPU}
		configure_ncurses
		pwd
		ls -l
		test -z "$CXX_FOR_TARGET" || ${MAKE} -C c++ etip.h || exit 1
		${MAKE} $JOBS || exit $?
		${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" includesubdir=/ncurses libdir=${TARGET_LIBDIR}/$multilibdir install || exit $?
		( cd "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include"; $LN_S -f ncurses/{curses,ncurses,term,termcap}.h . )
		# remove obsolete config script
		rm -f ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/ncurses*-config
		make_bin_archive $CPU
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
			test -z "$CXX_FOR_TARGET" || ${MAKE} -C c++ etip.h || exit 1
			${MAKE} $JOBS || exit $?
			${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" includesubdir=/ncursesw libdir=${TARGET_LIBDIR}/$multilibdir install.libs install.includes || exit $?
			# remove obsolete config script
			rm -f ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/ncurses*-config
		done
	fi
	
		
#   exec 0<&$safe_stdin
#	: {safe_stdin}<&-

}


cd "$srcdir"

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

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

mkdir -p "$MINT_BUILD_DIR"
mkdir -p "$HOST_BUILD_DIR"
cd "$MINT_BUILD_DIR"

build_ncurses

configured_prefix="${TARGET_PREFIX}"
copy_pkg_configs "ncurses*.pc"
copy_pkg_configs "form*.pc"
copy_pkg_configs "menu*.pc"
copy_pkg_configs "panel*.pc"

make_archives

rm -rf "${MINT_BUILD_DIR}"
rm -rf "${HOST_BUILD_DIR}"
