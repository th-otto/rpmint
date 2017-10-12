#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=SDL
VERSION=-1.2.15-hg
#VERSIONPATCH=-20171006
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/sdl/sdl-1.2.15-mintelf-config.patch \
patches/sdl/sdl-1.2.15-asm.patch"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-video-opengl --disable-threads"

CFLAGS="-m68020-60 $COMMON_CFLAGS" ${srcdir}/configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m68020-60'
hack_lto_cflags
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
make distclean

CFLAGS="-mcpu=5475 $COMMON_CFLAGS" ${srcdir}/configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m5475'
hack_lto_cflags
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
make distclean

CFLAGS="$COMMON_CFLAGS" ${srcdir}/configure ${CONFIGURE_FLAGS}
hack_lto_cflags
make $JOBS || exit 1
make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
#make distclean

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
