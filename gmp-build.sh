#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gmp
VERSION=-6.2.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

# disable lto for this package since it is needed for native compilers
ranlib=${TARGET}-ranlib
LTO_CFLAGS=

PATCHES="
patches/${PACKAGENAME}/gmp-coldfire.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
libtoolize --force

aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O3 -fomit-frame-pointer"

CONFIGURE_FLAGS="--prefix=${prefix} --host=${TARGET} --enable-cxx --enable-fat"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	# disable assembly for ColdFire for now; does not work yet
	assembly=
	if test $CPU = v4e; then
		assembly="--disable-assembly --disable-fat"
	fi
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} $assembly --libdir='${exec_prefix}/lib'$multilibdir
	# hack_lto_cflags
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
