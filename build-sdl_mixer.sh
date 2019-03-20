#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=SDL_mixer
VERSION=-1.2.12
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/sdl_mixer/double-free-crash.patch
patches/sdl_mixer/mikmod1.patch
patches/sdl_mixer/mikmod2.patch
patches/sdl_mixer/config.patch
patches/sdl_mixer/mintelf-config.patch
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
#libtoolize --force || exit 1
aclocal -I acinclude || exit 1
autoconf || exit 1

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
