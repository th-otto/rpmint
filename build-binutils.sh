#!/bin/sh

PACKAGENAME=binutils
VERSION=-2.29.1
VERSIONPATCH=20171006
REVISION="GNU Binutils for MiNT $VERSIONPATCH"

TARGET=m68k-atari-mintelf
PREFIX=/usr

ARCHIVES_DIR=$HOME/packages
BUILD_DIR=`pwd`
MINT_BUILD_DIR="$BUILD_DIR/mint7-build"
PKG_DIR=`pwd`/binary7-package

srcdir="${PACKAGENAME}${VERSION}"

PATCHES="\
        ${PACKAGENAME}${VERSION}-0001-binutils-2.29.1-branch.patch \
        ${PACKAGENAME}${VERSION}-0005-x86-64-biarch.patch \
        ${PACKAGENAME}${VERSION}-0007-ld-dtags.patch \
        ${PACKAGENAME}${VERSION}-0008-ld-relro.patch \
        ${PACKAGENAME}${VERSION}-0011-use-hashtype-both-by-default.patch \
        ${PACKAGENAME}${VERSION}-0022-binutils-bfd_h.patch \
        ${PACKAGENAME}${VERSION}-0201-aout.patch \
        ${PACKAGENAME}${VERSION}-0202-ldfile.patch \
        ${PACKAGENAME}${VERSION}-0203-config-rpath.patch \
        ${PACKAGENAME}${VERSION}-mint-${VERSIONPATCH}.patch \
"
case "${TARGET}" in
m68k-atari-mintelf*)
	PATCHES="$PATCHES ${PACKAGENAME}${VERSION}-mintelf.patch"
	;;
esac

if test ! -f ".patched-${PACKAGENAME}${VERSION}"; then
	for f in "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.xz" \
	         "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.bz2" \
	         "${PACKAGENAME}${VERSION}.tar.xz" \
	         "${PACKAGENAME}${VERSION}.tar.bz2"; do
		if test -f "$f"; then tar xvf "$f" || exit 1; fi
	done
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
	touch ".patched-${PACKAGENAME}${VERSION}"
fi

if test ! -d "$srcdir"; then
	echo "$srcdir: no such directory" >&2
	exit 1
fi

if test -d /usr/lib64; then
	BUILD_LIBDIR=${PREFIX}/lib64
else
	BUILD_LIBDIR=${PREFIX}/lib
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

bfd_targets="--enable-targets=$BUILD"
enable_plugins=--disable-plugins
enable_lto=--disable-lto
ranlib=ranlib

# add opposite of default mingw32 target for binutils,
# and also host target
case "${TARGET}" in
    x86_64-*-mingw32*)
	    bfd_targets="$bfd_targets,i686-pc-mingw32"
    	;;
    i686-*-mingw*)
    	bfd_targets="$bfd_targets,x86_64-w64-mingw64"
		;;
    *-*-*elf* | *-*-linux*)
    	enable_lto=--enable-lto
		enable_plugins=--enable-plugins
    	ranlib=gcc-ranlib
		;;
esac
case "${TARGET}" in
    m68k-atari-mintelf*)
    	bfd_targets="$bfd_targets,m68k-atari-mint"
		;;
    m68k-atari-mint*)
    	bfd_targets="$bfd_targets,m68k-atari-mintelf"
		;;
esac

rm -rf "$MINT_BUILD_DIR"
mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD="-s"
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"


../$srcdir/configure \
	--target="${TARGET}" --build="$BUILD" \
	--prefix="${PREFIX}" \
	--libdir="$BUILD_LIBDIR" \
	--bindir="${PREFIX}/bin" \
	--libexecdir='${libdir}' \
	CFLAGS="$CFLAGS_FOR_BUILD" \
	CXXFLAGS="$CXXFLAGS_FOR_BUILD" \
	LDFLAGS="$LDFLAGS_FOR_BUILD" \
	$bfd_targets \
	--with-pkgversion="$REVISION" \
    --with-stage1-ldflags=-s \
    --with-boot-ldflags="$LDFLAGS_FOR_BUILD" \
	--with-gcc --with-gnu-as --with-gnu-ld \
    --disable-werror \
	--disable-threads \
	$enable_lto \
	$enable_plugins \
	--disable-nls \
	--with-sysroot="${PREFIX}/${TARGET}/sys-root"

make $JOBS || exit 1
make DESTDIR="$PKG_DIR" install-strip || exit 1

mkdir -p "$PKG_DIR/${PREFIX}/${TARGET}/bin"

cd "$PKG_DIR/${PREFIX}/${TARGET}/bin"

for i in addr2line ar arconv as c++ nm cpp csize cstrip flags g++ gcc gcov gfortran ld ld.bfd mintbin nm objcopy objdump ranlib stack strip symex readelf; do
	if test -x ../../bin/${TARGET}-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/${TARGET}-$i; then
		rm -f $i
		ln -s ../../bin/${TARGET}-$i $i
	fi
done

cd "$PKG_DIR/${PREFIX}/bin"

rm -f ${TARGET}-ld
ln -s ${TARGET}-ld.bfd ${TARGET}-ld
cd "$PKG_DIR"

TARNAME=${PACKAGENAME}${VERSION}-mint-${VERSIONPATCH}

rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man

strip -p ${PREFIX#/}/bin/*
rm -f ${BUILD_LIBDIR#/}/libiberty.a

# tar --owner=0 --group=0 -jcvf $TARNAME.tar.bz2 ${PREFIX#/}
