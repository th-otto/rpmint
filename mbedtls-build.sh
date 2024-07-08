#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mbedtls
VERSION=-3.6.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/mbedtls-mint.patch
"
DISABLED_PATCHES="
"

BINFILES="
${TARGET_BINDIR#/}/*
"

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

	rm -rf build
	mkdir -p build
	cd build
	
	cmake -G "Unix Makefiles" \
		-DCMAKE_BUILD_TYPE=Release \
		-DCMAKE_INSTALL_PREFIX=${prefix} \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_C_COMPILER="${TARGET}-gcc" \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DCMAKE_TOOLCHAIN_FILE="${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake" \
		\
		-DBUILD_SHARED_LIBS=OFF \
		-DENABLE_TESTING=OFF \
		.. || exit 1

	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1

	if test "$multilibdir" != ""; then
		mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
		mv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/*.a ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
	fi
	
	make_bin_archive $CPU
done

# programs/test/selftest

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
