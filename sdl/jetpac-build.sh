#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=jetpac
VERSION=-0.2.5
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
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	cd "$MINT_BUILD_DIR"

	${MAKE} ${JOBS} CPU_CFLAGS="$CPU_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" || exit 1

	mkdir -p "${THISPKG_DIR}"

	mv jetpac "${THISPKG_DIR}/jetpac-${CPU}.prg" || exit 1
	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -pr pixmaps "${THISPKG_DIR}"
cp -p README StuffDone ToDo icon.bmp "${THISPKG_DIR}"
cp -p gpl.txt "${THISPKG_DIR}/COPYING"

make_bin_archive
make_archives
