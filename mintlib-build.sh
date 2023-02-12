#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mintlib
VERSION=-0.60.1
VERSIONPATCH=-20230212

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

find . \( -name 00README \
	-o -name COPYING \
	-o -name COPYING.LIB \
	-o -name COPYMINT \
	-o -name BINFILES \
	-o -name MISCFILES \
	-o -name SRCFILES \
	-o -name EXTRAFILES \
	-o -name Makefile \
	-o -name clean-include \) -delete -printf "rm %%p\n"

make_archives
