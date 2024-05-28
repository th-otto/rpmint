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

CONFIGURE_FLAGS="--prefix=${prefix} --cross-compile-prefix=${TARGET}- --openssldir=${SSLETCDIR} ${ELF_CFLAGS} zlib"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

targetconf_000=mint
targetconf_020=mint020
targetconf_v4e=mintv4e

for CPU in ${ALL_CPUS}; do
	eval targetconf=\${targetconf_$CPU}
	"$srcdir/Configure" ${CONFIGURE_FLAGS} $targetconf
	${MAKE} $JOBS V=1 || exit 1
	${MAKE} MANDIR=${TARGET_MANDIR} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	# if the library for coldfire/m68020 ended up in the toplevel directory, something went wrong
	if test "${CPU}" != 000 -a -f "${THISPKG_DIR}${sysroot}/${TARGET_LIBDIR}/libssl.a"; then
		echo "libssl.a installed to wrong directory" >&2
		exit 1
	fi
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
