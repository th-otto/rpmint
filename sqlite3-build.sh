#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=sqlite3
VERSION=-3.44.2
VERSIONPATCH=

. ${scriptdir}/functions.sh

srcdir="$here/sqlite-version-${VERSION#-}"
MINT_BUILD_DIR="$srcdir"

PATCHES="
patches/${PACKAGENAME}/sqlite3-mint.patch
"
DISABLED_PATCHES="
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 build-scripts/ltmain.sh acinclude/libtool.m4 acinclude/lt*
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
# automake --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
	--enable-static
	--without-pic
	--enable-readline
	--enable-fts3
	--enable-fts4
	--enable-fts5
	--enable-update-limit
	--enable-json
	--disable-amalgamation
	--disable-load-extension
	--disable-threadsafe
	--disable-largefile 
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} \
		--with-readline-lib='-lreadline -lncurses' \
		--with-readline-inc="-I${sysroot}/usr/include/readline" \
		--libdir='${exec_prefix}/lib'$multilibdir

	: hack_lto_cflags

	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
