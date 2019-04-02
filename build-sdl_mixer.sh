#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=SDL_mixer
VERSION=-1.2.13
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/sdl_mixer/double-free-crash.patch
patches/sdl_mixer/config.patch
patches/sdl_mixer/amigaos.patch
patches/sdl_mixer/mintelf-config.patch
"
DISABLED_PATCHES="
patches/sdl_mixer/mikmod1.patch
patches/sdl_mixer/mikmod2.patch
patches/sdl_mixer/smpeg-config.patch
"

BINFILES="
${TARGET_BINDIR#/}/playwave
${TARGET_BINDIR#/}/playmus
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
#libtoolize --force || exit 1
aclocal -I acinclude || exit 1
autoconf || exit 1

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

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
	hack_lto_cflags
	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install-bin
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
