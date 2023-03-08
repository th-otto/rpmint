#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libexif
VERSION=-0.6.22
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/libexif/libexif-build-date.patch
patches/libexif/libexif-CVE-2017-7544.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
patches/libexif/libexif-CVE-2016-6328.patch
"

BINFILES="
"

unpack_archive

cd "$srcdir"

export LANG=POSIX
export LC_ALL=POSIX

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub || exit 1

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--datadir=${prefix}/share \
	--with-doc-dir=${prefix}/share/doc/${PACKAGENAME} \
	--disable-nls \
	--disable-shared"

STACKSIZE="-Wl,-stack,128k"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
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
