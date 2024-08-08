#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mintlib
VERSION=-0.60.1
VERSIONPATCH=-20240718

. ${scriptdir}/functions.sh

PATCHES=""
BINFILES="
sbin/tzinit
${TARGET_PREFIX#/}/sbin/tzselect
${TARGET_PREFIX#/}/sbin/zic
${TARGET_PREFIX#/}/sbin/zdump
${TARGET_PREFIX#/}/share/zoneinfo
"

unpack_archive

cd "$MINT_BUILD_DIR"
export CROSS_TOOL=${TARGET}

# currently disabled; does not work
LTO_CFLAGS=""

${MAKE} $JOBS || exit 1

${MAKE} DESTDIR=${THISPKG_DIR}${sysroot} install || exit 1

cd "$MINT_BUILD_DIR"
rm -f tz/*.o
make type=m68020 -C tz DESTDIR=${THISPKG_DIR}${sysroot} install
make_bin_archive 020

cd "$MINT_BUILD_DIR"
rm -f tz/*.o
make type=coldfire -C tz DESTDIR=${THISPKG_DIR}${sysroot} install
make_bin_archive v4e

cd "$MINT_BUILD_DIR"
rm -f tz/*.o
make type=m68000 -C tz DESTDIR=${THISPKG_DIR}${sysroot} install
make_bin_archive 000

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

NO_STRIP=yes
make_archives
