#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mpfr
VERSION=-3.1.6
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/mpfr/mintelf-config.patch"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O3 -fomit-frame-pointer"

CONFIGURE_FLAGS="--prefix=${prefix} --host=${TARGET}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in 020 v4e 000; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval libdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$libdir
	hack_lto_cflags
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
