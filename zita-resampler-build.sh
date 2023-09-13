#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=zita-resampler
VERSION=-1.8.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/zita-resampler-mint.patch
"
BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing -ffast-math ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	cd "$MINT_BUILD_DIR/source"

	${MAKE} clean
	${MAKE} \
	   CXX=${TARGET}-g++ \
	   CC=${TARGET}-gcc \
	   AR=${TARGET}-ar \
	   RANLIB=${TARGET}-ranlib \
	   CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	   PREFIX=${sysroot}/usr \
	   LIBDIR='$(PREFIX)/lib'$multilibdir \
	   DESTDIR=${THISPKG_DIR} \
	   $JOBS install || exit 1
	
	cd "$MINT_BUILD_DIR/apps"

	${MAKE} clean
	${MAKE} \
	   CXX=${TARGET}-g++ \
	   CC=${TARGET}-gcc \
	   AR=${TARGET}-ar \
	   RANLIB=${TARGET}-ranlib \
	   CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	   PREFIX=${sysroot}/usr \
	   LIBDIR='$(PREFIX)/lib'$multilibdir \
	   MANDIR='$(PREFIX)/share/man/man1' \
	   DESTDIR=${THISPKG_DIR} \
	   $JOBS install || exit 1
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
