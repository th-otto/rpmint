#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=opus
VERSION=-1.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

BINFILES="
"

unpack_archive

cd "$srcdir"

autoreconf -fiv
cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing -Wno-attributes ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-static
	--disable-shared
	--enable-custom-modes
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} --libdir="${prefix}/lib$multilibdir" || exit 1

	${MAKE} V=1 $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} clean > /dev/null
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
