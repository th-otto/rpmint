#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=kobo-deluxe
VERSION=-0.5.1
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

rm -f aclocal.m4 acinclude.m4
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --foreign --force --copy --add-missing
rm -rf autom4te.cache aconfig.h.in.orig configure.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--without-x
	--disable-opengl
	--disable-sdltest
"
STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s -Wl,--msuper-memory" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	${MAKE} $JOBS DATA_PREFIX="./" || exit 1

	mkdir -p "${THISPKG_DIR}/scores"
	cp -p kobodl "${THISPKG_DIR}/KoboDeluxe-${CPU}.prg"

	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
cp -pr COPYING* ChangeLog TODO README* "${THISPKG_DIR}"
cp -pr data/gfx data/sfx "${THISPKG_DIR}"
rm -f "${THISPKG_DIR}/sfx/"Makefile*
rm -f "${THISPKG_DIR}/gfx/"Makefile*

make_bin_archive
make_archives
