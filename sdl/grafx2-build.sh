#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=grafx2
VERSION=-2.8.3200
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

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
export CROSS_PREFIX=${TARGET}-

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR/src"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} MCPU=${CPU_CFLAGS} ATARICROSS=1 NOLAYERS=1 NORECOIL=1 \
		|| exit 1

	mkdir -p "${THISPKG_DIR}/doc"
	
	cp -p ../bin/grafx2.ttp "${THISPKG_DIR}/grafx2-${CPU}.ttp"
	${MAKE} clean >/dev/null
	cd ..

	cp -pr share/grafx2/gfx2def.ini share/grafx2/gfx2.png share/grafx2/scripts "${THISPKG_DIR}"
	mkdir -p "${THISPKG_DIR}/fonts"
	for f in share/grafx2/fonts/*; do
	  n=$(basename $f | sed -e 's/PF_\([a-zA-Z]\)[a-zA-Z]*_/PF\1/')
	  cp -p "$f" "${THISPKG_DIR}/fonts/$n"
	done
	mkdir -p "${THISPKG_DIR}/skins"
	for f in share/grafx2/skins/*; do
	  n=$(basename $f | sed -e 's/^\([a-z]\).*_/\1/')
	  cp -p "$f" "${THISPKG_DIR}/skins/$n"
	done
	cp -p doc/COMPILING.txt "${THISPKG_DIR}/doc/compile.txt"
	cp -p doc/README-6502.txt "${THISPKG_DIR}/doc/6502.txt"
	cp -p doc/README-recoil.txt "${THISPKG_DIR}/doc/recoil.txt"
	cp -p doc/README.txt "${THISPKG_DIR}/doc"
	cp -p doc/PF_fonts.txt "${THISPKG_DIR}/doc"
	cp -p doc/gpl-2.0.txt "${THISPKG_DIR}/doc"
done

make_bin_archive
make_archives
