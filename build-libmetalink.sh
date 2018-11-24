#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libmetalink
VERSION=-0.1.3
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/libmetalink-autotools.patch
patches/${PACKAGENAME}/skip-libxml2-script-crap.patch
patches/${PACKAGENAME}/mintelf-config.patch
"

BINFILES=""

unpack_archive

cd "$srcdir"

sed -i -e 's@AM_CONFIG_HEADER@AC_CONFIG_HEADERS@g' configure.ac
rm -v m4/libtool.m4 m4/lt*
rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/mintelf-config.patch"

cd "$MINT_BUILD_DIR"

export LIBXML2_CFLAGS=-I${sysroot}${TARGET_PREFIX}/include/libxml2
export LIBXML2_LIBS="-lxml2 -lz -liconv -lm"

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LIBXML2_CFLAGS"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --docdir=${TARGET_PREFIX}/share/doc/${PACKAGENAME} \
--without-libexpat \
--disable-shared \
--enable-static \
--config-cache"

create_config_cache()
{
cat <<EOF >config.cache
EOF
	append_gnulib_cache
}

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LIBXML2_LIBS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags
	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install >/dev/null
	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
