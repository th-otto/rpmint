#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=hocoslamfy
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

	cd "$MINT_BUILD_DIR"

	export CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	export LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory"
	
	${MAKE} $JOBS V=0 DEFS=-DDONT_USE_PWD || exit 1

	mkdir -p "${THISPKG_DIR}"

	mv hocoslamfy "${THISPKG_DIR}/hocoslamfy-${CPU}.prg" || exit 1
	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -pr data "${THISPKG_DIR}"

cd "${THISPKG_DIR}/data"
# rename to 8+3
mv manual-en.txt ../manual.txt
mv Mountains.png Mountain.png
mv TitleHeader1.png TitleH1.png
mv TitleHeader2.png TitleH2.png
mv TitleHeader3.png TitleH3.png
mv TitleHeader4.png TitleH4.png
mv TitleHeader5.png TitleH5.png
mv TitleHeader6.png TitleH6.png
mv TitleHeader7.png TitleH7.png
mv TitleHeader8.png TitleH8.png
mv collision.wav collisio.wav
mv highscore.wav highscor.wav
mv hocoslamfy.png hocoslam.png
mv GameOverHeader.png GOverH.png

rm -f default.gcw0.desktop

cd "$MINT_BUILD_DIR"
cp -p COPYRIGHT README.md "${THISPKG_DIR}"

make_bin_archive
make_archives
