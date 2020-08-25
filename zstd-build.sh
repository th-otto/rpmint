#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zstd
VERSION=-1.4.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/zstd-compiler.h.patch
"
DISABLED_PATCHES="
patches/${PACKAGENAME}/zstd-pzstd.1.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$srcdir"

# conflicts with mintlib header file of the same name
mv lib/common/compiler.h lib/common/zcompiler.h

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"
case $TARGET in
m68k-atari-mint*)
	STACKSIZE="-Wl,-stack,256k"
	;;
m68k-amigaos*)
	;;
esac

export prefix=${prefix}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	export CC=${TARGET}-gcc
	export AR=${TARGET}-ar
	export CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	export LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}"
	export libdir="${prefix}/lib$multilibdir"

	${MAKE} $JOBS -C lib libzstd.a || exit 1
	${MAKE} $JOBS -C programs || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" -C lib install-static install-pc install-includes || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" -C programs install || exit 1
	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
