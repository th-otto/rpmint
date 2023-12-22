#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=starfighter
VERSION=-1.2
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"
EXTRA_DIST="patches/${PACKAGENAME}/${PACKAGENAME}-music.tar.xz"

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
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" DATADIR=./ || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p starfighter "${THISPKG_DIR}/starfighter-${CPU}.prg"
	cp -p starfighter.pak "${THISPKG_DIR}"

	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
cp -p docs/LICENSE docs/index.html "${THISPKG_DIR}"

cd "${THISPKG_DIR}"
tar xf "${scriptdir}/patches/${PACKAGENAME}/${PACKAGENAME}-music.tar.xz"

make_bin_archive
make_archives
