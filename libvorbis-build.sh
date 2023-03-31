#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libvorbis
VERSION=-1.3.6
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/libvorbis/libvorbis-m4.dif
patches/libvorbis/libvorbis-lib64.dif
patches/libvorbis/libvorbis-CVE-2017-14160.patch
patches/libvorbis/libvorbis-CVE-2018-10393.patch
patches/libvorbis/libvorbis-CVE-2018-10392.patch
patches/libvorbis/libvorbis-staticlibs.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

unpack_archive

cd "$srcdir"

rm -f config.sub
cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --with-ogg=yes --disable-shared ${CONFIGURE_FLAGS_AMIGAOS}"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	: hack_lto_cflags
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
