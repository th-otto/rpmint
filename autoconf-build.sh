#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=autoconf
VERSION=-2.69
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/autoconf/autoconf-2.69-0001-install-version.patch
patches/autoconf/autoconf-2.69-0002-atomic-replace.patch
patches/autoconf/autoconf-2.69-0003-ltdl.patch
patches/autoconf/autoconf-2.69-0004-cache.patch
patches/autoconf/autoconf-2.69-0006-man.patch
patches/autoconf/autoconf-2.69-0007-define.patch
patches/autoconf/autoconf-2.69-0008-crossconfig.patch
patches/autoconf/autoconf-2.69-0009-perl-5.17-fixes.patch
patches/autoconf/autoconf-texinfo.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/autoconf
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix}
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
