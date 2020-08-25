#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libgcrypt
VERSION=-1.8.2
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES="
${TARGET_BINDIR#/}
${TARGET_PREFIX#/}/share/man/*
${TARGET_PREFIX#/}/share/info/*
"

PATCHES="
patches/libgcrypt/libgcrypt-ppc64.patch
patches/libgcrypt/libgcrypt-strict-aliasing.patch
patches/libgcrypt/libgcrypt-1.4.1-rijndael_no_strict_aliasing.patch
patches/libgcrypt/libgcrypt-sparcv9.diff
patches/libgcrypt/libgcrypt-unresolved-dladdr.patch
patches/libgcrypt/libgcrypt-1.5.0-LIBGCRYPT_FORCE_FIPS_MODE-env.diff
patches/libgcrypt/libgcrypt-1.6.1-use-fipscheck.patch
patches/libgcrypt/libgcrypt-1.6.1-fips-cavs.patch
patches/libgcrypt/libgcrypt-1.6.1-fips-cfgrandom.patch
patches/libgcrypt/libgcrypt-fix-rng.patch
patches/libgcrypt/libgcrypt-init-at-elf-load-fips.patch
patches/libgcrypt/libgcrypt-drbg_test.patch
patches/libgcrypt/libgcrypt-fips_run_selftest_at_constructor.patch
patches/libgcrypt/libgcrypt-1.6.3-aliasing.patch
patches/libgcrypt/libgcrypt-mint.patch
patches/libgcrypt/libgcrypt-mintelf-config.patch
"

unpack_archive

cd "$MINT_BUILD_DIR"

./autogen.sh

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--disable-shared \
	--disable-hmac-binary-check"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_BINDIR#/}/libgcrypt-config
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

# create pkg-config file
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig
cat > ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig/${PACKAGENAME}.pc <<-EOF
prefix=${TARGET_PREFIX}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: ${PACKAGENAME}
Description: The GNU Crypto Library
Version: ${VERSION#-}
URL: http://directory.fsf.org/wiki/Libgcrypt

Libs: -lgcrypt -lgpg-error
Cflags:
Requires: libgpg-error
EOF

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
