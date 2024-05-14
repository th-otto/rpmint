#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=SDL_image
VERSION=-1.2.13
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/sdl_image/sdl_image-config.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I acinclude || exit 1
autoconf || exit 1
automake --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
	--disable-tif
	--disable-webp
"

#
# check that sdl.pc was installed.
# without it, SDL.m4 uses the sdl-config script from the host
# which does not work when cross-compiling
#
if test "`pkg-config --modversion sdl 2>/dev/null`" = ""; then
	echo "SDL and/or sdl.pc is missing" >&2
	exit 1
fi

WITH_FASTCALL=`if $gcc -mfastcall -E - < /dev/null >/dev/null 2>&1; then echo true; else echo false; fi`

STACKSIZE="-Wl,--msuper-memory"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	if $WITH_FASTCALL; then
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" \
		CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" \
		LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall ${STACKSIZE}" \
		LIBS="-lm" \
		${srcdir}/configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir/mfastcall

		${MAKE} $JOBS || exit 1

		${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
		${MAKE} distclean >/dev/null
	fi

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS ${STACKSIZE}" \
	LIBS="-lm" \
	${srcdir}/configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	: hack_lto_cflags
	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} distclean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
