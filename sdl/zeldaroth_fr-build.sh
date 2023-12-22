#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zeldaroth_fr
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh
THISPKG_DIR="${DIST_DIR}/zeldaroth"

PATCHES="patches/zeldaroth/${PACKAGENAME}.patch"
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
	
	cd src
	${MAKE} ${JOBS} || exit 1

	mkdir -p "${THISPKG_DIR}"

	mv ZeldaROTH "${THISPKG_DIR}/ZeldaROTH-${CPU}.prg" || exit 1
	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -pr src/data "${THISPKG_DIR}"
tar -C "${THISPKG_DIR}" -xf "${here}/patches/timidity.tar.xz"

PACKAGENAME="zeldaroth"
make_bin_archive
make_archives
