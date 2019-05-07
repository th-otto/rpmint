#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=rhash
VERSION=-1.3.8
VERSIONPATCH=
major_version=5.3

srcarchive=${PACKAGENAME}${VERSION}

. ${scriptdir}/functions.sh

PATCHES="
patches/rhash/rhash-1.3.8-shared.patch
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

CONFIGURE_FLAGS="--prefix=${prefix} --disable-lib-shared --enable-lib-static --enable-static --sysconfdir=/etc"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CC="${TARGET}-gcc" \
	AR="${ar}" \
	RANLIB=${ranlib} \
	OPTFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -D_GNU_SOURCE $LTO_CFLAGS" \
	OPTLDFLAGS="$CPU_CFLAGS $LTO_CFLAGS ${STACKSIZE}" \
		./configure $CONFIGURE_FLAGS || exit 1

	# Don't run parallel make $JOBS -- it doesn't work.
	${MAKE} \
		CC="${TARGET}-gcc" \
		AR="${ar}" \
		RANLIB=${ranlib} \
		OPTFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -D_GNU_SOURCE $LTO_CFLAGS" \
		OPTLDFLAGS="$CPU_CFLAGS $LTO_CFLAGS ${STACKSIZE}" \
		lib-static all || exit 1

	${MAKE} \
		PREFIX=${prefix} LIBDIR="${THISPKG_DIR}${sysroot}${prefix}/lib${multilibdir}" DESTDIR="${THISPKG_DIR}${sysroot}" \
		install install-lib-static install-man install-conf install-pkg-config || exit 1
	${MAKE} -C librhash \
		PREFIX=${prefix} DESTDIR="${THISPKG_DIR}${sysroot}" \
		install-lib-headers || exit 1
	
	${MAKE} clean
	make_bin_archive $CPU
	
	test $CPU = 000 || rm -f "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/man/"*/*
done

# create pkg-config file
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig
cat > ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig/librhash.pc <<-EOF
prefix=${TARGET_PREFIX}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: librhash
Description: RHash is a utility for computing and verifying hash sums of files
Version: ${VERSION#-}
URL: http://rhash.anz.ru/

Libs: -lrhash
Cflags:
EOF

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
