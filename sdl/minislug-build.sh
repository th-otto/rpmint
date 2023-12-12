#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=minislug
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
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s" || exit 1

	cd minislug0
	: ./swapdata lev*/*.edt || exit 1
	cd ..

	mkdir -p "${THISPKG_DIR}/level_ed"
	cp -p minislug0/minislug "${THISPKG_DIR}/minislug-${CPU}.prg"
	cp -p config0/config "${THISPKG_DIR}/minislug_cfg-${CPU}.prg"
	cp -p psdprot0/psdprot "${THISPKG_DIR}/psdprot-${CPU}.ttp"
	cp -p exechk0/exechk "${THISPKG_DIR}/exechk-${CPU}.ttp"
	cp -p edtile0/EdTile1  "${THISPKG_DIR}/level_ed/edtile-${CPU}.prg"
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
mkdir -p "${THISPKG_DIR}/gfx"
cp -pr edtile0/_FILE_FORMAT.txt edtile0/test "${THISPKG_DIR}/level_ed"
cp -p minislug0/_LISEZMOI_final.txt minislug0/_README_final.txt "${THISPKG_DIR}"
cp -pr minislug0/mslug.cfg minislug0/lev* minislug0/sfx "${THISPKG_DIR}"
cp -p minislug0/gfx/{sprbuf.bin,sprdef.bin,sprpal.bin,ms0.gif,bkg1.psd,gameover320.psd} "${THISPKG_DIR}/gfx"

cd "${THISPKG_DIR}"
rm -f "lev4/_Copie de lev4.edt"
rm -f "lev4/_Copie de lev4_plane2.psd"
rm -f "lev6/_lev6_plane1_wrk02.psd"
rm -f "lev6/lev6.edt_"
rm -f "lev8/_Copie de lev8_plane2.psd"
rm -f "lev8/__Copie de lev8_plane2.psd"
rm -f lev*/*.backup
rm -f lev*/mst.bmp

make_bin_archive
make_archives
