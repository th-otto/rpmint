#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zeldapicross_us
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh
THISPKG_DIR="${DIST_DIR}/zeldapicross"

PATCHES="patches/zeldaroth/${PACKAGENAME}.patch"

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

	mv ZeldaPicross "${THISPKG_DIR}/ZeldaPicross-${CPU}.prg" || exit 1
	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -pr data "${THISPKG_DIR}"

PACKAGENAME="zeldapicross"
make_bin_archive
make_archives
