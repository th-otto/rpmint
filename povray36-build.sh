#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=povray
VERSION=-3.6.1
VERSIONPATCH=-fdlibm

. ${scriptdir}/functions.sh

PATCHES="
patches/povray/povray36-autoconf.patch
"
DISABLED_PATCHES="
patches/${PACKAGENAME}/povray36-mintelf-config.patch
"

BINFILES="
etc/povray
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share/*
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

( cd libraries/png
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --foreign --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig
) || exit 1

( cd libraries/zlib
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --foreign --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig
) || exit 1

# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/povray36-mintelf-config.patch"

cp -a config/config.sub libraries/zlib/config.sub
cp -a config/config.sub libraries/png/config.sub
cp -a config/config.sub libraries/jpeg/config.sub
cp -a config/config.sub libraries/tiff/config.sub

# hack jpeg library configure script
sed -i "s|export CFLAGS|CC=${TARGET}-gcc; AR=$ar; RANLIB=$ranlib; export CFLAGS CC AR RANLIB|" "${srcdir}/libraries/jpeg/configure.gnu"
sed -i "s|AR= ar rc|AR = $ar rcs|" "${srcdir}/libraries/jpeg/makefile.cfg"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS"
STACKSIZE="-Wl,-stack,256k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --sysconfdir=/etc --disable-lib-checks"

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
    COMPILED_BY="Thorsten Otto for MiNT" \
    CC="${TARGET}-gcc" \
    AR="$ar" \
    RANLIB="$ranlib" \
	--libdir="${prefix}/lib${multilibdir}"

	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
