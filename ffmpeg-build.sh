#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ffmpeg
VERSION=-6.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/ffmpeg/ffmpeg-arm6l.patch
patches/ffmpeg/ffmpeg-avfilter-vf_libplacebo-remove-deprecated-field.patch
patches/ffmpeg/ffmpeg-chromium.patch
patches/ffmpeg/ffmpeg-codec-choice.patch
patches/ffmpeg/ffmpeg-new-coder-errors.patch
patches/ffmpeg/ffmpeg-mint.patch
"
DISABLED_PATCHES="
patches/ffmpeg/ffmpeg-4.2-dlopen-fdk_aac.patch
patches/ffmpeg/ffmpeg-dlopen-headers.tar.xz
patches/ffmpeg/ffmpeg-dlopen-openh264.patch
patches/ffmpeg/ffmpeg-enable_decoders
patches/ffmpeg/ffmpeg-enable_encoders
patches/ffmpeg/ffmpeg-work-around-abi-break.patch
patches/ffmpeg/ffmpeg_get_dlopen_headers.sh
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-cross-compile
	--pkg-config=${TARGET}-pkg-config
	--target-os=freemint
	--cross-prefix=${TARGET}-
	--arch=m68k
	--enable-static
	--disable-shared
	--disable-pic
	--enable-libxml2
	--enable-libvorbis
	--enable-libtheora
	--enable-libopus
	--enable-libmp3lame
	--enable-libfribidi
	--enable-libfreetype
	--enable-libfdk-aac
	--enable-libaom
	--enable-lcms2
	--enable-libvpx
	--enable-libwebp
	--enable-libx264
	--enable-libx265
	--disable-debug
	--enable-gpl
	--enable-version3
	--enable-nonfree
	--enable-openssl
	--disable-xlib
	--disable-libxcb
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--extra-cxxflags="$CPU_CFLAGS $COMMON_CFLAGS" \
	--extra-cflags="$CPU_CFLAGS $COMMON_CFLAGS" \
	--extra-ldflags="$CPU_CFLAGS $COMMON_CFLAGS" \
	--libdir="${prefix}/lib$multilibdir" || exit 1

	# hack_lto_cflags
	${MAKE} V=1 $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
