#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=giflib
VERSION=-5.1.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/giflib/giflib-visibility.patch
patches/giflib/giflib-automake-1_13.patch
patches/giflib/giflib-CVE-2016-3977.patch
patches/giflib/giflib-fix-autoconf11.patch
patches/giflib/giflib-mintelf-config.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$srcdir"

export LANG=POSIX
export LC_ALL=POSIX
autoreconf -fiv
# patch it again in case it was replaced by autoreconf
patch -p1 -i ${BUILD_DIR}/patches/giflib/giflib-mintelf-config.patch || :

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--datadir=${prefix}/share \
	--disable-nls \
	--disable-shared"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	STACKSIZE="-Wl,-stack,128k"
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
