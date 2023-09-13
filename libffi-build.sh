#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libffi
VERSION=-3.2.1.git
VERSIONPATCH=

# https://github.com/libffi/libffi/archive/0081378017c33a4b9b6fbf20efabdd9959d6a48d.tar.gz

. ${scriptdir}/functions.sh


BINFILES=""

DISABLE_PATCHES="
patches/automake/mintelf-config.sub
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

./autogen.sh

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub || exit 1

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

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
	: hack_lto_cflags

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
