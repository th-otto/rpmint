#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=blobwars
VERSION=-1.14
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
export CROSS_PREFIX=${TARGET}-

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR/src"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p BlobWars "${THISPKG_DIR}/BlobWars-${CPU}.prg"

	${MAKE} clean >/dev/null

	cd ..
	
	cp -pr Readme_MorphOS "${THISPKG_DIR}/README"
	cp -pr blobwars.pak doc locale "${THISPKG_DIR}"

done

make_bin_archive
make_archives
