#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zlib
VERSION=-1.3.1
VERSIONPATCH=-20240511

. ${scriptdir}/functions.sh

# disable lto for this package since it is needed for native compilers
ranlib=${TARGET}-ranlib
LTO_CFLAGS=

PATCHES="
patches/zlib/zlib-pkgconfig.patch
patches/zlib/zlib-1.2.12-0013-segfault.patch
patches/zlib/zlib-shared.patch
"

unpack_archive

export CHOST=$TARGET
COMMON_CFLAGS="-O3 -fomit-frame-pointer ${ELF_CFLAGS} ${CFLAGS_AMIGAOS}"
CONFIGURE_FLAGS="--prefix=${prefix}"

WITH_FASTCALL=`if $gcc -mfastcall -E - < /dev/null >/dev/null 2>&1; then echo true; else echo false; fi`

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	if $WITH_FASTCALL; then
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir/mfastcall ${CONFIGURE_FLAGS_AMIGAOS}
		${MAKE} $JOBS || exit 1
		${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
		${MAKE} distclean
	fi

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir ${CONFIGURE_FLAGS_AMIGAOS}
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1

	${MAKE} distclean
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
