#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=deathris
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

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	LDFLAGS="${STACKSIZE} -s"

	echo "${TARGET}-g++ ${CXXFLAGS} ${LDFLAGS} -o deathris"
	${TARGET}-g++ ${CXXFLAGS} ${LDFLAGS} -o deathris tetris.cpp `pkg-config --cflags --libs SDL_mixer SDL_image` || exit 1

	mkdir -p "${THISPKG_DIR}/data"

	mv deathris "${THISPKG_DIR}/deathris-${CPU}.prg" || exit 1
done

cd "$MINT_BUILD_DIR"

cp -p README.md highscore.dat "${THISPKG_DIR}"
cp -p *.png *.wav "${THISPKG_DIR}/data"

make_bin_archive
make_archives
