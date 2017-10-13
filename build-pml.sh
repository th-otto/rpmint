#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=pml
VERSION=-2.03
VERSIONPATCH=-20171006

. ${scriptdir}/functions.sh

MINT_BUILD_DIR="$srcdir/pmlsrc"

PATCHES="
patches/pml/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.patch
"

unpack_archive

# currently disabled; does not work
LTO_CFLAGS=""

cd "$srcdir"
if test "$LTO_CFLAGS" != ""; then
	sed -i "\@^CP    =@i CFLAGS += ${LTO_CFLAGS}" CONFIGVARS
fi

cd "$MINT_BUILD_DIR"
export CROSS_TOOL=${TARGET}

make $JOBS || exit 1

cd "$MINT_BUILD_DIR"
make DESTDIR="${THISPKG_DIR}" install || exit 1
	
make_archives
