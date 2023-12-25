#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=dillo
VERSION=-3.1-dev
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/${PACKAGENAME}.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/*
${TARGET_PREFIX#/}/share/doc/*
${TARGET_MANDIR#/}/man1/*
${TARGET_SYSCONFDIR#/}/*
"

unpack_archive

cd "$srcdir"

./autogen.sh
cp ${BUILD_DIR}/patches/automake/mintelf-config.sub config.sub

cd "$MINT_BUILD_DIR"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --docdir=${TARGET_PREFIX}/share/doc/${PACKAGENAME}
	--sysconfdir=${TARGET_SYSCONFDIR}
	--disable-threaded-dns
"

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS ${ELF_CFLAGS}"

export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

STACKSIZE="-Wl,-stack,256k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $STACKSIZE" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean >/dev/null

	make_bin_archive $CPU
done

make_archives
