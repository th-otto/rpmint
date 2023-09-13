#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=openssl
VERSION=-1.1.1p
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/openssl/openssl-1.1.1p-mint.patch
patches/openssl/openssl-zlib-static.patch
patches/openssl/openssl-bn_div-asm.patch
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
COMMON_CFLAGS="-O3 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--prefix=${prefix} --cross-compile-prefix=${TARGET}- --openssldir=${SSLETCDIR} zlib"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

targetconf_000=mint
targetconf_020=mint020
targetconf_v4e=mintv4e

for CPU in ${ALL_CPUS}; do
	eval targetconf=\${targetconf_$CPU}
	"$srcdir/Configure" ${CONFIGURE_FLAGS} $targetconf
	${MAKE} $JOBS || exit 1
	${MAKE} MANDIR=${TARGET_MANDIR} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
