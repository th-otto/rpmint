#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libarchive
VERSION=-3.3.2
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/libarchive/fix-CVE-2017-14166.patch
patches/libarchive/mintelf-config.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

autoreconf -fi
# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/libarchive/mintelf-config.patch"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--docdir=${TARGET_PREFIX}/share/doc/${PACKAGENAME} \
	--disable-shared \
	--enable-static \
	--enable-bsdcpio \
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags

	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
