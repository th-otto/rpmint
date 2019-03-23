#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=wget
VERSION=-1.19.5
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES="
${TARGET_BINDIR#/}
${TARGET_PREFIX#/}/share/man/*
${TARGET_PREFIX#/}/share/info/*
"

PATCHES="
patches/wget/wgetrc.patch
patches/wget/wget-libproxy.patch
patches/wget/wget-1.14-no-ssl-comp.patch
patches/wget/wget-fix-pod-syntax.diff
patches/wget/wget-errno-clobber.patch
patches/wget/wget-ignore-void-retvalue.patch
"

unpack_archive

cd "$MINT_BUILD_DIR"

autoreconf -v --force

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--with-ssl=openssl \
	--with-cares \
	--with-metalink"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

ALL_CPUS=020
for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_BINDIR#/}/libgcrypt-config
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
