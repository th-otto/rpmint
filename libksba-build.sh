#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libksba
VERSION=-1.6.3
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES="
"

DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

unpack_archive

cd "$MINT_BUILD_DIR"

./autogen.sh

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" build-aux/config.sub || exit 1

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_BINDIR#/}/ksba-config
	rmdir ${TARGET_BINDIR#/}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

# create pkg-config file
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig
cat > ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig/${PACKAGENAME}.pc <<-EOF
prefix=${TARGET_PREFIX}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: ${PACKAGENAME}
Description: A X.509 Library
Version: ${VERSION#-}
URL: http://www.gnupg.org/aegypten/

Libs: -lksba
Cflags:
EOF

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
