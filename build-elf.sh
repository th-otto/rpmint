#!/bin/sh

PACKAGENAME=gcc
VERSION=-7.2
VERSIONPATCH=20170919
REVISION="MiNT $VERSIONPATCH-elf"

TARGET=m68k-atari-mintelf
PREFIX=/usr

ARCHIVES_DIR=`pwd`
BUILD_DIR=`pwd`
MINT_BUILD_DIR="$BUILD_DIR/mint7-build"
PKG_DIR=`pwd`/binary7-package

srcdir="$HOME/m68k-atari-mint-gcc"

if test ! -d "$srcdir"; then
	echo "$srcdir: no such directory" >&2
	exit 1
fi
if test ! -f "$PREFIX/$TARGET/sys-root/usr/include/compiler.h"; then
	echo "mintlib headers must be installed in $PREFIX/$TARGET/sys-root/usr/include" >&2
	exit 1
fi

if test -d /usr/lib64; then
	BUILD_LIBDIR=${PREFIX}/lib64
else
	BUILD_LIBDIR=${PREFIX}/lib
fi

BASE_VER=$(cat $srcdir/gcc/BASE-VER)

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
#
BUILD=$(/usr/share/automake/config.guess 2>/dev/null)
test "$BUILD" = "" && BUILD=$($srcdir/config.guess)

mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
CFLAGS_FOR_TARGET="-O2 -fomit-frame-pointer -finhibit-size-directive"
LDFLAGS_FOR_BUILD=""
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"
CXXFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"
LDFLAGS_FOR_TARGET=

enable_lto=--disable-lto
enable_plugin=--disable-plugin
languages=c
ranlib=ranlib
case "$TARGET" in
    *-*-*elf* | *-*-linux*)
    	enable_lto=--enable-lto
    	enable_plugin=--enable-plugin
    	languages="$languages,lto"
    	ranlib=gcc-ranlib
		;;
esac

$srcdir/configure \
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
	--disable-werror \
	--with-gxx-include-dir=${PREFIX}/include/c++/${gcc_dir_version} \
	--with-default-libstdcxx-abi=gcc4-compatible \
	--with-gcc-major-version-only \
	--with-gcc --with-gnu-as --with-gnu-ld \
	--with-system-zlib \
	--disable-libgomp \
	--without-newlib \
	--disable-libstdcxx-pch \
	--disable-threads \
	$enable_lto \
	--enable-ssp \
	--enable-libssp \
	$enable_plugin \
	--enable-decimal-float \
	--disable-nls \
	--with-libiconv-prefix="$PREFIX" \
	--with-libintl-prefix="$PREFIX" \
	--with-sysroot="$PREFIX/$TARGET/sys-root" \
	--enable-languages="$languages"

make -j8 all-gcc || exit 1
make -j8 all-target-libgcc || exit 1
make -j8 || exit 1
make DESTDIR="$PKG_DIR" install || exit 1

mkdir -p "$PKG_DIR/usr/$TARGET/bin"

cd "$PKG_DIR/usr/$TARGET/bin"

for i in addr2line ar arconv as c++ nm cpp csize cstrip flags g++ gcc gcov gfortran ld ld.bfd mintbin nm objcopy objdump ranlib stack strip symex readelf; do
	if test -x ../../bin/$TARGET-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/$TARGET-$i; then
		rm -f $i
		ln -s ../../bin/$TARGET-$i $i
	fi
done

cd "$PKG_DIR/usr/bin"

if test -x $TARGET-c++ && test -x $TARGET-g++ && test ! -h $TARGET-c++; then
	rm -f $TARGET-c++
	ln -s $TARGET-g++ $TARGET-c++
fi
if test -x $TARGET-g++ && test ! -x $TARGET-g++; then
	rm -f $TARGET-g++-$BASE_VER
	mv $TARGET-g++ $TARGET-g++-$BASE_VER
	ln -s $TARGET-g++-$BASE_VER $TARGET-g++
fi
if test -x $TARGET-gcc && test ! -h $TARGET-gcc; then
	rm -f $TARGET-gcc-$BASE_VER
	mv $TARGET-gcc $TARGET-gcc-$BASE_VER
	ln -s $TARGET-gcc-$BASE_VER $TARGET-gcc
fi
if test -x $TARGET-cpp && test ! -h $TARGET-cpp; then
	rm -f $TARGET-cpp-$BASE_VER
	mv $TARGET-cpp $TARGET-cpp-$BASE_VER
	ln -s $TARGET-cpp-$BASE_VER $TARGET-cpp
fi

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
rm -f ${BUILD_LIBDIR#/}/gcc/$TARGET/*/*.la
rm -f ${PREFIX#/}/lib/$TARGET/lib/*.la ${PREFIX#/}/lib/$TARGET/lib/*/*.la
strip ${BUILD_LIBDIR#/}/gcc/$TARGET/*/{cc1,cc1plus,cc1obj,cc1objplus,f951,collect2,liblto_plugin.so.*,lto-wrapper,lto1}
strip ${BUILD_LIBDIR#/}/gcc/$TARGET/*/plugin/gengtype
strip ${BUILD_LIBDIR#/}/gcc/$TARGET/*/install-tools/fixincl

find ${PREFIX#/}/$TARGET -name "*.a" -exec "$PKG_DIR/usr/bin/${TARGET}-${ranlib}" {} \;
find ${BUILD_LIBDIR#/}/gcc/$TARGET -name "*.a" -exec "$PKG_DIR/usr/bin/${TARGET}-${ranlib}" {} \;

# tar --owner=0 --group=0 -jcvf $TARNAME.tar.bz2 ${PREFIX#/}
