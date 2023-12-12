#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=pegs
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

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	export CROSS_PREFIX=${TARGET}-
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS" LDFLAGS="${STACKSIZE} -s" || exit 1

	mkdir -p "${THISPKG_DIR}/editor"
	cp -p editor/pegs_ed "${THISPKG_DIR}/editor/pegs_ed-${CPU}.prg"
	cp -p src/pegs "${THISPKG_DIR}/pegs-${CPU}.prg"
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
cp -pr editor/gfx editor/gui editor/map_01.dat "${THISPKG_DIR}/editor"
cp -p README.txt GNU.txt "${THISPKG_DIR}"
cp -pr gfx maps sounds "${THISPKG_DIR}"

cd "${THISPKG_DIR}"
unix2dos *.txt

make_bin_archive
make_archives
