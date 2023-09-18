#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=cmake
VERSION=-3.10.2
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/cmake/cmake-fix-ruby-test.patch
patches/cmake/cmake-mint-rules.patch
patches/cmake/cmake-form.patch
patches/cmake/cmake-system-libs.patch
patches/cmake/cmake-3.10.1_boost-1.66.patch
patches/cmake/cmake-feature-python-interp-search-order.patch
patches/cmake/cmake-c17-default.patch
patches/cmake/cmake-0001-Cannot-use-C-reference-in-C-code.patch
patches/cmake/cmake-0001-No-SA_SIGINFO.patch
patches/cmake/cmake-mint-c++-math.patch
patches/cmake/cmake-no-isystem.patch
patches/cmake/cmake-replace-find_package-with-pkgconfig.patch
"
POST_INSTALL_SCRIPTS="
patches/cmake/cmake.macros
patches/cmake/cmake.attr
patches/cmake/cmake.prov
patches/cmake/cmake-mint.cmake
patches/cmake/cmake-mint-cross.cmake
patches/cmake/cmake-mintelf.cmake
patches/cmake/cmake-mintelf-cross.cmake
"

BINFILES="
${TARGET_SYSCONFDIR}/rpm
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/${PACKAGENAME}
${TARGET_LIBDIR#/}/rpm
${TARGET_PREFIX#/}/share/doc/${PACKAGENAME}
${TARGET_PREFIX#/}/share/aclocal
${TARGET_PREFIX#/}/share/${PACKAGENAME}
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"
STACKSIZE="-Wl,--stack,512k"

CMAKE_SYSTEM_NAME="${TARGET##*-}"

( cd "$MINT_BUILD_DIR/Modules/Platform/"; $LN_S -f ${CMAKE_SYSTEM_NAME}.cmake "${TARGET}.cmake" )

gcc=`which ${TARGET}-gcc`
gxx=`which ${TARGET}-g++`
# This is not autotools configure
CONFIGURE_FLAGS="
	--prefix=${prefix} \
	--datadir=/share/${PACKAGENAME} \
	--docdir=/share/doc/${PACKAGENAME} \
	--mandir=/share/man \
	--system-libs \
	--no-system-jsoncpp \
	--verbose \
	--no-qt-gui \
	${JOBS/-j/--parallel=} \
	-- \
	-DCMAKE_USE_SYSTEM_LIBRARY_LIBUV=ON \
	-DCMAKE_TOOLCHAIN_FILE=$MINT_BUILD_DIR/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake \
"

#
# For some obscure reason, bootstrapping seems
# to require absolute paths for the compiler
#
sed -e 's,CMAKE_C_COMPILER [^)]*),CMAKE_C_COMPILER '"$gcc"'),' \
    -e 's,CMAKE_CXX_COMPILER [^)]*),CMAKE_CXX_COMPILER '"$gxx"'),' \
    "$BUILD_DIR/patches/cmake/cmake-${CMAKE_SYSTEM_NAME}-cross.cmake" > "$MINT_BUILD_DIR/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	./configure ${CONFIGURE_FLAGS} \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DCMAKE_CXX_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $CXX_EXCEPTIONS" \
		-DCMAKE_EXE_LINKER_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $CXX_EXCEPTIONS $STACKSIZE"

	${MAKE} ${JOBS} || exit 1
	
	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} DESTDIR="${buildroot}" install
	mkdir -p "${buildroot}${TARGET_LIBDIR}/${PACKAGENAME}"
	find "${buildroot}${TARGET_PREFIX}/share/${PACKAGENAME}" -type f -print0 | xargs -0 chmod 644
	# rpm macros
	install -m644 ${BUILD_DIR}/patches/${PACKAGENAME}/cmake.macros -D ${buildroot}${TARGET_SYSCONFDIR}/rpm/macros.cmake
	install -m644 ${BUILD_DIR}/patches/${PACKAGENAME}/cmake.attr -D ${buildroot}${TARGET_PREFIX}/lib/rpm/fileattrs/cmake.attr
	install -m644 ${BUILD_DIR}/patches/${PACKAGENAME}/cmake.prov -D ${buildroot}${TARGET_PREFIX}/lib/rpm/cmake.prov
	install -m644 ${BUILD_DIR}/patches/${PACKAGENAME}/cmake-${CMAKE_SYSTEM_NAME}.cmake -D ${buildroot}${TARGET_PREFIX}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake
	if test "${CMAKE_SYSTEM_NAME}" = mint; then
	    ( cd "${buildroot}${TARGET_PREFIX}/share/cmake/Modules/Platform/"; $LN_S -f ${CMAKE_SYSTEM_NAME}.cmake FreeMiNT.cmake )
	fi
	
	install -m644 ${BUILD_DIR}/patches/${PACKAGENAME}/cmake-${CMAKE_SYSTEM_NAME}-cross.cmake -D "${THISPKG_DIR}${prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake"
	( cd "${THISPKG_DIR}${prefix}/share/cmake/Modules/Platform";
	  $LN_S ${CMAKE_SYSTEM_NAME}.cmake ${TARGET}.cmake;
	  if test "${CMAKE_SYSTEM_NAME}" = mint; then
	    $LN_S -f ${CMAKE_SYSTEM_NAME}.cmake FreeMiNT.cmake
	  fi
	)

	# no shared libs -> no plugins
	# rm -f ${buildroot}${TARGET_PREFIX}/share/cmake/include/*.h
	# rmdir ${buildroot}${TARGET_PREFIX}/share/cmake/include
	
	${MAKE} clean >/dev/null
	rm -f ${buildroot}${TARGET_LIBDIR}$multilibdir/charset.alias

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
