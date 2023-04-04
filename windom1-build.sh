#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=windom1
VERSION=-1.21.3
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/windom1/windom1-1.21.3.patch
patches/windom1/windom1-cross.patch
patches/windom1/windom1-menuexec.patch
patches/windom1/windom1-formthumb.patch
patches/windom1/windom1-gemlib.patch
"

BINFILES="
${TARGET_BINDIR}/windom1-demo.app
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-Os -fomit-frame-pointer $LTO_CFLAGS"

SUBDIRS="src demo"

mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include

for CPU in ${ALL_CPUS}; do
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	rm -f lib/gcc/*.a
	for dir in $SUBDIRS; do
		cd $dir || exit 1
		${MAKE} clean
		${MAKE} -f gcc.mak \
			CROSS_PREFIX=${TARGET}- \
			M68K_ATARI_MINT_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
			M68K_ATARI_MINT_LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" || exit 1
		mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/lib
		mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include
		${MAKE} -f gcc.mak \
			PREFIX=${THISPKG_DIR}${sysroot}${TARGET_PREFIX} \
			CROSS_PREFIX=${TARGET}- \
			M68K_ATARI_MINT_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
			M68K_ATARI_MINT_LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" install || exit 1
		cd ..
	done
	if test "$multilibdir" != ""; then
		mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir"
		mv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/*.a "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir"
	fi
	make_bin_archive $CPU
done

docdir="${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/doc/${PACKAGENAME}"
mkdir -p "$docdir"
cp -ra doc/. "$docdir"

make_archives
