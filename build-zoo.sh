#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zoo
VERSION=-2-10-1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/zoo/zoo.patch
patches/zoo/zoo-2.10-tempfile.patch
patches/zoo/zoo-gcc.patch
patches/zoo/zoo-2.10-CAN-2005-2349.patch
patches/zoo/zoo-return.patch
patches/zoo/zoo-security_pathsize.patch
patches/zoo/zoo-security_parse.patch
patches/zoo/zoo-2.10-security-infinite_loop.patch
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

srcdir="$srcdir/v2-10.1"
MINT_BUILD_DIR="$srcdir"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O3 -fomit-frame-pointer $LTO_CFLAGS -DANSI_HDRS=1 -DANSI_PROTO=1 $LTO_CFLAGS"

export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} CC="${TARGET}-gcc" MODEL="$CPU_CFLAGS $COMMON_CFLAGS -D__linux" CFLAGS=-c zoo fiz || exit 1
	install -Dpm 0755 zoo "${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/zoo"
	install -Dpm 0755 fiz "${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/fiz"
	install -Dpm 0644 zoo.1 "${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man1/zoo.1"
	install -Dpm 0644 fiz.1 "${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man1/fiz.1"
	${MAKE} clean
	make_bin_archive $CPU
done

make_archives
