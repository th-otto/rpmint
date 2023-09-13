#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=autoconf-archive
VERSION=-2023.02.20
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""

BINFILES="
${TARGET_PREFIX#/}/share/aclocal
${TARGET_PREFIX#/}/share/info
${TARGET_PREFIX#/}/share/doc
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--docdir=${prefix}/share/doc/packages/${PACKAGENAME}
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

NO_STRIP=true

for CPU in noarch; do
	cd "$MINT_BUILD_DIR"

	CFLAGS="$COMMON_CFLAGS" LDFLAGS="$COMMON_CFLAGS ${STACKSIZE}" ./configure ${CONFIGURE_FLAGS}
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null
	rm -fv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir/charset.alias
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
