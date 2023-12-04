#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=SDL_sound
VERSION=-1.0.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/sdl_sound/sdl_sound-mint.patch
"
DISABLED_PATCHES="
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 build-scripts/ltmain.sh acinclude/libtool.m4 acinclude/lt*
libtoolize --force || exit 1
aclocal -I acinclude || exit 1
autoconf || exit 1
automake --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" build-scripts/config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"

#
# check that sdl.pc was installed.
# without it, SDL.m4 uses the sdl-config script from the host
# which does not work when cross-compiling
#
if test "`pkg-config --modversion sdl 2>/dev/null`" = ""; then
	echo "SDL and/or sdl.pc is missing" >&2
	exit 1
fi

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	: hack_lto_cflags

	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

mkdir -p ${THISPKG_DIR}${sysroot}/usr/lib/pkgconfig
cat > ${THISPKG_DIR}${sysroot}/usr/lib/pkgconfig/SDL_sound.pc << EOF
prefix=/usr
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include

Name: SDL_sound
Description: SDL_sound; an abstract soundfile decoder.
Version: ${VERSION#-}
Requires: sdl >= 1.2.10
Libs: -lSDL_sound -lSDL -lldg -lgem -lmpg123 -lmikmod -lm
Cflags: -I\${includedir}/SDL
EOF

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
