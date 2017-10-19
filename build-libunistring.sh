#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libunistring
VERSION=-0.9.7
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/libunistring/mintelf-config.patch"

BINFILES=""

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --docdir=${TARGET_PREFIX}/share/doc/${PACKAGENAME} \
	--disable-shared \
	--enable-static \
	--disable-rpath \
	--config-cache \
"

create_config_cache()
{
cat <<EOF >config.cache
EOF
	append_gnulib_cache
}

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags
	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
