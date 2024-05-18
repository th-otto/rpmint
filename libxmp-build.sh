#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libxmp
VERSION=-4.6.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/libxmp.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
patches/libxmp/xmpinfo.c
patches/libxmp/xmpplay.c
"
BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared ${CONFIGURE_FLAGS_AMIGAOS}"

WITH_FASTCALL=`if $gcc -mfastcall -E - < /dev/null >/dev/null 2>&1; then echo true; else echo false; fi`

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	if $WITH_FASTCALL; then
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" \
		CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" \
		LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall ${STACKSIZE}" \
		./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir/mfastcall
		${MAKE} $JOBS || exit 1
		${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
		${MAKE} distclean >/dev/null
	fi

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS -Iinclude ${ELF_LDFLAGS} -o ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/xmpinfo "${BUILD_DIR}/patches/libxmp/xmpinfo.c" lib/libxmp.a -lm || exit 1
	${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS -Iinclude ${ELF_LDFLAGS} -o ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/xmpplay "${BUILD_DIR}/patches/libxmp/xmpplay.c" lib/libxmp.a -lSDL -lvorbis -lm || exit 1

	${MAKE} distclean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias

	#
	# remove cmake dirs in architecture dependent subdirs
	# we only need the one in the toplevel directory
	#
	if test "$multilibdir" != ""; then
		rm -rf "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/$multilibdir/cmake"
	fi

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
