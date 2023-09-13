#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=cflib
VERSION=-21
VERSIONPATCH=-20230912

. ${scriptdir}/functions.sh

MINT_BUILD_DIR="$srcdir/cflib"

PATCHES=""

unpack_archive

# this Makefiles are not yet ready for parallel makes
JOBS=-j1

cd "$srcdir"
#if test "$LTO_CFLAGS" != ""; then
#	sed -i "\@^DEFINITIONS =@i OPTS += $LTO_CFLAGS" CONFIGVARS
#fi

#
# ugly hack until makefiles have been ajusted
#
cd "$srcdir"
sed -i "\@^DEFINITIONS =@i PREFIX := ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" CONFIGVARS

cd "$MINT_BUILD_DIR"

export CROSS_TOOL=${TARGET}
${MAKE} $JOBS || exit 1

mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/lib
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/lib/mshort
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/lib/m68020-60
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/lib/m68020-60/mshort
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/lib/m5475
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/lib/m5475/mshort
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/stguide
${MAKE} PREFIX=${THISPKG_DIR}${sysroot}${TARGET_PREFIX} install || exit 1

make_archives
