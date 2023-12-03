#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=airball
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

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	export CROSS_PREFIX=${TARGET}-
	${MAKE} CPU_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" || exit 1

	cd airball0
	./swapdata || exit 1
	cd ..

	mkdir -p "${THISPKG_DIR}/level_ed"
	cp -pr airball0/airball.prg airball0/airball.cfg airball0/data "${THISPKG_DIR}"
	cp -pr config0/airball_cfg.prg exechk0/exechk.ttp psdprot0/psdprot.ttp "${THISPKG_DIR}"
	cp -pr level_ed0/airball_ed.prg level_ed0/*.bmp level_ed0/tmp.txt level_ed0/_rooms.txt level_ed0/rooms.bin "${THISPKG_DIR}/level_ed"
	
	${MAKE} clean >/dev/null
	make_bin_archive $CPU
done

make_archives
