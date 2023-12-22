#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=airstrike
VERSION=-pre6a
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
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p airstrike "${THISPKG_DIR}/airstrike-${CPU}.prg"

	${MAKE} clean >/dev/null
	${MAKE} CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="${STACKSIZE} -s -Wl,--msuper-memory" airstrike-sound || exit 1
	cp -p airstrike "${THISPKG_DIR}/airstrike-sound-${CPU}.prg"

	cp -pr COPYING ChangeLog LICENSE README airstrikerc data doc pov "${THISPKG_DIR}"
	
	${MAKE} clean >/dev/null
done

make_bin_archive
make_archives
