#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=airball
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
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" || exit 1

	cd airball0
	./swapdata || exit 1
	cd ..

	mkdir -p "${THISPKG_DIR}/level_ed"
	cp -p airball0/airball "${THISPKG_DIR}/airball-${CPU}.prg"
	cp -p config0/airball_cfg "${THISPKG_DIR}/airball_cfg-${CPU}.prg"
	cp -p psdprot0/psdprot "${THISPKG_DIR}/psdprot-${CPU}.ttp"
	cp -p exechk0/exechk "${THISPKG_DIR}/exechk-${CPU}.ttp"
	cp -pr airball0/airball.cfg airball0/data "${THISPKG_DIR}"
	cp -p level_ed0/airball_ed "${THISPKG_DIR}/level_ed/airball_ed-${CPU}.prg"
	cp -pr level_ed0/*.bmp level_ed0/tmp.txt level_ed0/_rooms.txt level_ed0/rooms.bin "${THISPKG_DIR}/level_ed"
	
	${MAKE} clean >/dev/null
done

make_bin_archive
make_archives
