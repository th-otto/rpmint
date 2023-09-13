#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=SDL
VERSION=-1.2.16-hg
#VERSIONPATCH=-20171006
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/sdl/sdl-1.2.16-asm.patch
patches/sdl/sdl-gsxb.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
patches/sdl/sdl-1.2.15-c99.patch
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh acinclude/libtool.m4 acinclude/lt*
libtoolize --force || exit 1
aclocal -I acinclude || exit 1
autoconf || exit 1
#automake --force --copy --add-missing || exit 1

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" build-scripts/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-video-opengl
	--disable-threads
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	LIBS="-lm" \
	${srcdir}/configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	: hack_lto_cflags
	# ICONV isn't really used
	sed -i 's/ -liconv//' config.status
	./config.status

	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	rm -f "${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/sdl-config"
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done


move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
