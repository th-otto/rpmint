#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libxml2
VERSION=-2.10.3
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/libxml2/libxml2-fix-perl.diff
patches/libxml2/libxml2-python3-unicode-errors.patch
patches/libxml2/libxml2-python3-string-null-check.patch
patches/libxml2/libxml2-make-XPATH_MAX_NODESET_LENGTH-configurable.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$srcdir"

cp ${BUILD_DIR}/patches/automake/mintelf-config.sub config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"
STACKSIZE="-Wl,-stack,128k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --docdir=${TARGET_PREFIX}/share/doc/${PACKAGENAME} ${CONFIGURE_FLAGS_AMIGAOS} \
--disable-shared \
--enable-static \
    --with-html-dir=${TARGET_PREFIX}/share/doc/libxml2/html \
    --with-fexceptions \
    --with-history \
    --without-python \
    --disable-ipv6 \
    --with-sax1 \
    --with-regexps \
    --without-threads \
    --with-reader \
    --with-http
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
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
