#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=lynx
VERSION=-2.9.1
VERSIONPATCH=

srcarchive=${PACKAGENAME}${VERSION#-}

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/lynx-mint.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/locale/*
${TARGET_PREFIX#/}/share/doc/
etc/lynx.cfg
etc/lynx.lss
"

srcdir="$here/$srcarchive"
MINT_BUILD_DIR="$srcdir"
unpack_archive

cd "$srcdir"
#autoreconf -fiv
cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

export LANG=POSIX
export LC_ALL=POSIX

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--sysconfdir=/etc
	--enable-nls
	--with-ssl
	--with-screen=ncurses
"
STACKSIZE="-Wl,-stack,128k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	./configure ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install-help
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install-doc

	cd ${MINT_BUILD_DIR}
	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
