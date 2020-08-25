#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libxml2
VERSION=-2.9.6
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/libxml2/libxml2-fix-perl.diff
patches/libxml2/libxml2-mintelf-config.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --docdir=${TARGET_PREFIX}/share/doc/${PACKAGENAME} \
--disable-shared \
--enable-static \
    --with-html-dir=${TARGET_PREFIX}/share/doc/libxml2/html \
    --with-fexceptions \
    --with-history \
    --without-python \
    --disable-ipv6 \
    --with-sax1 \
    --with-regexps \
    --with-threads \
    --with-reader \
    --with-http
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags
	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	rm -f ${TARGET_BINDIR#/}/xml2-config
	find ${TARGET_LIBDIR#/} -type f -name "xml2Conf.sh" -delete -printf "rm %p\n"
	rm -rf ${TARGET_LIBDIR#/}/*/cmake
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
