#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zlib
VERSION=-1.2.11
VERSIONPATCH=-20171006

. ${scriptdir}/functions.sh

PATCHES="patches/zlib/zlib-1.2.11-pkgconfig.patch \
patches/zlib/zlib-1.2.11-0012-format.patch \
patches/zlib/zlib-1.2.11-0013-segfault.patch \
"

unpack_archive

cd "$MINT_BUILD_DIR"

export CHOST=$TARGET
COMMON_CFLAGS="-O3 -fomit-frame-pointer $LTO_CFLAGS"

CFLAGS="-m68020-60 $COMMON_CFLAGS" ./configure --prefix=${prefix} --libdir='${exec_prefix}/lib/m68020-60'
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install-libs || exit 1
make distclean

CFLAGS="-mcpu=5475 $COMMON_CFLAGS" ./configure --prefix=${prefix} --libdir='${exec_prefix}/lib/m5475'
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install-libs || exit 1
make distclean

CFLAGS="$COMMON_CFLAGS" ./configure --prefix=${prefix}
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
#make distclean

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
