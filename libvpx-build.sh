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

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CHOST="$TARGET" \
	LD="${TARGET}-gcc" \
	CC="${TARGET}-gcc" \
	CXX="${TARGET}-g++" \
	AR="${ar}" \
	RANLIB=${ranlib} \
	NM=${TARGET}-nm \
	STRIP=${TARGET}-strip \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} --libdir="${prefix}/lib$multilibdir" || exit 1

	# hack_lto_cflags
	${MAKE} V=1 $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
