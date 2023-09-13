#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=traceroute
VERSION=-1.4a5
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/traceroute-mint.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

BINFILES="
sbin/*
${TARGET_MANDIR#/}/man8/*
"

unpack_archive

cd "$srcdir"

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS ${ELF_CFLAGS}"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CC=${TARGET}-gcc \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	./configure
	
	make
	
	mkdir -p "${THISPKG_DIR}${sysroot}/sbin"
	install -m 4755 traceroute "${THISPKG_DIR}${sysroot}/sbin"
	mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man8"
	install -m 644 traceroute.8 "${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man8"
	
	make clean

	make_bin_archive $CPU
done

make_archives
