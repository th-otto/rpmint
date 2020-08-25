#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=fdlibm
VERSION=-20200108

. ${scriptdir}/functions.sh

PATCHES=""

unpack_archive

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

cd "$MINT_BUILD_DIR"
CFLAGS="$COMMON_CFLAGS" LDFLAGS="$COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS}
hack_lto_cflags
${MAKE} $JOBS || exit 1
${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
