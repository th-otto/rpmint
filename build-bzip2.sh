#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=bzip2
VERSION=-1.0.6
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/bzip2/bzip2-1.0.6-patch-0001-configure.patch
patches/bzip2/bzip2-1.0.6-patch-0002-cygming.patch
patches/bzip2/bzip2-1.0.6-patch-0003-debian-bzgrep.patch
patches/bzip2/bzip2-1.0.6-patch-0004-unsafe-strcpy.patch
patches/bzip2/bzip2-1.0.6-patch-0005-progress.patch
patches/bzip2/bzip2-1.0.6-patch-0006-mint.patch
"

BINFILES="
${TARGET_BINDIR}/bunzip2
${TARGET_BINDIR}/bzcat
${TARGET_BINDIR}/bzcmp
${TARGET_BINDIR}/bzdiff
${TARGET_BINDIR}/bzegrep
${TARGET_BINDIR}/bzfgrep
${TARGET_BINDIR}/bzgrep
${TARGET_BINDIR}/bzip2
${TARGET_BINDIR}/bzip2recover
${TARGET_BINDIR}/bzless
${TARGET_BINDIR}/bzmore
${TARGET_MANDIR}/man1/bunzip2.1.gz
${TARGET_MANDIR}/man1/bzcat.1.gz
${TARGET_MANDIR}/man1/bzcmp.1.gz
${TARGET_MANDIR}/man1/bzdiff.1.gz
${TARGET_MANDIR}/man1/bzegrep.1.gz
${TARGET_MANDIR}/man1/bzfgrep.1.gz
${TARGET_MANDIR}/man1/bzgrep.1.gz
${TARGET_MANDIR}/man1/bzip2.1.gz
${TARGET_MANDIR}/man1/bzless.1.gz
${TARGET_MANDIR}/man1/bzmore.1.gz
"

unpack_archive

cd "$MINT_BUILD_DIR"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

CFLAGS="-m68020-60 $COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m68020-60'
${MAKE} $JOBS || exit 1
${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
${MAKE} distclean
make_bin_archive 020

CFLAGS="-mcpu=5475 $COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib/m5475'
${MAKE} $JOBS || exit 1
${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
${MAKE} distclean
make_bin_archive v4e

CFLAGS="$COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS}
${MAKE} $JOBS || exit 1
${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
#${MAKE} distclean
make_bin_archive 000

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
