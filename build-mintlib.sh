#!/bin/sh

me="$0"

PACKAGENAME=mintlib
VERSION=-0.60.1
VERSIONPATCH=20171006

TARGET=${1:-m68k-atari-mint}
export CROSS_TOOL=${TARGET}

case `uname -s` in
	MINGW*) PREFIX=/mingw ;;
	*) PREFIX=/usr ;;
esac
sysroot=${PREFIX}/${TARGET}/sys-root

ARCHIVES_DIR=$HOME/packages
PKG_DIR=`pwd`/binary7-package
DIST_DIR=`pwd`/pkgs

srcdir=`pwd`/"${PACKAGENAME}${VERSION}"
BUILD_DIR=`pwd`
MINT_BUILD_DIR="$srcdir"

PATCHES="\
"
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
	         "${PACKAGENAME}${VERSION}.tar.xz" \
	         "${PACKAGENAME}${VERSION}.tar.bz2"; do
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

ranlib=`which ${ranlib} 2>/dev/null`
strip=`which "${TARGET}-strip"`
gcc=`which "${TARGET}-gcc"`

if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$gcc" -o ! -x "$strip"; then
	echo "cross tools for ${TARGET} not found" >&2
	exit 1
fi

cd "$MINT_BUILD_DIR"

THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"

#
# ugly hack until makefiles have been ajusted
#
sed -i "\@^# This is where include@i prefix := ${THISPKG_DIR}${sysroot}/usr" configvars
make $JOBS || exit 1

rm -rf "${THISPKG_DIR}"

cd "$MINT_BUILD_DIR"
make prefix=${THISPKG_DIR}${sysroot}/usr install || exit 1

cd "${THISPKG_DIR}${sysroot}/usr" || exit 1
gzip -9 share/man/man*/*

find . -name 00README | xargs rm -f
find . -name COPYING | xargs rm -f
find . -name COPYING.LIB | xargs rm -f
find . -name COPYMINT | xargs rm -f
find . -name BINFILES | xargs rm -f
find . -name MISCFILES | xargs rm -f
find . -name SRCFILES | xargs rm -f
find . -name EXTRAFILES | xargs rm -f
find . -name Makefile | xargs rm -f
find . -name clean-include | xargs rm -f

find . -name "*.a" -exec "${strip}" -S -x '{}' \;
find . -name "*.a" -exec "${ranlib}" '{}' \;

cd "${THISPKG_DIR}"

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}-${VERSIONPATCH}

tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${TARNAME}-bin.tar.xz usr

cd "${BUILD_DIR}"
#rm -rf "${THISPKG_DIR}"
rm -rf "${srcdir}"

test -z "${PATCHES}" || tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint-${VERSIONPATCH}.tar.xz ${PATCHES}
cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}-${VERSIONPATCH}.sh
