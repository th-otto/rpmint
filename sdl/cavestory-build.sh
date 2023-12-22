#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=cavestory
VERSION=-1.0.0.6
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"
EXTRA_DIST="
patches/${PACKAGENAME}/${PACKAGENAME}en.tar.xz
patches/${PACKAGENAME}/cavestory-xm-data.tar.xz
"

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
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p nx "${THISPKG_DIR}/cavestory-${CPU}.prg"
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
cp -p LICENSE tilekey.dat smalfont.bmp font.ttf sprites.sif "${THISPKG_DIR}"

cd "${THISPKG_DIR}"
mkdir -p org xm replay pxt endpic
tar xf "${scriptdir}/patches/${PACKAGENAME}/${PACKAGENAME}en.tar.xz"
tar xf "${scriptdir}/patches/${PACKAGENAME}/cavestory-xm-data.tar.xz"

make_bin_archive
make_archives
