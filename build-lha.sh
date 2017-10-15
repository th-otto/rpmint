#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=lha
VERSION=-1.14i-ac20050924p1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/lha/mintelf-config.patch"

BINFILES="
${TARGET_BINDIR#/}/lha
${TARGET_MANDIR#/}/mann/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --mandir=${prefix}/share/man"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in 020 v4e 000; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval libdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="${CPU_CFLAGS} $COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$libdir
	hack_lto_cflags
	make $JOBS || exit 1
	make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	make distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
