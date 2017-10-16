#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zip
VERSION=-3.0
VERSIONPATCH=
srcarchive="${PACKAGENAME}30"

. ${scriptdir}/functions.sh

PATCHES="
patches/zip/zip-3.0-iso8859_2.patch
patches/zip/zip-3.0-add_options_to_help.patch
patches/zip/zip-3.0-nonexec-stack.patch
patches/zip/zip-3.0-optflags.patch
patches/zip/zip-3.0-tempfile.patch
patches/zip/zip-notimestamp.patch
patches/zip/zip-3.0-nomutilation.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

srcdir="$here/$srcarchive"
MINT_BUILD_DIR="$srcdir"
unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O3 -fomit-frame-pointer $LTO_CFLAGS"

export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in 020 v4e 000; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval libdir=\${CPU_LIBDIR_$CPU}
	make -f unix/Makefile prefix=${prefix} CC="${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS" CPP="${TARGET}-gcc -E $CPU_CFLAGS $COMMON_CFLAGS" generic || exit 1
	make -f unix/Makefile BINDIR="${THISPKG_DIR}${sysroot}${TARGET_BINDIR}" MANDIR=${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man1 install
	make -f unix/Makefile clean
	make_bin_archive $CPU
done

make_archives
