#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=freetype2
VERSION=-2.8.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

srcarchive=freetype${VERSION}
srcdir="$here/freetype${VERSION}"
MINT_BUILD_DIR="$srcdir"

PATCHES="
patches/freetype2/freetype2-bugzilla-308961-cmex-workaround.patch
patches/freetype2/freetype2-mintelf-config.patch
patches/freetype2/freetype2-static-config.patch
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -std=gnu99 -D_GNU_SOURCE ${CFLAGS_AMIGAOS}"

#
# Several programs on AmigaOS compile against a bundled
# version of libpng and/or zlib, which (in most cases)
# is an older version. So we must avoid using a newer
# version which might reference functions that are not available there
#
case $TARGET in
m68k-amigaos*)
	CONFIGURE_FLAGS_AMIGAOS+=" --with-png=no"
	;;
esac

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared \
	--with-bzip2 \
	--with-png \
	--with-zlib \
	--disable-shared \
	--enable-static \
	${CONFIGURE_FLAGS_AMIGAOS}
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags
	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	rm -f ${TARGET_BINDIR#/}/freetype-config
	rmdir ${TARGET_BINDIR#/}
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
