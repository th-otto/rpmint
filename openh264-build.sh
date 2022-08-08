#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=openh264
VERSION=-2.3.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/${PACKAGENAME}${VERSION}-mint.patch
"
BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	OS=freemint \
	ARCH=m68k \
	CC="${TARGET}-gcc" \
	CXX="${TARGET}-g++" \
	AR="${ar}" \
	ARFLAGS=rcs \
	RANLIB=${ranlib} \
	NM=${TARGET}-nm \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	${MAKE} V=Yes $JOBS || exit 1

	OS=freemint \
	ARCH=m68k \
	${MAKE} PREFIX="${THISPKG_DIR}${sysroot}/usr" LIBDIR_NAME='lib'$multilibdir install || exit 1
	mkdir -p "${THISPKG_DIR}${sysroot}/usr/bin"
	cp h264dec h264enc "${THISPKG_DIR}${sysroot}/usr/bin"
	
	OS=freemint \
	ARCH=m68k \
	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
