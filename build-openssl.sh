#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=openssl
VERSION=-1.0.2l
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/openssl/openssl-1.0.2l-mint.patch
patches/openssl/openssl-zlib-static.patch
"

unpack_archive

cd "$MINT_BUILD_DIR"

SSLETCDIR=/etc/ssl

BINFILES="
${SSLETCDIR}
${TARGET_BINDIR}/c_rehash
${TARGET_BINDIR}/openssl
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man3/*
${TARGET_MANDIR#/}/man5/*
${TARGET_MANDIR#/}/man7/*
"


#
# CFLAGS have been patched in the Configure script
#
COMMON_CFLAGS="-O3 -fomit-frame-pointer"

CONFIGURE_FLAGS="--prefix=${prefix} --cross-compile-prefix=${TARGET}- --openssldir=${SSLETCDIR} zlib"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

"$srcdir/Configure" ${CONFIGURE_FLAGS} mint020
${MAKE} $JOBS || exit 1
${MAKE} MANDIR=${TARGET_MANDIR} INSTALL_PREFIX="${THISPKG_DIR}${sysroot}" install || exit 1
${MAKE} distclean
make_bin_archive 020

"$srcdir/Configure" ${CONFIGURE_FLAGS} mintv4e
${MAKE} $JOBS || exit 1
${MAKE} MANDIR=${TARGET_MANDIR} INSTALL_PREFIX="${THISPKG_DIR}${sysroot}" install || exit 1
${MAKE} distclean
make_bin_archive v4e

"$srcdir/Configure" ${CONFIGURE_FLAGS} mint
${MAKE} $JOBS || exit 1
${MAKE} MANDIR=${TARGET_MANDIR} INSTALL_PREFIX="${THISPKG_DIR}${sysroot}" install || exit 1
#${MAKE} distclean
make_bin_archive 000

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
