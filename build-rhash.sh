#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=rhash
VERSION=-1.3.5
VERSIONPATCH=
major_version=5.3

srcarchive=${PACKAGENAME}${VERSION}-src

. ${scriptdir}/functions.sh

PATCHES="
patches/rhash/rhash-1.3.0-shared.patch
"

BINFILES="
${TARGET_SYSCONFDIR#/}
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

srcdir="$here/RHash${VERSION}"
MINT_BUILD_DIR="$srcdir"
unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
STACKSIZE="-Wl,-stack,256k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	# Don't run parallel make $JOBS -- it doesn't work.
	${MAKE} \
		CC="${TARGET}-gcc" \
		AR="${ar}" \
		RANLIB=${ranlib} \
		OPTFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -D_GNU_SOURCE $LTO_CFLAGS" \
		OPTLDFLAGS="$CPU_CFLAGS $LTO_CFLAGS ${STACKSIZE}" \
		lib-static all || exit 1

	${MAKE} \
		PREFIX=${prefix} LIBDIR='${PREFIX}/lib'$multilibdir DESTDIR="${THISPKG_DIR}${sysroot}" \
		install install-lib-static || exit 1
	${MAKE} -C librhash \
		PREFIX=${prefix} DESTDIR="${THISPKG_DIR}${sysroot}" \
		install-headers || exit 1
	
	${MAKE} clean
	make_bin_archive $CPU
	
	test $CPU = 000 || rm -f "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/man/"*/*
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
