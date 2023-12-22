#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=symphyla
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

	mkdir -p "${THISPKG_DIR}"
	cp -p symphyla "${THISPKG_DIR}/symphyla-${CPU}.prg"
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
cp -p README.md "${THISPKG_DIR}"
cp -pr gfx "${THISPKG_DIR}"
cd "${THISPKG_DIR}"
ffparams="-acodec pcm_u8 -ar 22050"
ffmpeg -i gfx/music1.mus $ffparams gfx/music1.wav
rm gfx/music1.mus

make_bin_archive
make_archives
