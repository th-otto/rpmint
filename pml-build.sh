#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=pml
VERSION=-2.03
VERSIONPATCH=-20171006

. ${scriptdir}/functions.sh

MINT_BUILD_DIR="$srcdir/pmlsrc"

# Note: when compiling with gcc-2.95, activate the 2nd patch below.
# The first is only included for reference, and already applied in the archive
DISABLED_PATCHES="
patches/pml/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.patch
patches/pml/${PACKAGENAME}-gcc2.patch
"

unpack_archive

# currently disabled; does not work
LTO_CFLAGS=""

cd "$srcdir"
#if test "$LTO_CFLAGS" != ""; then
#	sed -i "\@^CP    =@i CFLAGS += ${LTO_CFLAGS}" CONFIGVARS
#fi
if test "$ELF_CFLAGS" != ""; then
	sed -i "\@^CP    =@i CFLAGS += ${ELF_CFLAGS}" CONFIGVARS
fi

cd "$MINT_BUILD_DIR"
export CROSS_TOOL=${TARGET}

${MAKE} $JOBS || exit 1

cd "$MINT_BUILD_DIR"
${MAKE} DESTDIR="${THISPKG_DIR}" install || exit 1

# gcc2 does not know about -sysroot
if ! test -d ${THISPKG_DIR}/usr/${TARGET}/sys-root; then
	mv ${THISPKG_DIR}/usr ${THISPKG_DIR}/uusr
	mkdir -p ${THISPKG_DIR}/usr/${TARGET}/sys-root/usr
	mv ${THISPKG_DIR}/uusr/* ${THISPKG_DIR}/usr/${TARGET}/sys-root/usr
	rmdir ${THISPKG_DIR}/uusr
fi

make_archives
