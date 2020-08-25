#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=tree
VERSION=-1.8.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/tree-makefile.patch
patches/${PACKAGENAME}/tree-mint.patch
"

DISABLED_PATCHES="
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--disable-nls \
	--disable-shared \
	--localstatedir=/var/lib \
	--config-cache"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	STACKSIZE="-Wl,-stack,128k"

	${MAKE} CC=${TARGET}-gcc CPU_CFLAGS="${CPU_CFLAGS}" || exit 1

	${MAKE} prefix="${THISPKG_DIR}${sysroot}/${TARGET_PREFIX}" MANDIR="${THISPKG_DIR}${sysroot}/${TARGET_MANDIR}/man1" install
	
	${MAKE} clean >/dev/null

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
