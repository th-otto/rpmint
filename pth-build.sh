#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=pth
VERSION=-2.0.7
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/pth-2.0.7-m68k-atari-mint.patch
patches/${PACKAGENAME}/mintelf-config.patch
"
BINFILES="
"

unpack_archive

cd "$srcdir"

autoconf
# autoreconf -fiv
# autoreconf may have overwritten config.sub
# patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/mintelf-config.patch"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --enable-pthread --config-cache ${CONFIGURE_FLAGS_AMIGAOS}"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_check_stackgrowth=down
ac_cv_check_sjlj=sjljmint
ac_cv_check_mcsc=no
ac_cv_func_sigstack=no
ac_cv_func_sigaltstack=no
ac_cv_func_makecontext=no
EOF
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache

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
