#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ncompress
VERSION=-5.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
"
EXTRA_DIST="
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$srcdir"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"
CMAKE_SYSTEM_NAME="${TARGET##*-}"

export prefix=${prefix}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	${MAKE} $JOBS \
		CC="${TARGET}-gcc" \
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		|| exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" PREFIX="${prefix}" install

	# do not replace zcmp/zmore/zdiff from gzip
	rm -f ${THISPKG_DIR}${sysroot}${prefix}/bin/{zcmp,zmore,zdiff,zcat}

	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
