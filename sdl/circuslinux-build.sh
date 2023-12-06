#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=circuslinux
VERSION=-1.0.3
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
automake --foreign --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
	--enable-static
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	${MAKE} DATA_PREFIX="data/" $JOBS || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p circuslinux "${THISPKG_DIR}/circuslinux-${CPU}.prg"

	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
cp -pr AUTHORS.txt COPYING.txt CHANGES.txt FAQ.txt README.txt README-SDL.txt TODO.txt "${THISPKG_DIR}"
mkdir -p "${THISPKG_DIR}/data"
cp -pr data/images data/music data/sounds "${THISPKG_DIR}/data"
touch "${THISPKG_DIR}/circuslinux.dat"

make_bin_archive
make_archives
