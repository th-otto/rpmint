#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=vorbis-tools
VERSION=-1.4.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/vorbis-tools/vorbis-tools-warning-fixes.diff
patches/vorbis-tools/vorbis-tools-cflags.diff
patches/vorbis-tools/vorbis-tools-vcut-fix-segfault.diff
patches/vorbis-tools/vorbis-tools-r19117-CVE-2014-9640.patch
patches/vorbis-tools/vorbis-tools-oggenc-CVE-2014-9639.patch
patches/vorbis-tools/vorbis-tools-oggenc-Fix-large-alloca.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"


unpack_archive

cd "$srcdir"

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-nls"

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
