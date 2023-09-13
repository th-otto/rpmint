#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ctris
VERSION=-0.42
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""


BINFILES="
${TARGET_PREFIX#/}/games
${TARGET_MANDIR#/}/man6/*
"

MINT_BUILD_DIR="$srcdir"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fcommon ${ELF_CFLAGS}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} CC=${TARGET}-gcc CFLAGS="${CPU_CFLAGS} $COMMON_CFLAGS ${ELF_CFLAGS} ${LTO_CFLGS}"
	${MAKE} MANDIR="${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man6" BINDIR="${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/games" install || exit 1
	${MAKE} clean
	make_bin_archive $CPU
done

make_archives
