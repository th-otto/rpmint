#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ldg
VERSION=-20171014
VERSIONPATCH=

. ${scriptdir}/functions.sh

MINT_BUILD_DIR="$srcdir/src/devel"

PATCHES="patches/ldg/ldg-cross.patch"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-W -Wall -O2 -fomit-frame-pointer -I../../include -I.. -I. ${ELF_CFLAGS}"

WITH_FASTCALL=`if $gcc -mfastcall -E - < /dev/null >/dev/null 2>&1; then echo true; else echo false; fi`

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	if $WITH_FASTCALL; then
		${MAKE} -f gcc.mak CROSS_PREFIX=${TARGET}- CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall"
		mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir/mfastcall"
		cp -a ../../lib/gcc/libldg.a "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir/mfastcall"
		${MAKE} -f gcc.mak clean
	fi

	${MAKE} -f gcc.mak CROSS_PREFIX=${TARGET}- CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir"
	cp -a ../../lib/gcc/libldg.a "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir"
	${MAKE} -f gcc.mak clean
done

mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include"
cp -a ../../include/ldg.h "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include"

make_archives
