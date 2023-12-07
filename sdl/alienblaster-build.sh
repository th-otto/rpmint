#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=alienblaster
VERSION=-1.1.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"
srcdir="${here}/${PACKAGENAME}"
MINT_BUILD_DIR="$srcdir"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"
export CROSS_PREFIX=${TARGET}-
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p alienBlaster "${THISPKG_DIR}/alienBlaster-${CPU}.prg"

	cp -pr AUTHORS CHANGELOG LICENSE README VERSION cfg images sound "${THISPKG_DIR}"
	
	${MAKE} clean >/dev/null
done

make_bin_archive
make_archives
