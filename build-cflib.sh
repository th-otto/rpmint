#!/bin/sh

me="$0"

PACKAGENAME=cflib
VERSION=-21
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
MINT_BUILD_DIR="$srcdir/cflib"

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

# this Makefiles are not yet ready for parallel makes
JOBS=-j1

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

cd "$srcdir"
case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
		sed -i "\@^DEFINITIONS =@i OPTS += -flto" CONFIGVARS
		;;
esac

#
# ugly hack until makefiles have been ajusted
#
cd "$srcdir"
sed -i "\@^DEFINITIONS =@i PREFIX := ${THISPKG_DIR}/usr" CONFIGVARS

cd "$MINT_BUILD_DIR"

THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"

make $JOBS || exit 1

rm -rf "${THISPKG_DIR}"

cd "$MINT_BUILD_DIR"
mkdir -p ${THISPKG_DIR}/usr/include
mkdir -p ${THISPKG_DIR}/usr/lib
mkdir -p ${THISPKG_DIR}/usr/lib/mshort
mkdir -p ${THISPKG_DIR}/usr/lib/m68020-60
mkdir -p ${THISPKG_DIR}/usr/lib/m68020-60/mshort
mkdir -p ${THISPKG_DIR}/usr/lib/m5475
mkdir -p ${THISPKG_DIR}/usr/lib/m5475/mshort
mkdir -p ${THISPKG_DIR}/usr/stguide
make PREFIX=${THISPKG_DIR}/usr install || exit 1

cd "${THISPKG_DIR}/usr" || exit 1

find . -name "*.a" ! -type l -exec "${strip}" -S -x '{}' \;
find . -name "*.a" ! -type l -exec "${ranlib}" '{}' \;

cd "${THISPKG_DIR}"

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}-${VERSIONPATCH}

tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${TARNAME}-bin.tar.xz .

cd "${BUILD_DIR}"
#rm -rf "${THISPKG_DIR}"
rm -rf "${srcdir}"

test -z "${PATCHES}" || tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint-${VERSIONPATCH}.tar.xz ${PATCHES}
cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}-${VERSIONPATCH}.sh
