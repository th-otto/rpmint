#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=amphetamine
VERSION=-0.8.10
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
export CROSS_PREFIX=${TARGET}-

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -pr amph "${THISPKG_DIR}/amph.prg"

	cp -pr COPYING ChangeLog NEWS README game "${THISPKG_DIR}"
	
	${MAKE} clean >/dev/null
	make_bin_archive $CPU
done

make_archives
