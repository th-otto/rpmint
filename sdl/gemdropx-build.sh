#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gemdropx
VERSION=-0.9
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

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}

	export CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	export LDFLAGS="${STACKSIZE} -s"
	${MAKE}

	mkdir -p "${THISPKG_DIR}"

	mv gemdropx "${THISPKG_DIR}/gemdropx-${CPU}.prg" || exit 1
	${MAKE} clean

	${MAKE} nosound
	mv gemdropx "${THISPKG_DIR}/gemdropx-nosound-${CPU}.prg" || exit 1
	${MAKE} clean
done

cd "$MINT_BUILD_DIR"

cp -p AUTHORS.txt CHANGES.txt COPYING.txt ICON.txt README.txt TODO.txt "${THISPKG_DIR}"
cp -pr data/images data/sounds "${THISPKG_DIR}"

make_bin_archive
make_archives
