#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=graphite2
VERSION=-1.3.14
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
"
DISABLED_PATCHES="
patches/graphite2/graphite2-1.2.0-cmakepath.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
"

srcdir="$here/graphite${VERSION}"
MINT_BUILD_DIR="$srcdir"
unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"
CMAKE_SYSTEM_NAME="${TARGET##*-}"


export prefix=${prefix}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	mkdir -p build/${TARGET}
	cd build/${TARGET}
	
	cmake -G "Unix Makefiles" \
		-DCMAKE_BUILD_TYPE=Release \
		-DBUILD_SHARED_LIBS=OFF \
		-DCMAKE_INSTALL_PREFIX=${prefix} \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_C_COMPILER="${TARGET}-gcc" \
		-DCMAKE_CXX_COMPILER="${TARGET}-g++" \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DCMAKE_CXX_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DCMAKE_TOOLCHAIN_FILE="${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake" \
		../..

	${MAKE} V=1 $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1

	if test "$multilibdir" != ""; then
		mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
		mv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/*.a ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
	fi
	
	${MAKE} clean > /dev/null
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
