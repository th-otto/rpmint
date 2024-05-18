#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=a52dec
VERSION=-0.8.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$srcdir"

autoreconf -fiv
cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-static
	--disable-shared
"

WITH_FASTCALL=`if $gcc -mfastcall -E - < /dev/null >/dev/null 2>&1; then echo true; else echo false; fi`

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	if $WITH_FASTCALL; then
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" \
		LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" \
		"$srcdir/configure" ${CONFIGURE_FLAGS} --libdir="${prefix}/lib$multilibdir/mfastcall" || exit 1
		${MAKE} V=1 $JOBS || exit 1
		${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
		${MAKE} distclean
	fi

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} --libdir="${prefix}/lib$multilibdir" || exit 1
	${MAKE} V=1 $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
