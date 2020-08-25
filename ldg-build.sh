#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ldg
VERSION=-svn-20171014
VERSIONPATCH=

. ${scriptdir}/functions.sh

MINT_BUILD_DIR="$srcdir/src/devel"

PATCHES="patches/ldg/ldg-cross.patch"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-W -Wall -O2 -fomit-frame-pointer -I../../include -I.. -I. $LTO_CFLAGS"

${MAKE} -f gcc.mak CROSS_PREFIX=${TARGET}- CFLAGS="-m68020-60 $COMMON_CFLAGS"
mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/m68020-60"
cp -a ../../lib/gcc/libldg.a "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/m68020-60"
${MAKE} -f gcc.mak clean

${MAKE} -f gcc.mak CROSS_PREFIX=${TARGET}- CFLAGS="-mcpu=5475 $COMMON_CFLAGS"
mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/m5475"
cp -a ../../lib/gcc/libldg.a "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/m5475"
${MAKE} -f gcc.mak clean

${MAKE} -f gcc.mak CROSS_PREFIX=${TARGET}- CFLAGS="-m68000 $COMMON_CFLAGS"
mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/m5475"
cp -a ../../lib/gcc/libldg.a "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}"
${MAKE} -f gcc.mak clean

mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include"
cp -a ../../include/ldg.h "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include"

make_archives
