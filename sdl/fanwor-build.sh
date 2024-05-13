#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=fanwor
VERSION=-1.16
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/fanwor/fanwor-mint.patch
patches/fanwor/fanwor-atari.patch
"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing -fno-exceptions ${ELF_CFLAGS}"
export CROSS_PREFIX=${TARGET}-
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}

	cd "$MINT_BUILD_DIR"

	export CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	export LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory"
	
	${MAKE} ${JOBS} || exit 1

	mkdir -p "${THISPKG_DIR}"
	mv fanwor "${THISPKG_DIR}/fanwor-${CPU}.prg" || exit 1

	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -pr gpl.txt readme.txt graphics rooms sounds "${THISPKG_DIR}"

make_bin_archive
make_archives
