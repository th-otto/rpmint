#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=metrocross
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

	cd metrocross0
	./swapdata levels/*.edt || exit 1
	cd ..

	mkdir -p "${THISPKG_DIR}/level_ed"
	cp -p metrocross0/metro "${THISPKG_DIR}/metro-${CPU}.prg"
	cp -p config0/metro_cfg "${THISPKG_DIR}/metro_cfg-${CPU}.prg"
	cp -p psdprot0/psdprot "${THISPKG_DIR}/psdprot-${CPU}.ttp"
	cp -p exechk0/exechk "${THISPKG_DIR}/exechk-${CPU}.ttp"
	cp -p edtile0/EdTile1  "${THISPKG_DIR}/level_ed/edtile-${CPU}.prg"
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
mkdir -p "${THISPKG_DIR}/gfx"
cp -pr edtile0/_FILE_FORMAT.txt "${THISPKG_DIR}/level_ed"
cp -p metrocross0/_README.txt "${THISPKG_DIR}"
cp -pr metrocross0/metro.cfg metrocross0/levels metrocross0/sfx "${THISPKG_DIR}"
cp -p metrocross0/gfx/{sprbuf.bin,sprdef.bin,sprpal.bin,bkg0.psd,gnd0.psd,img_roto.psd,mclogo.psd} "${THISPKG_DIR}/gfx"

cd "${THISPKG_DIR}"
rm -f levels/mst.bmp
unix2dos *.txt

make_bin_archive
make_archives
