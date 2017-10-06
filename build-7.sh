#!/bin/sh

PACKAGENAME=gcc
VERSION=-7.2
VERSIONPATCH=20171004
REVISION="MiNT $VERSIONPATCH"

TARGET=m68k-atari-linux
TARGET=m68k-atari-mint
PREFIX=/usr

ARCHIVES_DIR=`pwd`
BUILD_DIR=`pwd`
MINT_BUILD_DIR="$BUILD_DIR/linux-build"
MINT_BUILD_DIR="$BUILD_DIR/mint7-build"
PKG_DIR=`pwd`/linux-package
PKG_DIR=`pwd`/binary7-package

srcdir="$HOME/m68k-atari-mint-gcc"

if test ! -d "$srcdir"; then
	echo "$srcdir: no such directory" >&2
	exit 1
fi
if test ! -f "${PREFIX}/${TARGET}/sys-root/usr/include/compiler.h"; then
	echo "mintlib headers must be installed in ${PREFIX}/${TARGET}/sys-root/usr/include" >&2
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

BASE_VER=$(cat $srcdir/gcc/BASE-VER)
gcc_dir_version=$(echo $BASE_VER | cut -d '.' -f 1)

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
#
BUILD=$(/usr/share/automake/config.guess 2>/dev/null)
test "$BUILD" = "" && BUILD=$($srcdir/config.guess)

rm -rf "$MINT_BUILD_DIR"
mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
CFLAGS_FOR_TARGET="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD=""
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"
CXXFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"
LDFLAGS_FOR_TARGET=

enable_lto=--disable-lto
enable_plugin=--disable-plugin
languages=c,c++
ranlib=ranlib
case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
    	enable_lto=--enable-lto
    	enable_plugin=--enable-plugin
    	languages="$languages,lto"
    	ranlib=gcc-ranlib
		;;
esac
EXEEXT=
case `uname -s` in
	CYGWIN* | MINGW*) EXEEXT=.exe ;;
esac

$srcdir/configure \
	--target="${TARGET}" --build="$BUILD" \
	--prefix="${PREFIX}" \
	--libdir="$BUILD_LIBDIR" \
	--bindir="${PREFIX}/bin" \
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
	--with-gxx-include-dir=${PREFIX}/${TARGET}/sys-root/usr/include/c++/${gcc_dir_version} \
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
	--with-libiconv-prefix="${PREFIX}" \
	--with-libintl-prefix="${PREFIX}" \
	--with-sysroot="${PREFIX}/${TARGET}/sys-root" \
	--enable-languages="$languages"

make $JOBS all-gcc || exit 1
make $JOBS all-target-libgcc || exit 1
make $JOBS || exit 1
make DESTDIR="$PKG_DIR" install || exit 1

mkdir -p "$PKG_DIR/usr/${TARGET}/bin"

cd "$PKG_DIR/usr/${TARGET}/bin"

for i in addr2line ar arconv as c++ nm cpp csize cstrip flags g++ gcc gcov gfortran ld ld.bfd mintbin nm objcopy objdump ranlib stack strip symex readelf; do
	if test -x ../../bin/${TARGET}-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/${TARGET}-$i; then
		rm -f $i
		ln -s ../../bin/${TARGET}-$i $i
	fi
done

cd "$PKG_DIR/usr/bin"

if test -x ${TARGET}-c++ && test -x ${TARGET}-g++ && test ! -h ${TARGET}-c++; then
	rm -f ${TARGET}-c++${EXEEXT} ${TARGET}-c++
	ln -s ${TARGET}-g++${EXEEXT} ${TARGET}-c++
fi
if test -x ${TARGET}-g++ && test ! -x ${TARGET}-g++; then
	rm -f ${TARGET}-g++-${BASE_VER}${EXEEXT} ${TARGET}-g++-${BASE_VER}
	mv ${TARGET}-g++${EXEEXT} ${TARGET}-g++-${BASE_VER}${EXEEXT}
	ln -s ${TARGET}-g++-${BASE_VER}${EXEEXT} ${TARGET}-g++
fi
if test -x ${TARGET}-gcc && test ! -h ${TARGET}-gcc; then
	rm -f ${TARGET}-gcc-${BASE_VER}${EXEEXT} ${TARGET}-gcc-${BASE_VER}
	mv ${TARGET}-gcc${EXEEXT} ${TARGET}-gcc-${BASE_VER}${EXEEXT}
	ln -s ${TARGET}-gcc-${BASE_VER}${EXEEXT} ${TARGET}-gcc
fi
if test -x ${TARGET}-cpp && test ! -h ${TARGET}-cpp; then
	rm -f ${TARGET}-cpp-${BASE_VER}${EXEEXT} ${TARGET}-cpp-${BASE_VER}
	mv ${TARGET}-cpp${EXEEXT} ${TARGET}-cpp-${BASE_VER}${EXEEXT}
	ln -s ${TARGET}-cpp-${BASE_VER}${EXEEXT} ${TARGET}-cpp
fi

cd "$PKG_DIR"

TARNAME=$PACKAGENAME$VERSION-mint-$VERSIONPATCH

gzip -9 ${PREFIX#/}/share/man/*/*
rm -f ${PREFIX#/}/share/info/dir
gzip -9 ${PREFIX#/}/share/info/*
tar --owner=0 --group=0 -jcvf $TARNAME-doc.tar.bz2 ${PREFIX#/}/share/info ${PREFIX#/}/share/man
rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man

strip -p ${PREFIX#/}/bin/*
rm -f ${BUILD_LIBDIR#/}/libiberty.a
rm -f ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/*.la
rm -f ${PREFIX#/}/lib/${TARGET}/lib/*.la ${PREFIX#/}/lib/${TARGET}/lib/*/*.la
strip -p ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/{cc1,cc1plus,cc1obj,cc1objplus,f951,collect2,liblto_plugin.so.*,lto-wrapper,lto1}
strip -p ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/plugin/gengtype
strip -p ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/install-tools/fixincl

if test -f ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/liblto_plugin.so.0.0.0; then
	mkdir -p ${PREFIX#/}/lib/bfd-plugins
	rm -f ${PREFIX#/}/lib/bfd-plugins/liblto_plugin.so.0.0.0
	ln -s ../../${BUILD_LIBDIR##*/}/gcc/${TARGET}/${gcc_dir_version}/liblto_plugin.so.0.0.0 ${PREFIX#/}/lib/bfd-plugins/liblto_plugin.so.0.0.0
fi

find ${PREFIX#/}/${TARGET} -name "*.a" -exec "$PKG_DIR/usr/bin/${TARGET}-${ranlib}" '{}' \;
find ${BUILD_LIBDIR#/}/gcc/${TARGET} -name "*.a" -exec "$PKG_DIR/usr/bin/${TARGET}-${ranlib}" '{}' \;

cd ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/include-fixed && {
	for i in `find . -type f`; do
		case $i in
		./README | ./limits.h | ./syslimits.h) ;;
		*) echo "removing fixed include file $i"; rm -f $i ;;
		esac
	done
	for i in `find . -depth -type d`; do
		test "$i" = "." || rmdir "$i"
	done
}

cd "$PKG_DIR"

# tar --owner=0 --group=0 -jcvf $TARNAME.tar.bz2 ${PREFIX#/}
