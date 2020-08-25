#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=popt
VERSION=-1.16
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/popt/popt-libc-updates.patch
patches/popt/popt-alignment-checks.patch
patches/popt/popt-glibc-clashes.patch
patches/popt/popt-mintelf-config.patch
"

BINFILES=""

unpack_archive

cd "$MINT_BUILD_DIR"

autoreconf -fi
# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/popt/popt-mintelf-config.patch"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} \
		--libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
