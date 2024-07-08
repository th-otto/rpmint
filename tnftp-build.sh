#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=tnftp
VERSION=-20230507
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/tnftp-mint.patch
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
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" buildaux/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS} \
	--enable-editcomplete
	--disable-ipv6
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1

	# hack_lto_cflags
	${MAKE} V=1 $JOBS || exit 1
	${MAKE} prefix="${THISPKG_DIR}${sysroot}/usr" install || exit 1
	cd "${THISPKG_DIR}${sysroot}/usr/bin" && $LN_S tnftp ftp

	cd "$MINT_BUILD_DIR"
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
