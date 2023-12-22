#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=tetris
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"
EXTRA_DIST="patches/${PACKAGENAME}/fnt.bmp"


BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	export CROSS_PREFIX=${TARGET}-
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p tetris "${THISPKG_DIR}/tetris-${CPU}.prg"
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
cp -p _LISEZMOI.txt "${THISPKG_DIR}"
cp -pr gfx sfx "${THISPKG_DIR}"

# replace fnt.bmp from original archive, which is broken
cp -p "${scriptdir}/patches/${PACKAGENAME}/fnt.bmp" "${THISPKG_DIR}/gfx"

make_bin_archive
make_archives
