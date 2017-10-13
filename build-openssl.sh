#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=openssl
VERSION=-1.0.2l
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/openssl/openssl-1.0.2l-mint.patch"

unpack_archive

cd "$MINT_BUILD_DIR"


#
# CFLAGS have been patched in the Configure script
#
COMMON_CFLAGS="-O3 -fomit-frame-pointer"

CONFIGURE_FLAGS="--prefix=${prefix} --cross-compile-prefix=${TARGET}- --openssldir=/etc zlib"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

"$srcdir/Configure" ${CONFIGURE_FLAGS} mint020
make $JOBS || exit 1
make INSTALL_PREFIX="${THISPKG_DIR}${sysroot}" install_sw || exit 1
make distclean
move_020_bins

"$srcdir/Configure" ${CONFIGURE_FLAGS} mintv4e
make $JOBS || exit 1
make INSTALL_PREFIX="${THISPKG_DIR}${sysroot}" install_sw || exit 1
make distclean
move_v4e_bins

"$srcdir/Configure" ${CONFIGURE_FLAGS} mint
make $JOBS || exit 1
make INSTALL_PREFIX="${THISPKG_DIR}${sysroot}" install_sw || exit 1
#make distclean

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
