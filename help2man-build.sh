#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=help2man
VERSION=-1.49.3
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix}
	--docdir=${prefix}/share/doc/packages/${PACKAGENAME}
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

NO_STRIP=true

for CPU in noarch; do
	cd "$MINT_BUILD_DIR"

	CFLAGS="$COMMON_CFLAGS" \
	LDFLAGS="$COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS}

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null
	rm -fv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir/charset.alias
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
