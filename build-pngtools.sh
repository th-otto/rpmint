#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=pngtools
VERSION=-0.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/pngtools-0.4.patch
"

DISABLED_PATCHES="
patches/${PACKAGENAME}/mintelf-config.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4
aclocal || exit 1
autoconf || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/mintelf-config.patch"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--disable-nls"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	STACKSIZE="-Wl,-stack,160k"
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null
	rm -fv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	rm -fv ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include/gnumake.h
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
