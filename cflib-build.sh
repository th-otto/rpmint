#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=cflib
VERSION=-21
VERSIONPATCH=-20240430

. ${scriptdir}/functions.sh

PATCHES=""

unpack_archive

cd "$srcdir"
#if test "$LTO_CFLAGS" != ""; then
#	sed -i "\@^DEFINITIONS =@i OPTS += $LTO_CFLAGS" CONFIGVARS
#fi

cd "$MINT_BUILD_DIR"

export CROSS_TOOL=${TARGET}
${MAKE} $JOBS || exit 1

${MAKE} DESTDIR=${THISPKG_DIR}${sysroot} PREFIX=${TARGET_PREFIX} install || exit 1

make_archives
