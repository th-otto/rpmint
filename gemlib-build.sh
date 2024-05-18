#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gemlib
VERSION=-0.44.0
VERSIONPATCH=-20240425

. ${scriptdir}/functions.sh

MINT_BUILD_DIR="$srcdir"

PATCHES=""

unpack_archive

# this Makefiles are not yet ready for parallel makes
#JOBS=-j1

cd "$srcdir"
if test "$LTO_CFLAGS" != ""; then
	: sed -i "\@^DEFINITIONS =@i OPTS += $LTO_CFLAGS" CONFIGVARS
fi

#
# ugly hack until makefiles have been ajusted
#
cd "$srcdir"
sed -i "\@^DEFINITIONS =@i PREFIX := ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" CONFIGVARS

cd "$MINT_BUILD_DIR"

export CROSS_TOOL=${TARGET}
${MAKE} $JOBS || exit 1

${MAKE} PREFIX=${THISPKG_DIR}${sysroot}${TARGET_PREFIX} install || exit 1

make_archives
