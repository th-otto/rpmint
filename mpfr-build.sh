#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mpfr
VERSION=-4.2.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

# disable lto for this package since it is needed for native compilers
ranlib=${TARGET}-ranlib
LTO_CFLAGS=

EXTRA_DIST="patches/automake/mintelf-config.sub"

unpack_archive

cd "$srcdir"

cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--prefix=${prefix} --host=${TARGET}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	# hack_lto_cflags
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
