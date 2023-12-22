#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=opentyrian
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"
EXTRA_DIST="patches/${PACKAGENAME}/tyrian21.zip"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	export CROSS_PREFIX=${TARGET}-
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" TYRIAN_DIR=data || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p opentyrian "${THISPKG_DIR}/opentyrian-${CPU}.prg"

	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p CREDITS NEWS README COPYING linux/man/opentyrian.6 "${THISPKG_DIR}"

cd "${THISPKG_DIR}"
unix2dos NEWS README

mkdir -p data
cd data
unzip -j "${scriptdir}/patches/${PACKAGENAME}/tyrian21.zip"
rm -f *.exe *.ovl order.doc order.tfp

make_bin_archive
make_archives
