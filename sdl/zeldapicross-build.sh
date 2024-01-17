#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zeldapicross
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""
EXTRA_DIST=patches/timidity.tar.xz

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

	cd "$MINT_BUILD_DIR"

	export CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	export LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory"
	
	${MAKE} ${JOBS} || exit 1

	mkdir -p "${THISPKG_DIR}/data/locale"

	mv ZeldaPicross "${THISPKG_DIR}/ZeldaPicross-${CPU}.prg" || exit 1
	cp -pr data/locale/* "${THISPKG_DIR}/data/locale"

	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -pr data UserGuide.pdf solution "${THISPKG_DIR}"
tar -C "${THISPKG_DIR}" -xf "${here}/patches/timidity.tar.xz"
mkdir -p "${THISPKG_DIR}/saves"

make_bin_archive
make_archives
