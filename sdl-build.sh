#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=SDL
VERSION=-1.2.15-hg
#VERSIONPATCH=-20171006
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/sdl/sdl-1.2.15-mintelf-config.patch \
patches/sdl/sdl-1.2.15-asm.patch
patches/sdl/sdl-1.2.15-c99.patch
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh acinclude/libtool.m4
libtoolize --force || exit 1
aclocal -I acinclude || exit 1
autoconf || exit 1
#automake --add-missing || exit 1

# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/sdl-1.2.15-mintelf-config.patch"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-video-opengl --disable-threads ${CONFIGURE_FLAGS_AMIGAOS}"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	LIBS="-lm" \
	${srcdir}/configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m68020-60'
	hack_lto_cflags
	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1

	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done


move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
