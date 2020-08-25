#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=arc
VERSION=-5.21p
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/arc/arc-time.patch"

BINFILES="
${TARGET_BINDIR}/arc
${TARGET_BINDIR}/marc
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -s -Wall $LTO_CFLAGS"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}

	sed -i "s:^PREFIX = .*:PREFIX = ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}:
s:^SYSTEM = .*:SYSTEM = -DBSD=1:
s:^OPT = .*:OPT = ${COMMON_CFLAGS} ${CPU_CFLAGS}:
s:^CC = .*:CC = ${TARGET}-gcc:
s:install -s:install:g" Makefile

	${MAKE} $JOBS || exit 1
	${MAKE} install || exit 1
	${MAKE} clean
	make_bin_archive $CPU
done

configured_prefix="${prefix}"

make_archives
