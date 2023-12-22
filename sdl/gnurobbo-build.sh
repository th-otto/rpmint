#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gnurobbo
VERSION=-0.66
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
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	cd "$MINT_BUILD_DIR"

	export CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	${MAKE} ${JOBS} LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" || exit 1

	mkdir -p "${THISPKG_DIR}"

	mv gnurobbo "${THISPKG_DIR}/gnurobbo-${CPU}.prg" || exit 1
	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -pr data "${THISPKG_DIR}"
cp -p Bugs AUTHORS ChangeLog NEWS COPYING README TODO LICENSE-sound LICENSE-ttf "${THISPKG_DIR}"

make_bin_archive
make_archives
