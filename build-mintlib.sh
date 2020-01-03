#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mintlib
VERSION=-0.60.1
VERSIONPATCH=-20200102

. ${scriptdir}/functions.sh

PATCHES=""

unpack_archive

cd "$MINT_BUILD_DIR"
export CROSS_TOOL=${TARGET}

# currently disabled; does not work
LTO_CFLAGS=""

#
# ugly hack until makefiles have been ajusted
#
sed -i "\@^# This is where include@i prefix := ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" configvars
${MAKE} $JOBS || exit 1

${MAKE} prefix=${THISPKG_DIR}${sysroot}${TARGET_PREFIX} install || exit 1

cd "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" || exit 1

find . -name 00README | xargs rm -f
find . -name COPYING | xargs rm -f
find . -name COPYING.LIB | xargs rm -f
find . -name COPYMINT | xargs rm -f
find . -name BINFILES | xargs rm -f
find . -name MISCFILES | xargs rm -f
find . -name SRCFILES | xargs rm -f
find . -name EXTRAFILES | xargs rm -f
find . -name Makefile | xargs rm -f
find . -name clean-include | xargs rm -f

make_archives
