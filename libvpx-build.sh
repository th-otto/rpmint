#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libvpx
VERSION=-1.13.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/libvpx-mint.diff
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

WITH_FASTCALL=`if $gcc -mfastcall -E - < /dev/null >/dev/null 2>&1; then echo true; else echo false; fi`

doconf()
{
	locale extra_cflags
	
	if test "$1" = "fastcall"; then
		extra_cflags=" -mfastcall"
		subdir=/mfastcall
	else
		extra_cflags=""
		subdir=
	fi
	CHOST="$TARGET" \
	LD="${TARGET}-gcc" \
	CC="${TARGET}-gcc" \
	CXX="${TARGET}-g++" \
	AR="${ar}" \
	RANLIB=${ranlib} \
	NM=${TARGET}-nm \
	STRIP=${TARGET}-strip \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $extra_cflags" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $extra_cflags" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $extra_cflags" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} --libdir="${prefix}/lib$multilibdir$subdir" || exit 1

	# the --size-limit switch is broken atm ...
	echo "#undef CONFIG_SIZE_LIMIT" >> vpx_config.h
	echo "#define CONFIG_SIZE_LIMIT 1" >> vpx_config.h
	echo '#define DECODE_WIDTH_LIMIT 8192'  >> vpx_config.h
	echo '#define DECODE_HEIGHT_LIMIT 8192' >> vpx_config.h
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	if $WITH_FASTCALL; then
		doconf fastcall
		${MAKE} V=1 $JOBS || exit 1
		${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
		${MAKE} distclean
	fi

	doconf
	${MAKE} V=1 $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
