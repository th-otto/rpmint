#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=automake
VERSION=-1.16
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/automake/automake-1.16-0001-source.patch
patches/automake/automake-1.16-0002-crossconfig.patch
patches/automake/automake-1.16-0003-subdir-objects.patch
patches/automake/automake-1.16-0004-fix-primary-prefix-invalid-couples-test.patch
patches/automake/automake-1.16-0006-correct-parameter-parsing-in-test-driver-script.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/doc/automake
${TARGET_PREFIX#/}/share/automake*
${TARGET_PREFIX#/}/share/aclocal*
"

unpack_archive

cd "$MINT_BUILD_DIR"
sed -e 's@-unknown-@-${VENDOR}-@g' lib/config.guess > lib/config.guess.new && mv lib/config.guess.new lib/config.guess
touch -r configure Makefile.am Makefile.in t/testsuite-part.am

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix}"

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
