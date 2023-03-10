#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=jpeg
VERSION=-8d
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

PATCHES="
patches/jpeg/jpeg-mintelf-config.patch
patches/jpeg/jpeg-8d-0007-mintslb.patch 
"

srcarchive=${PACKAGENAME}src.v${VERSION#-}

unpack_archive

cd "$MINT_BUILD_DIR"



COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared \
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
	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/bin
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
