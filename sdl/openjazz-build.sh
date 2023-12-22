#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=openjazz
VERSION=-20231028
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"
EXTRA_DIST="patches/${PACKAGENAME}/${PACKAGENAME}-shareware.tar.xz"

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
	cp -p OpenJazz "${THISPKG_DIR}/OpenJazz-${CPU}.prg"

	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p licenses.txt README.md COPYING "${THISPKG_DIR}"
cp -p res/unix/OpenJazz.6.adoc "${THISPKG_DIR}/OpenJazz.txt"

cd "${THISPKG_DIR}"
unix2dos *.txt
tar xf "${scriptdir}/patches/${PACKAGENAME}/${PACKAGENAME}-shareware.tar.xz"

make_bin_archive
make_archives
