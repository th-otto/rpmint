#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=2048
VERSION=-git
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"

BINFILES="
${PACKAGENAME}
"
EXTRA_DIST="patches/${PACKAGENAME}/fonts"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} $JOBS CROSS_PREFIX=${TARGET}- CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p 2048.prg "${THISPKG_DIR}/2048-${CPU}.prg"
	cp -pr ${BUILD_DIR}/patches/${PACKAGENAME}/fonts "${THISPKG_DIR}/"
	
	${MAKE} clean >/dev/null
done

make_bin_archive
make_archives
