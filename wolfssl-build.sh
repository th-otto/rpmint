#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=wolfssl
VERSION=-5.5.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/wolfssl-5.5.0-mint.patch
patches/${PACKAGENAME}/single-thread.patch
"
DISABLED_PATCHES="
patches/${PACKAGENAME}/mintelf-config.patch
"
BINFILES="
"

unpack_archive

cd "$srcdir"

./autogen.sh
# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/mintelf-config.patch"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--enable-opensslextra \
	--enable-supportedcurves \
	--disable-jobserver \
	--enable-sp \
	--enable-ed25519 \
	--enable-des3 \
	--enable-ripemd \
	--enable-all-crypto \
	--enable-singlethreaded \
	--disable-asyncthreads \
	${CONFIGURE_FLAGS_AMIGAOS}"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CC="${TARGET}-gcc" \
	AR="${ar}" \
	RANLIB=${ranlib} \
	NM=${TARGET}-nm \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1

	# hack_lto_cflags
	${MAKE} V=1 $JOBS || exit 1
	${MAKE} prefix="${THISPKG_DIR}${sysroot}/usr" install || exit 1
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
