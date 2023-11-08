#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libgcrypt
VERSION=-1.10.1
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES="
${TARGET_BINDIR#/}
${TARGET_PREFIX#/}/share/man/*
${TARGET_PREFIX#/}/share/info/*
"

PATCHES="
patches/libgcrypt/libgcrypt-1.10.0-allow_FSM_same_state.patch
patches/libgcrypt/libgcrypt-FIPS-SLI-pk.patch
patches/libgcrypt/libgcrypt-FIPS-SLI-hash-mac.patch
patches/libgcrypt/libgcrypt-FIPS-SLI-kdf-leylength.patch
patches/libgcrypt/libgcrypt-1.10.0-out-of-core-handler.patch
patches/libgcrypt/libgcrypt-jitterentropy-3.4.0.patch
patches/libgcrypt/libgcrypt-FIPS-rndjent_poll.patch
patches/libgcrypt/libgcrypt-1.10.0-use-fipscheck.patch
patches/libgcrypt/libgcrypt-mint.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

unpack_archive

cd "$MINT_BUILD_DIR"

./autogen.sh

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" build-aux/config.sub || exit 1

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

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
	: hack_lto_cflags
	echo "#undef HAVE_PTHREAD" >> config.h

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
