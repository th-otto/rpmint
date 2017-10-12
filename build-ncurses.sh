#!/bin/sh

me="$0"

PACKAGENAME=ncurses
VERSION=-6.0
#VERSIONPATCH=-20171006
VERSIONPATCH=

TARGET=${1:-m68k-atari-mint}
export CROSS_TOOL=${TARGET}
prefix=/usr
sysroot=${prefix}/${TARGET}/sys-root

TARGET_PREFIX=/usr
TARGET_LIBDIR="${TARGET_PREFIX}/lib"
TARGET_BINDIR="${TARGET_PREFIX}/bin"

ARCHIVES_DIR=$HOME/packages
here=`pwd`
PKG_DIR="$here/binary7-package"
DIST_DIR="$here/pkgs"

srcdir="$here/${PACKAGENAME}${VERSION}"
BUILD_DIR="$here"
MINT_BUILD_DIR="$srcdir/build-target"
HOST_BUILD_DIR="$srcdir/build-host"

PATCHES="patches/ncurses/ncurses-6.0.dif \
patches/ncurses/ncurses-5.9-ibm327x.dif \
patches/ncurses/ncurses-6.0-0003-overwrite.patch \
patches/ncurses/ncurses-6.0-0005-environment.patch \
patches/ncurses/ncurses-6.0-0010-source.patch \
patches/ncurses/ncurses-6.0-0011-termcap.patch \
patches/ncurses/ncurses-6.0-0020-configure.patch \
patches/ncurses/ncurses-6.0-0021-mintelf-config.patch \
patches/ncurses/ncurses-6.0-0022-dynamic.patch \
"
PATCHARCHIVE=patches/ncurses/ncurses-6.0-patches.tar.bz2

BUILD_EXEEXT=
TARGET_EXEEXT=
LN_S="ln -s"
case `uname -s` in
	CYGWIN* | MINGW* | MSYS*) BUILD_EXEEXT=.exe ;;
esac
case `uname -s` in
	MINGW* | MSYS*) LN_S="cp -p" ;;
esac
case $TARGET in
 	*-*-cygwin* | *-*-mingw* | *-*-msys*) TARGET_EXEEXT=.exe ;;
esac


rm -rf "$srcdir"
if :; then
	missing=true
	for f in "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.xz" \
	         "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.bz2" \
	         "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.gz" \
	         "${PACKAGENAME}${VERSION}.tar.xz" \
	         "${PACKAGENAME}${VERSION}.tar.bz2" \
	         "${PACKAGENAME}${VERSION}.tar.gz"; do
		if test -f "$f"; then missing=false; tar xvf "$f" || exit 1; fi
	done
	if $missing; then
		echo "${PACKAGENAME}${VERSION}.*: no such file" >&2
		exit 1
	fi
	if test ! -d "$srcdir"; then
		echo "$srcdir: no such directory" >&2
		exit 1
	fi
	mkdir -p "$BUILD_DIR/ncurses-patches"
	tar -C "$BUILD_DIR/ncurses-patches" --strip-components=1 -xjf ${PATCHARCHIVE}
	cd "$srcdir"
	for patch in $BUILD_DIR/ncurses-patches/ncurses*.patch
	do
	    patch -f -T -p1 -s < $patch
	done
	cd "$BUILD_DIR"
	rm -rf "$BUILD_DIR/ncurses-patches"
	
	for f in $PATCHES; do
	  if test -f "$f"; then
	    cd "$srcdir" && patch -p1 < "$BUILD_DIR/$f" || exit 1
	  else
	    echo "missing patch $f" >&2
	    exit 1
	  fi
	  cd "$BUILD_DIR"
	done
fi

if test ! -d "$srcdir"; then
	echo "$srcdir: no such directory" >&2
	exit 1
fi

JOBS=`rpm --eval '%{?jobs:%jobs}' 2>/dev/null`
P=$(getconf _NPROCESSORS_CONF 2>/dev/null || nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null)
if test -z "$P"; then P=$NUMBER_OF_PROCESSORS; fi
if test -z "$P"; then P=1; fi
if test -z "$JOBS"; then
  JOBS=$P
else
  test 1 -gt "$JOBS" && JOBS=1
fi
JOBS=-j$JOBS

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
#
BUILD=`/usr/share/automake/config.guess 2>/dev/null`
test "$BUILD" = "" && BUILD=`$srcdir/config.guess`

ranlib=ranlib
case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
    	ranlib=gcc-ranlib
		;;
esac

ranlib=`which ${ranlib} 2>/dev/null`
strip=`which "${TARGET}-strip"`
gcc=`which "${TARGET}-gcc"`
cxx=`which "${TARGET}-g++"`
MAKE=make

if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$gcc" -o ! -x "$strip"; then
	echo "cross tools for ${TARGET} not found" >&2
	exit 1
fi

THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -pipe -D_REENTRANT -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
LTO_CFLAGS=
case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
		# we cannot add this to CFLAGS, because then autoconf tests
		# for missing c library functions will always succeed
		LTO_CFLAGS="-flto"
		;;
esac

CC_FOR_BUILD=gcc
CXX_FOR_BUILD=g++

CC_FOR_TARGET="$gcc"
CXX_FOR_TARGET="$cxx"

ENABLE_SHARED_TARGET=no

TARGET_CONFIGURE_ARGS="--prefix=${sysroot}${TARGET_PREFIX} --host=${TARGET}"
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
		*-os2-emx*|*-msdosdjgpp*|*-cygwin*|*-msys*|*-mingw*|*-uwin*|*-atari-mint*)
			mixedcase=--enable-mixed-case=no
			;;
	esac
	export CC CXX CFLAGS CXXFLAGS LDFLAGS TERM GZIP PATH TMPDIR

	cd "$HOST_BUILD_DIR" || exit 1
    if true
    then
    	test -f Makefile && $MAKE clean
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
    	test -f Makefile && $MAKE clean
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
	        --with-pkg-config-libdir="${sysroot}${TARGET_LIBDIR}/pkgconfig" \
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
        sed -i 's/^s,@CFLAGS@,\(.*\)$/s,@CFLAGS@,'"$LTO_CFLAGS"' \1/
s/^s,@CXXFLAGS@,\(.*\)$/s,@CXXFLAGS@,'"$LTO_CFLAGS"' \1/' config.status
			./config.status
    fi
}


copy_pkg_configs()
{
	local pattern="${1:-*.pc}"
	local build_prefix="$prefix/$TARGET"
	local i base dst
	
	mkdir -p ./$build_prefix/lib/pkgconfig
	
	#
	# replace absolute pathnames by their symbolic equivalents
	# and remove unneeded -I and -L switches,
	# since those directories are always on the
	# default search path.
	# remove -L${sharedlibdir}, because
	# sharedlibdir is the bin directory, but the import libraries
	# are in the lib directory
	#
	for i in .${sysroot}$TARGET_LIBDIR/pkgconfig/$pattern; do
		test -e "$i" || continue
		true && {
			# from the *.pc files generated for the target,
			# generate *.pc files that are suitable for the cross-compiler
			base=${i##*/}
			dst=./$build_prefix/lib/pkgconfig/$base
			if test ! -f $dst -o $i -nt $dst; then
				cp -a $i $dst
				test -h "$i" && continue
				sed -i 's,",,g
						 s,prefix[ ]*=[ ]*'${sysroot}${TARGET_PREFIX}',prefix='${sysroot}${TARGET_PREFIX}',
			             /^prefix[ ]*=/{p;d}
			             s,=[ ]*'$prefix',=${prefix},
			             s,-L'$TARGET_LIBDIR',-L${libdir},g
			             s,-L${sharedlibdir} ,,g
			             s,-L${libdir} ,,g
			             s,-L${libdir}$,,
			             s,-L'${TARGET_BINDIR}'[ ]*,,g
			             s,-I/usr/include,-I${includedir},g
			             s,-I'${sysroot}${TARGET_PREFIX}/include',-I${includedir},g
			             s,-I${includedir} ,,g
			             s,-I${includedir}$,,' $dst
			fi
		}
		true && {
			sed -e 's,",,g
					 s,prefix[ ]*=[ ]*'${sysroot}${TARGET_PREFIX}',prefix='${TARGET_PREFIX}',
			         /^prefix[ ]*=/{p;d}
			         s,[ ]*=[ ]*'$prefix',=${prefix},
			         s,-L'$TARGET_LIBDIR',-L${libdir},g
		             s,-L${sharedlibdir} ,,g
			         s,-L${libdir} ,,g
			         s,-L${libdir}$,,
		             s,-L'${TARGET_BINDIR}'[ ]*,,g
 		             s,-I/usr/include,-I${includedir},g
		             s,-I'${sysroot}${TARGET_PREFIX}/include',-I${includedir},g
				     s,-I${includedir} ,,g
				     s,-I${includedir}$,,' $i > $i.tmp
			diff -q $i $i.tmp >/dev/null && rm -f $i.tmp || {
				echo "fixed $i"
				mv $i.tmp $i
			}
		}
	done
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
    	$MAKE $JOBS -C include &&
    	$MAKE $JOBS -C ncurses fallback.c FALLBACK_LIST="" &&
    	$MAKE $JOBS -C progs termsort.c &&
    	$MAKE $JOBS -C progs transform.h &&
    	$MAKE $JOBS -C progs infocmp$BUILD_EXEEXT &&
    	$MAKE $JOBS -C progs tic$BUILD_EXEEXT \
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
    LDFLAGS=""
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
		*-os2-emx*|*-msdosdjgpp*|*-cygwin*|*-msys*|*-mingw*|*-uwin*|*-atari-mint*)
			mixedcase=--enable-mixed-case=no
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
	
    CPU_CFLAGS=-m68000
    configure_ncurses
    test -z "$CXX_FOR_TARGET" || $MAKE -C c++ etip.h || exit 1
    $MAKE $JOBS || exit $?
    $MAKE DESTDIR="${THISPKG_DIR}" install includesubdir=/ncurses || exit $?
    ( cd "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include"; $LN_S -f ncurses/{curses,ncurses,term,termcap}.h . )
    
	# the install process sometimes erroneously installs the host exes with a target prefix
    if :; then
    	(cd ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/bin
    		for i in clear infocmp tabs tic toe tput tset; do
    			if test -x ${TARGET}-${i}${TARGET_EXEEXT}; then
    				rm -f ${i}${TARGET_EXEEXT}
    				mv ${TARGET}-${i}${TARGET_EXEEXT} ${i}${TARGET_EXEEXT}
    			fi
    			$strip --strip-unneeded ${i}${TARGET_EXEEXT}
    		done
    		for i in captoinfo infotocap reset; do
    			rm -f ${TARGET}-${i}${TARGET_EXEEXT} ${i}${TARGET_EXEEXT}
    		done
    		$LN_S tic${TARGET_EXEEXT} captoinfo${TARGET_EXEEXT}
    		$LN_S tic${TARGET_EXEEXT} infotocap${TARGET_EXEEXT}
    		$LN_S tset${TARGET_EXEEXT} reset${TARGET_EXEEXT}
    	)
    fi

    CPU_CFLAGS=-m68020-60
    configure_ncurses --without-progs
    test -z "$CXX_FOR_TARGET" || $MAKE -C c++ etip.h || exit 1
    $MAKE $JOBS || exit $?
    $MAKE DESTDIR="${THISPKG_DIR}" libdir=${sysroot}${TARGET_LIBDIR}/m68020-60 install.libs || exit $?
    
    CPU_CFLAGS=-mcpu=5475
    configure_ncurses --without-progs
    test -z "$CXX_FOR_TARGET" || $MAKE -C c++ etip.h || exit 1
    $MAKE $JOBS || exit $?
    $MAKE DESTDIR="${THISPKG_DIR}" libdir=${sysroot}${TARGET_LIBDIR}/m5475 install.libs || exit $?
    
    # Now use --enable-widec for UTF8/wide character support.
    # The libs with 16 bit wide characters are binary incompatible
    # to the normal 8bit wide character libs.
    #
	# currently does not work because mintlib lacks the wcwidth function
	#
    if false; then
	    configure_ncurses --enable-widec --without-progs
	    test -z "$CXX_FOR_TARGET" || $MAKE -C c++ etip.h || exit 1
	    $MAKE $JOBS || exit $?
	    $MAKE DESTDIR="${THISPKG_DIR}" install.libs install.includes includesubdir=/ncursesw || exit $?

	    CPU_CFLAGS=-m68020-60
	    configure_ncurses --enable-widec --without-progs
	    test -z "$CXX_FOR_TARGET" || $MAKE -C c++ etip.h || exit 1
	    $MAKE $JOBS || exit $?
	    $MAKE DESTDIR="${THISPKG_DIR}" libdir=${sysroot}${TARGET_LIBDIR}/m68020-60 install.libs || exit $?
	
	    CPU_CFLAGS=-mcpu=5475
	    configure_ncurses --enable-widec --without-progs
	    test -z "$CXX_FOR_TARGET" || $MAKE -C c++ etip.h || exit 1
	    $MAKE $JOBS || exit $?
	    $MAKE DESTDIR="${THISPKG_DIR}" libdir=${sysroot}${TARGET_LIBDIR}/m5475 install.libs || exit $?
	fi
	
	cd "${THISPKG_DIR}"
    copy_pkg_configs "ncurses*.pc"
    copy_pkg_configs "form*.pc"
    copy_pkg_configs "menu*.pc"
    copy_pkg_configs "panel*.pc"
    
#   exec 0<&$safe_stdin
#    : {safe_stdin}<&-
    
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


mkdir -p "$MINT_BUILD_DIR"
mkdir -p "$HOST_BUILD_DIR"
cd "$MINT_BUILD_DIR"

rm -rf "${THISPKG_DIR}"
build_ncurses


cd "${THISPKG_DIR}${sysroot}" || exit 1

find . -name "*.a" ! -type l -exec "${strip}" -S -x '{}' \;
find . -name "*.a" ! -type l -exec "${ranlib}" '{}' \;

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}${VERSIONPATCH}

cd "${THISPKG_DIR}" || exit 1

tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${TARNAME}-bin.tar.xz usr

cd "${BUILD_DIR}"
#rm -rf "${THISPKG_DIR}"
rm -rf "${MINT_BUILD_DIR}"
rm -rf "${HOST_BUILD_DIR}"
rm -rf "${srcdir}"

test -z "${PATCHES}" || tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.tar.xz ${PATCHES} ${PATCHARCHIVE}
cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}${VERSIONPATCH}.sh
