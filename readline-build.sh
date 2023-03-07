#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=readline
VERSION=-7.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

DISABLED_PATCHES="patches/automake/mintelf-config.sub"

unpack_archive

cd "$srcdir"

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" support/config.sub

cd "$MINT_BUILD_DIR"


COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared --config-cache"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_func_strcoll_works=yes
bash_cv_func_strcoll_broken=no
bash_cv_must_reinstall_sighandlers=no
bash_cv_func_sigsetjmp=present
bash_cv_func_ctype_nonascii=no
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
