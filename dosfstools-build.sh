#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=dosfstools
VERSION=-4.1+git
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
"

BINFILES="
sbin/*
${TARGET_PREFIX#/}/share/doc/*
${TARGET_MANDIR#/}/man8/*
"

unpack_archive

cd "$srcdir"

aclocal || exit 1
autoconf || exit 1
automake --copy --add-missing || exit 1

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME}
	--sbindir=/sbin
	--enable-compat-symlinks
	--enable-atari-check
	--without-udev
"

export LIBICONV=-liconv

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
