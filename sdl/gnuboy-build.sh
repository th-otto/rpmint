#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gnuboy
VERSION=-1.0.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"

EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=/
	--datarootdir=/
	--with-sdl
	--without-x
	--without-sdl2
	${CONFIGURE_FLAGS_AMIGAOS}
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	./configure ${CONFIGURE_FLAGS}

	${MAKE} $JOBS || exit 1

	mkdir -p "${THISPKG_DIR}"
	mv sdlgnuboy "${THISPKG_DIR}/gnuboy-${CPU}.gtp" || exit 1
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p COPYING README docs/* "${THISPKG_DIR}"
cp -pr etc "${THISPKG_DIR}"

make_bin_archive
make_archives
