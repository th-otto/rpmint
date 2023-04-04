#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libbeecrypt
VERSION=-4.1.2
VERSIONPATCH=

srcarchive=beecrypt${VERSION}

. ${scriptdir}/functions.sh

PATCHES="
patches/libbeecrypt6/beecrypt-4.1.2.patch
patches/libbeecrypt6/beecrypt-4.1.2-build.patch
patches/libbeecrypt6/beecrypt-4.1.2-fix_headers.patch
patches/libbeecrypt6/beecrypt-libdir.patch
patches/libbeecrypt6/beecrypt-no-asm-m68k.patch
patches/libbeecrypt6/beecrypt-enable-cplusplus.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

BINFILES=""

srcdir="$here/$srcarchive"
MINT_BUILD_DIR="$srcdir"
unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing"
STACKSIZE="-Wl,-stack,256k"

CONFIGURE_FLAGS="--host=${TARGET}
	--prefix=${prefix}
	--without-java
	--without-python
	--disable-threads
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags

	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean

	: make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
