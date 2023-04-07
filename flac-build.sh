#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=flac
VERSION=-1.3.2
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/flac/flac-CVE-2017-6888.patch
patches/flac/flac-cflags.patch
patches/flac/flac-lrintf.patch
patches/flac/flac-staticlibs.patch
patches/flac/flac-config.patch
patches/flac/flac-amigaos.patch
patches/flac/flac-wcwidth.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME}
	--with-ogg=yes
	--disable-shared
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags

	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME} install
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
