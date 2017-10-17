#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libpng
VERSION=-1.6.34
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/libpng/mintelf-config.patch"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

sed -i 's/^option CONSOLE_IO.*/\0 disabled/' scripts/pnglibconf.dfa

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared --config-cache --without-binconfigs"

create_config_cache()
{
cat <<EOF >config.cache
EOF
}

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache
CFLAGS="-m68020-60 $COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m68020-60'
hack_lto_cflags
${MAKE} $JOBS || exit 1
${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
${MAKE} distclean

create_config_cache
CFLAGS="-mcpu=5475 $COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m5475'
hack_lto_cflags
${MAKE} $JOBS || exit 1
${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
${MAKE} distclean

create_config_cache
CFLAGS="$COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS}
hack_lto_cflags
${MAKE} $JOBS || exit 1
${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
#${MAKE} distclean

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
