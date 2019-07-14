#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ping
VERSION=-20190714
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/ping-20190714-mint.patch
"

BINFILES="
/bin/ping
${TARGET_MANDIR}/man8/ping.8.gz
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"

NO_STRIP=1

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s -o ping ping.c ping_hostops.c -lm || exit 1
	
	mkdir -p "${THISPKG_DIR}${sysroot}"/bin
	install -m 4555 ping "${THISPKG_DIR}${sysroot}"/bin
	mkdir -p "${THISPKG_DIR}${sysroot}"${TARGET_MANDIR}/man8
	install -m 444 ping.8 "${THISPKG_DIR}${sysroot}"${TARGET_MANDIR}/man8
	
	rm -f ping

	make_bin_archive $CPU
done

make_archives
