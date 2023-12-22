#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=megamario
VERSION=-1.7
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"
EXTRA_DIST=patches/timidity.tar.xz

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
	${MAKE} $JOBS CROSS_PREFIX=${TARGET}- CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" DATADIR=data || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p megamario "${THISPKG_DIR}/megamario-${CPU}.prg"
	
	${MAKE} clean >/dev/null
done

cp -p  CONTROLS.txt mario.ini "Official MegaMario Homepage.url" fixes_v1.7.txt licence.txt megamario.png atari.txt readme.txt "${THISPKG_DIR}"
cp -pr data "${THISPKG_DIR}"
cp -pr help screens "${THISPKG_DIR}"
cp -pr mp3music "${THISPKG_DIR}/data/sfx"
mkdir -p "${THISPKG_DIR}/data/sfx/wavmusic"
cd "${THISPKG_DIR}/data/sfx/mp3music"
ffparams="-acodec pcm_u8 -ar 22050"
for i in *.mp3; do ffmpeg -i $i $ffparams ../wavmusic/${i%.mp3}.wav; done
echo 1 > ../wavmusic/music_available.dat
cd "${THISPKG_DIR}"
unix2dos *.txt

tar -C "${THISPKG_DIR}" -xf "${scriptdir}/patches/timidity.tar.xz"

make_bin_archive
make_archives
