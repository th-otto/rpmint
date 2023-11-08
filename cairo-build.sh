#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=cairo
VERSION=-1.18.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/cairo/cairo-get_bitmap_surface-bsc1036789-CVE-2017-7475.diff
patches/cairo/cairo-xlib-endianness.patch
patches/cairo/cairo-mint.patch
" 
EXTRA_DIST="
patches/meson/m68k-atari-mint.txt
patches/meson/m68k-atari-mintelf.txt
"

BINFILES="
"

unpack_archive

cd "$srcdir"

cp ${BUILD_DIR}/patches/meson/m68k-atari-mint.txt .
cp ${BUILD_DIR}/patches/meson/m68k-atari-mintelf.txt .

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"
export PKG_CONFIG=${TARGET}-pkg-config

CONFIGURE_FLAGS="--cross-file ${TARGET}.txt --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	-D xcb=disabled
	-D freetype=enabled
	-D fontconfig=disabled
	-D glib=disabled
	-D gtk_doc=false
	-D spectre=disabled
	-D symbol-lookup=disabled
	-D tee=enabled
	-D tests=disabled
	-D xlib=disabled
	-D default_library=static
	-D buildtype=release
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	rm -rf build
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"meson" setup ${CONFIGURE_FLAGS} --libdir="${prefix}/lib$multilibdir" build || exit 1
	sed -i 's/-fPIC//g' build/meson-info/intro-targets.json build/build.ninja build/compile_commands.json
	echo "#undef CAIRO_HAS_PTHREAD" >> build/config.h
	echo "#undef CAIRO_HAS_REAL_PTHREAD" >> build/config.h
	echo "#define CAIRO_NO_MUTEX 1" >> build/config.h

	meson compile -C build || exit 1
	DESTDIR="${THISPKG_DIR}${sysroot}" meson install -C build || exit 1
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
