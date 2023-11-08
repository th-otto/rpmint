#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=x265
VERSION=-3.5
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/x265/x265-arm.patch
patches/x265/x265-fix_enable512.patch
patches/x265/x265-mint.patch
"
EXTRA_DIST="
"

BINFILES="
${TARGET_BINDIR#/}/*
"

srcarchive="${PACKAGENAME}_${VERSION#-}"
srcdir="${here}/${PACKAGENAME}_${VERSION#-}"
MINT_BUILD_DIR="$srcdir"
unpack_archive

cd "$srcdir"

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
		-Wno-dev \
		-DCMAKE_BUILD_TYPE=Release \
		-DCMAKE_INSTALL_PREFIX=${prefix} \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_C_COMPILER="${TARGET}-gcc" \
		-DCMAKE_CXX_COMPILER="${TARGET}-g++" \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DCMAKE_CXX_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DENABLE_PIC=OFF \
		-DENABLE_CLI=ON \
		-DCMAKE_TOOLCHAIN_FILE="${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake" \
		../../source
	
	# parallel does not work? creates truncated objects in libx265.a
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	if test "$multilibdir" != ""; then
		mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
		mv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/*.a ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
	fi
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
