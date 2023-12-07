#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=digger
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/${PACKAGENAME}.patch
patches/${PACKAGENAME}/${PACKAGENAME}-1.patch
patches/${PACKAGENAME}/${PACKAGENAME}-2.patch
patches/${PACKAGENAME}/${PACKAGENAME}-3.patch
patches/${PACKAGENAME}/${PACKAGENAME}-4.patch
patches/${PACKAGENAME}/${PACKAGENAME}-5.patch
"

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
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	LDFLAGS="${STACKSIZE} -s"

	${MAKE} -C src CPU_CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" || exit 1

	mkdir -p "${THISPKG_DIR}"

	mv src/digger "${THISPKG_DIR}/digger-${CPU}.prg" || exit 1
	${MAKE} -C src clean
done

cd "$MINT_BUILD_DIR"

cp -p digger-68k.readme digger.txt "${THISPKG_DIR}"

make_bin_archive
make_archives
