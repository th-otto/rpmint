#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=windom
VERSION=-2.0.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/windom/cross.patch"

BINFILES="
${TARGET_BINDIR}/windom-demo.app
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="$LTO_CFLAGS"

SUBDIRS="src demo"

mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include

for CPU in 020 v4e 000; do
	eval libdir=${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}\${CPU_LIBDIR_$CPU}
	mkdir -p "$libdir"
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	mkdir -p "$libdir"
	rm -f lib/gcc/*.a
	for dir in $SUBDIRS; do
		cd $dir || exit 1
		${MAKE} clean
		${MAKE} -f gcc.mak \
			CROSS_PREFIX=${TARGET}- \
			M68K_ATARI_MINT_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
			M68K_ATARI_MINT_LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" || exit 1
		${MAKE} -f gcc.mak \
			PREFIX=${THISPKG_DIR}${sysroot}${TARGET_PREFIX} \
			CROSS_PREFIX=${TARGET}- \
			M68K_ATARI_MINT_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
			M68K_ATARI_MINT_LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" install || exit 1
		cd ..
	done
	mv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/*.a "$libdir"
	make_bin_archive $CPU
done

docdir="${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/doc/${PACKAGENAME}"
mkdir -p "$docdir"
cp -ra doc/. "$docdir"

make_archives
