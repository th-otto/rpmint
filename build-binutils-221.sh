#!/bin/sh

PACKAGENAME=binutils
VERSION=-2.21.1
VERSIONPATCH=-20170919
REVISION="GNU Binutils for MiNT ${VERSIONPATCH#-}"

TARGET=${1:-m68k-atari-mint}
PREFIX=/usr

ARCHIVES_DIR=$HOME/packages
BUILD_DIR=`pwd`
MINT_BUILD_DIR="$BUILD_DIR/mint7-build"
PKG_DIR=`pwd`/binary7-package

srcdir="$PACKAGENAME$VERSION"

PATCH1="$PACKAGENAME$VERSION-mint${VERSIONPATCH}.patch"

if test ! -d "$srcdir"; then
	echo "$srcdir: no such directory" >&2
	exit 1
fi

if test -d /usr/lib64; then
	BUILD_LIBDIR=${PREFIX}/lib64
else
	BUILD_LIBDIR=${PREFIX}/lib
fi
MAKE=${MAKE:-make}

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

# add opposite of default mingw32 target for binutils,
# and also host target
case "$TARGET" in
    x86_64-*-mingw32*)
	    bfd_targets="$bfd_targets,i686-pc-mingw32"
    	;;
    i686-*-mingw*)
    	bfd_targets="$bfd_targets,x86_64-w64-mingw64"
		;;
    *-*-*elf* | *-*-linux*)
    	enable_lto=--enable-lto
		enable_plugins=--enable-plugins
		;;
esac
case "$TARGET" in
    m68k-atari-mintelf*)
    	bfd_targets="$bfd_targets,m68k-atari-mint"
		;;
    m68k-atari-mint*)
    	bfd_targets="$bfd_targets,m68k-atari-mintelf"
		;;
esac

mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD="-s"
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"


../$srcdir/configure \
	--target="$TARGET" --build="$BUILD" \
	--prefix="$PREFIX" \
	--libdir="$BUILD_LIBDIR" \
	--bindir="$PREFIX/bin" \
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
	--with-sysroot="$PREFIX/$TARGET/sys-root"

${MAKE} -j8 || exit 1
${MAKE} DESTDIR="$PKG_DIR" install-strip || exit 1

mkdir -p "$PKG_DIR/usr/$TARGET/bin"

cd "$PKG_DIR/usr/$TARGET/bin"

for i in addr2line ar as nm ld ld.bfd objcopy objdump ranlib strip readelf dlltool dllwrap size strings; do
	if test -x ../../bin/$TARGET-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/$TARGET-$i; then
		rm -f $i
		ln -s ../../bin/$TARGET-$i $i
	fi
done

cd "$PKG_DIR/usr/bin"

rm -f $TARGET-ld
ln -s $TARGET-ld.bfd $TARGET-ld
cd "$PKG_DIR"

TARNAME=$PACKAGENAME$VERSION-mint${VERSIONPATCH}

rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man

strip -p ${PREFIX#/}/bin/*
rm -f ${BUILD_LIBDIR#/}/libiberty.a

# tar --owner=0 --group=0 -jcvf $TARNAME.tar.bz2 ${PREFIX#/}
