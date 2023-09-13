#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zlib
VERSION=-1.2.13
VERSIONPATCH=-20230301

. ${scriptdir}/functions.sh

# disable lto for this package since it is needed for native compilers
ranlib=${TARGET}-ranlib
LTO_CFLAGS=

PATCHES="patches/zlib/zlib-pkgconfig.patch \
patches/zlib/zlib-1.2.12-0012-format.patch \
patches/zlib/zlib-1.2.12-0013-segfault.patch \
"

unpack_archive

export CHOST=$TARGET
COMMON_CFLAGS="-O3 -fomit-frame-pointer ${ELF_CFLAGS} ${CFLAGS_AMIGAOS}"

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
