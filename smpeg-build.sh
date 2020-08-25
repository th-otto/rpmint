#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=smpeg
VERSION=-0.4.5
VERSIONPATCH=

. ${scriptdir}/functions.sh

DISABLED_PATCHES="
patches/${PACKAGENAME}/smpeg-mintelf-config.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share/man/*
"


unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I acinclude || exit 1
autoconf || exit 1
automake --copy --add-missing
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/smpeg-mintelf-config.patch"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/smpeg*-config
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
