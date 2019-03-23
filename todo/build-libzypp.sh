#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libzypp
VERSION=-17.2.2
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/zypp
${TARGET_SYSCONFDIR#/}
${TARGET_PREFIX#/}/share/doc
${TARGET_PREFIX#/}/share/man
${TARGET_PREFIX#/}/share/locale
${TARGET_PREFIX#/}/share/zypp
var
"

CMAKE_SYSTEM_NAME="${TARGET##*-}"

if ! test -f "${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake"; then
	echo "${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake missing" >&2
	echo "please install the CMake package first" >&2
	exit 1
fi

cmake -DCMAKE_INSTALL_PREFIX=/usr -DDOC_INSTALL_DIR=/usr/share/doc/packages/libzypp -DCMAKE_BUILD_TYPE=Release -DCMAKE_SKIP_RPATH=1 -DDISABLE_LIBPROXY=ON -DENABLE_USE_THREADS=OFF -DCMAKE_SYSTEM_NAME=mint
exit 0

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

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	
	rm -rf build
	mkdir build
	cd build || exit 1

	export CC="$gcc"
	export CXX="$gxx"
	
	cmake \
		-DCMAKE_INSTALL_PREFIX=${prefix} \
		-DDOC_INSTALL_DIR=${prefix}/share/doc/packages/${PACKAGENAME} \
		-DCMAKE_BUILD_TYPE=Release \
		-DCMAKE_SKIP_RPATH=1 \
		-DDISABLE_LIBPROXY=ON \
		-DENABLE_USE_THREADS=OFF \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS" \
		-DCMAKE_CXX_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS" \
		-DCMAKE_EXE_LINKER_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS $STACKSIZE" \
		..
	
# sed -i 's/docbook2x-man/docbook-to-man/' doc/doc.mk

	${MAKE} ${JOBS} || exit 1

	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} DESTDIR="${buildroot}" install

	mkdir -p ${buildroot}${TARGET_SYSCONFDIR}/zypp/services.d
	mkdir -p ${buildroot}${TARGET_SYSCONFDIR}/zypp/systemCheck.d
	mkdir -p ${buildroot}${TARGET_SYSCONFDIR}/zypp/vars.d
	mkdir -p ${buildroot}${TARGET_SYSCONFDIR}/zypp/vendors.d
	mkdir -p ${buildroot}${TARGET_SYSCONFDIR}/zypp/multiversion.d
	mkdir -p ${buildroot}${TARGET_SYSCONFDIR}/zypp/credentials.d
	mkdir -p ${buildroot}${TARGET_PREFIX}/lib/zypp/plugins/appdata
	mkdir -p ${buildroot}${TARGET_PREFIX}/lib/zypp/plugins/commit
	mkdir -p ${buildroot}${TARGET_PREFIX}/lib/zypp/plugins/services
	mkdir -p ${buildroot}${TARGET_PREFIX}/lib/zypp/plugins/system
	mkdir -p ${buildroot}${TARGET_PREFIX}/lib/zypp/plugins/urlresolver
	mkdir -p ${buildroot}/var/lib/zypp
	mkdir -p ${buildroot}/var/log/zypp
	mkdir -p ${buildroot}/var/cache/zypp

	if test "$multilibdir" != ""; then
		mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
		mv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/*.a ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir
	fi
	
	cd ..
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
