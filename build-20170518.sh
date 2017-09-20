#!/bin/sh

PACKAGENAME=gcc
VERSION=-4.6.4
VERSIONPATCH=20170518
REVISION="MiNT $VERSIONPATCH"

TARGET=m68k-atari-mint
PREFIX=/usr

ARCHIVES_DIR=`pwd`
BUILD_DIR=`pwd`
MINT_BUILD_DIR="$BUILD_DIR/mint-build"
PKG_DIR=`pwd`/binary-package

srcdir="$PACKAGENAME$VERSION"

PATCH1="$PACKAGENAME$VERSION-mint-$VERSIONPATCH.patch"
PATCH2="$PACKAGENAME$VERSION-fastcall.patch"

if ! test -f ".patched-$PACKAGENAME$VERSION"; then
tar jxvf "$ARCHIVES_DIR/$PACKAGENAME$VERSION.tar.bz2" || exit 1
for f in "$PATCH1" "$PATCH2"; do
  if test -f "$f"; then
    cd "$srcdir" && patch -p1 < "$BUILD_DIR/$f"
  fi
  cd "$BUILD_DIR"
  touch ".patched-$PACKAGENAME$VERSION"
done
fi

if ! test -d "$srcdir"; then
	echo "$srcdir: no such directory" >&2
	exit 1
fi
if ! test -f "$PREFIX/$TARGET/sys-root/usr/include/compiler.h"; then
	echo "mintlib headers must be installed in $PREFIX/$TARGET/sys-root/usr/include" >&2
	exit 1
fi

if test -d /usr/lib64; then
	BUILD_LIBDIR=${PREFIX}/lib64
else
	BUILD_LIBDIR=${PREFIX}/lib
fi

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
#
BUILD=`/usr/share/automake/config.guess 2>/dev/null`
test "$BUILD" = "" && BUILD=`$srcdir/config.guess`

mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
CFLAGS_FOR_TARGET="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD=""
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"
CXXFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"
LDFLAGS_FOR_TARGET=

enable_lto=--disable-lto
case "$TARGET" in
    *-*-*elf* | *-*-linux*)
    	enable_lto=--enable-lto
		;;
esac

../$srcdir/configure \
	--target="$TARGET" --build="$BUILD" \
	--prefix="$PREFIX" \
	--libdir="$BUILD_LIBDIR" \
	--bindir="$PREFIX/bin" \
	--libexecdir='${libdir}' \
	CFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD" \
	CFLAGS="$CFLAGS_FOR_BUILD" \
	CXXFLAGS_FOR_BUILD="$CXXFLAGS_FOR_BUILD" \
	CXXFLAGS="$CXXFLAGS_FOR_BUILD" \
	BOOT_CFLAGS="$CFLAGS_FOR_BUILD" \
	CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET" \
	CXXFLAGS_FOR_TARGET="$CXXFLAGS_FOR_TARGET" \
	LDFLAGS_FOR_BUILD="$LDFLAGS_FOR_BUILD" \
	LDFLAGS="$LDFLAGS_FOR_BUILD" \
	--with-pkgversion="$REVISION" \
	--disable-libvtv \
	--disable-libmpx \
	--disable-libcc1 \
	--with-default-libstdcxx-abi=gcc4-compatible \
	--with-gcc --with-gnu-as --with-gnu-ld \
	--with-system-zlib \
	--disable-libgomp \
	--without-newlib \
	--disable-libstdcxx-pch \
	--disable-threads \
	$enable_lto \
	--enable-ssp \
	--enable-libssp \
	--disable-plugin \
	--enable-decimal-float \
	--disable-nls \
	--with-libiconv-prefix="$PREFIX" \
	--with-libintl-prefix="$PREFIX" \
	--with-sysroot="$PREFIX/$TARGET/sys-root" \
	--enable-languages=c,c++

make -j8 all-gcc || exit 1
make -j8 all-target-libgcc || exit 1
make -j8 || exit 1
make DESTDIR="$PKG_DIR" install || exit 1

mkdir -p "$PKG_DIR/usr/$TARGET/bin"

cd "$PKG_DIR/usr/$TARGET/bin"
for i in c++ cpp g++ gcc gcov gfortran; do
	test -h $i || ln -s ../../bin/$TARGET-$i $i
done
cd "$PKG_DIR"

TARNAME=$PACKAGENAME$VERSION-mint-$VERSIONPATCH

gzip -9 ${PREFIX#/}/share/man/*/*
rm -f ${PREFIX#/}/share/info/dir
gzip -9 ${PREFIX#/}/share/info/*
tar --owner=0 --group=0 -jcvf $TARNAME-doc.tar.bz2 ${PREFIX#/}/share/info ${PREFIX#/}/share/man
rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man

strip ${PREFIX#/}/bin/*
rm -f ${BUILD_LIBDIR#/}/libiberty.a
strip ${BUILD_LIBDIR#/}/gcc/$TARGET/*/*
strip ${BUILD_LIBDIR#/}/gcc/$TARGET/*/install-tools/*

tar --owner=0 --group=0 -jcvf $TARNAME.tar.bz2 ${PREFIX#/}
