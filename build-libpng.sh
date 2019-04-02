#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libpng
VERSION=-1.6.34
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/libpng/mintelf-config.patch
patches/libpng/libpng-1.6.34-0001-config.patch
"

unpack_archive

cd "$srcdir"

autoreconf -fiv
# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/mintelf-config.patch"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

sed -i 's/^option CONSOLE_IO.*/\0 disabled/' scripts/pnglibconf.dfa

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared --config-cache --without-binconfigs --disable-shared ${CONFIGURE_FLAGS_AMIGAOS}"

create_config_cache()
{
cat <<EOF >config.cache
EOF
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
