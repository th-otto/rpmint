#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zlib
VERSION=-1.2.11
VERSIONPATCH=-20171006

. ${scriptdir}/functions.sh

PATCHES="patches/zlib/zlib-1.2.11-pkgconfig.patch \
patches/zlib/zlib-1.2.11-0012-format.patch \
patches/zlib/zlib-1.2.11-0013-segfault.patch \
"

unpack_archive

export CHOST=$TARGET
COMMON_CFLAGS="-O3 -fomit-frame-pointer $LTO_CFLAGS ${CFLAGS_AMIGAOS}"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure --prefix=${prefix} --libdir='${exec_prefix}/lib'$multilibdir ${CONFIGURE_FLAGS_AMIGAOS}
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
