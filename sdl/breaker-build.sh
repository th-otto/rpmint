#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=breaker
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"
srcdir="${here}/${PACKAGENAME}3264"
MINT_BUILD_DIR="$srcdir"

BINFILES="
${PACKAGENAME}
"

unpack_archive
rm -f lvl_grabber.tar.gz

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
export CROSS_PREFIX=${TARGET}-

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p breaker "${THISPKG_DIR}/breaker-${CPU}.prg"

	${MAKE} clean >/dev/null

	cp -pr _LISEZMOI.txt _README.txt gfx sfx "${THISPKG_DIR}"

done

make_bin_archive
make_archives
