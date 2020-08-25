#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libsolv
VERSION=-0.6.33
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/libsolv/libsolv-mint.patch
patches/libsolv/libsolv-lto.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share/man
${TARGET_PREFIX#/}/share/cmake/Modules
"

CMAKE_SYSTEM_NAME="${TARGET##*-}"

if ! test -f "${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake"; then
	echo "${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake missing" >&2
	echo "please install the CMake package first" >&2
	exit 1
fi

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
STACKSIZE="-Wl,--stack,512k"

gcc=`which ${TARGET}-gcc`
gxx=`which ${TARGET}-g++`

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --docdir=${TARGET_PREFIX}/share/doc/${PACKAGENAME}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

mkdir cmake/modules/Platform
sed -e 's,CMAKE_C_COMPILER [^)]*),CMAKE_C_COMPILER '"$gcc"'),' \
    -e 's,CMAKE_CXX_COMPILER [^)]*),CMAKE_CXX_COMPILER '"$gxx"'),' \
	${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake > cmake/modules/Platform/${CMAKE_SYSTEM_NAME}.cmake

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	find . -type f -name CMakeCache.txt -delete
	find . -type d -name CMakeFiles -print0 | xargs -0 rm -rf

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	
	export CC="$gcc"
	export CXX="$gxx"
	
	cmake \
		-DCMAKE_INSTALL_PREFIX=${prefix} \
		-DCMAKE_BUILD_TYPE=RelWithDebInfo \
		-DSUSE=1 \
		-DENABLE_SUSEREPO=1 \
		-DENABLE_APPDATA=1 \
		-DENABLE_HELIXREPO=1 \
		-DENABLE_COMPS=1 \
		-DUSE_VENDORDIRS=1 \
		-DCMAKE_SKIP_RPATH=1 \
		-DWITH_LIBXML2=1 \
		-DENABLE_STATIC=1 \
		-DDISABLE_SHARED=1 \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS" \
		-DCMAKE_CXX_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS" \
		-DCMAKE_EXE_LINKER_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS $STACKSIZE" \
		.
	
	${MAKE} ${JOBS} || exit 1

	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} DESTDIR="${buildroot}" install

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
