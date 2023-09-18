#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=physfs
VERSION=-3.2.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/physfs/physfs-mint.patch
"
DISABLED_PATCHES="
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"
CMAKE_SYSTEM_NAME="${TARGET##*-}"

export prefix=${prefix}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	cmake \
		-DCMAKE_BUILD_TYPE=Release \
		-DCMAKE_INSTALL_PREFIX=${prefix} \
		-DPHYSFS_BUILD_STATIC=TRUE \
		-DPHYSFS_BUILD_SHARED=FALSE \
		-DPHYSFS_BUILD_TEST=FALSE \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_C_COMPILER="${TARGET}-gcc" \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DPTHREAD_LIBRARY="" \
		-DCMAKE_TOOLCHAIN_FILE="${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake" \
		.
	
	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	if test "$multilibdir" != ""; then
		mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
		mv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/*.a ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
	fi
	
	${MAKE} clean >/dev/null
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
