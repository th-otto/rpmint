#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=unrar
VERSION=-5.5.8
VERSIONPATCH=

. ${scriptdir}/functions.sh

srcdir="$here/${PACKAGENAME}"
MINT_BUILD_DIR="$srcdir"
srcarchive=${PACKAGENAME}src${VERSION}

PATCHES="patches/unrar/wprintf.patch"

BINFILES="
${TARGET_BINDIR#/}/unrar
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --mandir=${prefix}/share/man"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

cd "${srcdir}"
sed -i 's:READBINARY   "r":READBINARY   "rb":g' os.hpp
sed -i 's:READTEXT     "r":READTEXT     "rt":g' os.hpp
sed -i 's:UPDATEBINARY "r+":UPDATEBINARY "r+b":g' os.hpp
sed -i 's:CREATEBINARY "w+":CREATEBINARY "w+b":g' os.hpp
sed -i 's:APPENDTEXT   "a":APPENDTEXT   "at":g' os.hpp
sed -i 's:#define RAR_SMP:#undef RAR_SMP:g' os.hpp

for CPU in 020 v4e 000; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval libdir=\${CPU_LIBDIR_$CPU}
	${MAKE} $JOBS CXX=${TARGET}-g++ CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" STRIP=${TARGET}-strip AR=${TARGET}-ar LDFLAGS= LIBFLAGS= DEFINES= || exit 1
	mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_BINDIR}"
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" install
	${MAKE} clean
	make_bin_archive $CPU
done

# TODO: add stack-size 128k

move_prefix
configured_prefix="${prefix}"

make_archives
