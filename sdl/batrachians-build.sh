#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=batrachians
VERSION=-0.1.7
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""

EXTRA_DIST="
patches/automake/mintelf-config.sub
patches/flatzebra/flatzebra.patch
"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

rm -f aclocal.m4 acinclude.m4 config.cache config.status config.log
aclocal -I macros || exit 1
autoconf || exit 1
automake --foreign --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=/usr
	${CONFIGURE_FLAGS_AMIGAOS}
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s -Wl,--msuper-memory" \
	./configure ${CONFIGURE_FLAGS} || exit 1

	${MAKE} $JOBS datadir=. pkgdatadir=data pkgsounddir=sounds || exit 1

	mkdir -p "${THISPKG_DIR}"
	mv src/batrachians "${THISPKG_DIR}/batrachians-${CPU}.prg" || exit 1
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p AUTHORS COPYING README NEWS THANKS "${THISPKG_DIR}"
cp -pr src/sounds "${THISPKG_DIR}"

make_bin_archive
make_archives
