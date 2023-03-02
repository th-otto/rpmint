#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mtm
VERSION=-1.2.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/mtm/mtm-1.2.1-m68k-atari-mint.patch
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/terminfo
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-std=c99 -Wall -Wextra -pedantic -Os -fomit-frame-pointer $LTO_CFLAGS"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} CC="${TARGET}-gcc" CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" || exit 1
	install -Dpm 0755 mtm "${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/mtm"
	install -Dpm 0644 mtm.1 "${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man1/mtm.1"
	tic -s -x -o"${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/terminfo" mtm.ti
	${MAKE} clean
	make_bin_archive $CPU
done

make_archives
