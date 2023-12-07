#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=xpired
VERSION=
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
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	LDFLAGS="${STACKSIZE} -s"

	${MAKE} -C src CPU_CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" || exit 1

	mkdir -p "${THISPKG_DIR}"

	mv src/xpired "${THISPKG_DIR}/xpired-${CPU}.prg" || exit 1
	mv src/xpiredit "${THISPKG_DIR}/xpiredit-${CPU}.gtp" || exit 1
	${MAKE} -C src clean
done

cd "$MINT_BUILD_DIR"

cp -p Readme.linux Readme.txt xpired.lvl xpired.cfg bgimages.txt xpired.dmo obsolete.lvl obsolete.txt firstlevel.dmo "${THISPKG_DIR}" || exit 1
cp -pr img snd "${THISPKG_DIR}"

make_bin_archive
make_archives
