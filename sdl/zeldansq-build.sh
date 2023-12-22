#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zeldansq
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh

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
	export LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory"
	
	${MAKE} ${JOBS} release || exit 1

	mkdir -p "${THISPKG_DIR}"

	mv bin/Release/ZeldaNSQ "${THISPKG_DIR}/ZeldaNSQ-${CPU}.prg" || exit 1
	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -pr data saves config "${THISPKG_DIR}"

make_bin_archive
make_archives
