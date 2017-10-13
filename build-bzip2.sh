#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=bzip2
VERSION=-1.0.6
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/bzip2/bzip2-1.0.6-patch-0001-configure.patch \
patches/bzip2/bzip2-1.0.6-patch-0002-cygming.patch \
patches/bzip2/bzip2-1.0.6-patch-0003-debian-bzgrep.patch \
patches/bzip2/bzip2-1.0.6-patch-0004-unsafe-strcpy.patch \
patches/bzip2/bzip2-1.0.6-patch-0005-progress.patch \
patches/bzip2/bzip2-1.0.6-patch-0006-mint.patch \
"

unpack_archive

cd "$MINT_BUILD_DIR"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

CFLAGS="-m68020-60 $COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m68020-60'
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
make distclean
move_020_bins

CFLAGS="-mcpu=5475 $COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m5475'
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
make distclean
move_v4e_bins

CFLAGS="$COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS}
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
#make distclean

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
