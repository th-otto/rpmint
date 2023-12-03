#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=griffon
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"
export CROSS_PREFIX=${TARGET}-

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p build/griffon "${THISPKG_DIR}/griffon-${CPU}.prg"

	cp -pr COPYING LICENSE README build/objectdb.dat build/readme.txt build/art build/data build/mapdb build/music build/sfx build/griffon.png "${THISPKG_DIR}"
	
	${MAKE} clean >/dev/null
done

make_bin_archive
make_archives
