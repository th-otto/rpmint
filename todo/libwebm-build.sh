#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libwebm
VERSION=-1.0.0.29
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/libwebm-1.0.0.29-m68k-atari-mint.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

#
# SDL is only needed for the example
#
CONFIGURE_FLAGS="--prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
	--disable-unit-tests
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	${MAKE} -f Makefile.unix \
		CXX="${TARGET}-g++ $CPU_CFLAGS $COMMON_CFLAGS -D_GNU_SOURCE -s" \
		AR="${ar}" \
		RANLIB=${ranlib} \
		V=1 $JOBS || exit 1

	# there is no install target :(
	
	mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_BINDIR}"
	mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir"
	mkdir -p "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include/webm"

	cp -a mkvparser_sample mkvmuxer_sample dumpvtt vttdemux "${THISPKG_DIR}${sysroot}${TARGET_BINDIR}"
	cp -a libwebm.a "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir"
	cp -a webm_parser/include/webm/* "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include/webm"
	
	${MAKE} -f Makefile.unix clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
