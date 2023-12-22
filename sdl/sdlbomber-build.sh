#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=sdlbomber
VERSION=-1.0.4
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
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	export CROSS_PREFIX=${TARGET}-
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p bomber "${THISPKG_DIR}/bomber-${CPU}.prg"
	cp -p matcher "${THISPKG_DIR}/bomber-${CPU}.ttp"

	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p AUTHORS COPYING ChangeLog README "${THISPKG_DIR}"
cp -pr data "${THISPKG_DIR}"

cd "${THISPKG_DIR}"
rm -rf data/CVS

make_bin_archive
make_archives
