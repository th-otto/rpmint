#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=freecraft
VERSION=-1.18
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"
EXTRA_DIST="
patches/${PACKAGENAME}/${PACKAGENAME}-data.tar.xz
"

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
	${MAKE} $JOBS CPU_CFLAGS="$CPU_CFLAGS" LDFLAGS="${STACKSIZE} -s"
	${MAKE} CPU_CFLAGS="$CPU_CFLAGS" LDFLAGS="${STACKSIZE} -s" || exit 1

	mkdir -p "${THISPKG_DIR}/tools"
	cp -p freecraft "${THISPKG_DIR}/freecraft-${CPU}.prg"
	cp -p tools/wartool "${THISPKG_DIR}/tools/wartool-${CPU}.prg"
	cp -p tools/startool "${THISPKG_DIR}/tools/startool-${CPU}.prg"
	cp -p tools/aledoc "${THISPKG_DIR}/tools/aledoc-${CPU}.prg"
	cp -p tools/build.sh "${THISPKG_DIR}/tools"
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
cp -p README "${THISPKG_DIR}"
cp -pr data doc contrib "${THISPKG_DIR}"

cd "${THISPKG_DIR}"
tar -xf "${scriptdir}/patches/${PACKAGENAME}/freecraft-data.tar.xz"

make_bin_archive
make_archives
