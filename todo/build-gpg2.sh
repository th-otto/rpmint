#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gpg2
VERSION=-2.2.5
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES=""

PATCHES="
patches/gpg2/gnupg-2.0.9-langinfo.patch
patches/gpg2/gnupg-2.0.18-files-are-digests.patch
patches/gpg2/gnupg-dont-fail-with-seahorse-agent.patch
patches/gpg2/gnupg-set_umask_before_open_outfile.patch
patches/gpg2/gnupg-detect_FIPS_mode.patch
patches/gpg2/gnupg-add_legacy_FIPS_mode_option.patch
patches/gpg2/mint.patch
patches/gpg2/mintelf-config.patch
"

srcarchive=gnupg-${VERSION#-}
srcdir="$here/$srcarchive"
MINT_BUILD_DIR="$srcdir"

unpack_archive

cd "$MINT_BUILD_DIR"

./autogen.sh

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
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
