#!/bin/sh

me="$0"

PACKAGENAME=mintbin
VERSION=-0.3
VERSIONPATCH=20171006

TARGET=${1:-m68k-atari-mint}
export CROSS_TOOL=${TARGET}

ARCHIVES_DIR=$HOME/packages
PKG_DIR=`pwd`/binary7-package
DIST_DIR=`pwd`/pkgs

#
# The prefix where the executables should
# be installed later. If installed properly,
# this actually does not matter much, since
# all relevant directories are looked up
# relative to the executable
#
case `uname -s` in
	MINGW64*) host=mingw64; MINGW_PREFIX=/mingw64; ;;
	MINGW32*) host=mingw32; MINGW_PREFIX=/mingw32; ;;
	MINGW*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	MSYS*) host=msys ;;
	CYGWIN*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi ;;
	*) host=linux ;;
esac
case `uname -s` in
	MINGW*) prefix=${MINGW_PREFIX} ;;
	*) prefix=/usr ;;
esac
sysroot=${prefix}/${TARGET}/sys-root

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

ranlib=`which ${TARGET}-${ranlib} 2>/dev/null`
strip=`which "${TARGET}-strip"`
gcc=`which "${TARGET}-gcc"`

if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$gcc" -o ! -x "$strip"; then
	echo "cross tools for ${TARGET} not found" >&2
	exit 1
fi

cd "$MINT_BUILD_DIR"

THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"

./configure --prefix=${prefix} --disable-nls --target=$TARGET
make $JOBS || exit 1

rm -rf "${THISPKG_DIR}"

cd "$MINT_BUILD_DIR"
make DESTDIR="${THISPKG_DIR}" install || exit 1

cd "${THISPKG_DIR}/${prefix}/bin" || exit 1
strip -p *

cd "${THISPKG_DIR}/${prefix}/${TARGET}/bin" || exit 1
strip -p *

for i in arconv cnm csize cstrip flags mintbin stack symex; do
	if test -x ../../bin/${TARGET}-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/${TARGET}-$i; then
		rm -f ${i} ${i}${EXEEXT}
		$LN_S ../../bin/${TARGET}-$i${EXEEXT} $i
	fi
done
	
cd "${THISPKG_DIR}"
rm -f ${prefix#/}/share/info/dir
for f in ${prefix#/}/share/info/*; do
	case $f in
	*.gz) ;;
	*) rm -f ${f}.gz; gzip -9 $f ;;
	esac
done

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}-${VERSIONPATCH}

tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${TARNAME}-bin-${host}.tar.xz .

cd "${BUILD_DIR}"
#rm -rf "${THISPKG_DIR}"
rm -rf "${srcdir}"

test -z "${PATCHES}" || tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint-${VERSIONPATCH}.tar.xz ${PATCHES}
cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}-${VERSIONPATCH}.sh
