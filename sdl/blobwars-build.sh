#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=blobwars
VERSION=-2.00
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
export CROSS_PREFIX=${TARGET}-
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p BlobWars "${THISPKG_DIR}/BlobWars-${CPU}.prg"

	${MAKE} clean >/dev/null

done

${MAKE} buildpak || exit 1

: cp -pr Readme_MorphOS "${THISPKG_DIR}/README"
cp -pr blobwars.pak doc locale "${THISPKG_DIR}"
mkdir "${THISPKG_DIR}"/config
mkdir "${THISPKG_DIR}"/save
mkdir "${THISPKG_DIR}"/snapshot

# 

make_bin_archive
${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${BINTARNAME}-data.tar.xz locale data gfx music sound
make_archives
