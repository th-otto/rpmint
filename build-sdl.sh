#!/bin/sh

me="$0"

PACKAGENAME=SDL
VERSION=-1.2.15-hg
#VERSIONPATCH=-20171006
VERSIONPATCH=

TARGET=${1:-m68k-atari-mint}
prefix=/usr
sysroot=${prefix}/${TARGET}/sys-root

ARCHIVES_DIR=$HOME/packages
PKG_DIR=`pwd`/binary7-package
DIST_DIR=`pwd`/pkgs

srcdir=`pwd`/"${PACKAGENAME}${VERSION}"
BUILD_DIR=`pwd`
MINT_BUILD_DIR="$srcdir"

PATCHES="patches/sdl/sdl-1.2.15-mintelf-config.patch \
patches/sdl/sdl-1.2.15-asm.patch"

EXEEXT=
LN_S="ln -s"
case `uname -s` in
	CYGWIN* | MINGW* | MSYS*) EXEEXT=.exe ;;
esac
case `uname -s` in
	MINGW* | MSYS*) LN_S="cp -p" ;;
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

ranlib=`which ${TARGET}-${ranlib} 2>/dev/null`
strip=`which "${TARGET}-strip"`
gcc=`which "${TARGET}-gcc"`

if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$gcc" -o ! -x "$strip"; then
	echo "cross tools for ${TARGET} not found" >&2
	exit 1
fi

cd "$MINT_BUILD_DIR"

THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
LTO_CFLAGS=
case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
		# we cannot add this to CFLAGS, because then autoconf tests
		# for missing c library functions will always succeed
		LTO_CFLAGS="-flto"
		;;
esac

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-video-opengl --disable-threads"

# FIXME: libtool kills it
hack_lto_cflags()
{
        sed -i 's/^S\["CFLAGS"\]="\([^"]*"\)$/S\["CFLAGS"\]="'"$LTO_CFLAGS"' \1"/
s/^S\["CXXFLAGS"\]="\([^"]*"\)$/S\["CXXFLAGS"\]="'"$LTO_CFLAGS"' \1"/' config.status
			./config.status
}

CFLAGS="$COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS}
hack_lto_cflags
make $JOBS || exit 1

rm -rf "${THISPKG_DIR}"

make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
make distclean

CFLAGS="-m68020-60 $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m68020-60'
hack_lto_cflags
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
make distclean

CFLAGS="-mcpu=5475 $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m5475'
hack_lto_cflags
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
#make distclean

cd "${THISPKG_DIR}${sysroot}/usr" || exit 1
gzip -9 share/man/man*/*

find . -name "*.la" -exec rm '{}' \;
find . -name "*.a" ! -type l -exec "${strip}" -S -x '{}' \;
find . -name "*.a" ! -type l -exec "${ranlib}" '{}' \;

rm -rf ${THISPKG_DIR}${sysroot}${prefix}/lib/*/pkgconfig

cd "${THISPKG_DIR}"

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}${VERSIONPATCH}

tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${TARNAME}-bin.tar.xz usr

cd "${BUILD_DIR}"
#rm -rf "${THISPKG_DIR}"
rm -rf "${srcdir}"

test -z "${PATCHES}" || tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.tar.xz ${PATCHES}
cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}${VERSIONPATCH}.sh
