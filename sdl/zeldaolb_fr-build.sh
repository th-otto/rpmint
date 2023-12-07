#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zeldaolb_fr
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh
THISPKG_DIR="${DIST_DIR}/zeldaolb"

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
	export LDFLAGS="${STACKSIZE} -s"
	
	${MAKE} ${JOBS} || exit 1

	mkdir -p "${THISPKG_DIR}"

	mv ZeldaOLB "${THISPKG_DIR}/ZeldaOLB-${CPU}.prg" || exit 1
	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -pr data "${THISPKG_DIR}"
tar -C "${THISPKG_DIR}" -xf "${here}/patches/timidity.tar.xz"

PACKAGENAME="zeldaolb"
make_bin_archive
make_archives
