#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=xrick
VERSION=-021212
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/xrick/xrick.patch
"

EXTRA_DIST="
"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}

	${MAKE} $JOBS CROSS_PREFIX=$TARGET- CPU_CFLAGS="$CPU_CFLAGS" LDFLAGS="-s -Wl,--msuper-memory" || exit 1

	mkdir -p "${THISPKG_DIR}"
	mv xrick "${THISPKG_DIR}/xrick-${CPU}.prg" || exit 1
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p KeyCodes README xrick.6.gz "${THISPKG_DIR}"
gzip -dc xrick.6.gz | nroff -Tascii -c -man > "${THISPKG_DIR}/xrick.man"
mkdir -p "${THISPKG_DIR}/data"
unzip data.zip -d "${THISPKG_DIR}/data"

make_bin_archive
make_archives
