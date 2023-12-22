#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=xgalaga
VERSION=-2.1.1.0
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
aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --foreign --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=/
	--datarootdir=/
	${CONFIGURE_FLAGS_AMIGAOS}
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s -Wl,--msuper-memory" \
	./configure ${CONFIGURE_FLAGS} \
	--localstatedir='${datarootdir}' \
	--libdir='${exec_prefix}/lib'$multilibdir

	# configure does not allow to use --datarootdir=.
	${MAKE} $JOBS prefix=. datarootdir=. || exit 1

	mkdir -p ${THISPKG_DIR}
	
	mv "src/xgalaga-sdl" "${THISPKG_DIR}/xgalaga-${CPU}.prg" || exit 1
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p COPYING README CREDITS CHANGES "${THISPKG_DIR}"
cp -p xgalaga-sdl.6x "${THISPKG_DIR}/xgalaga.6"
cp -pr fonts images levels sounds "${THISPKG_DIR}"

make_bin_archive
make_archives
