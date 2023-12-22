#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=stargun
VERSION=-0.2
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

rm -f aclocal.m4 acinclude.m4 config.cache config.status config.log
aclocal || exit 1
autoconf || exit 1
automake --foreign --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig
# WTF
rm -f src/SDL_mixer.h src/SDL_ttf.h

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
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s -Wl,--msuper-memory" \
	./configure ${CONFIGURE_FLAGS}

	${MAKE} $JOBS || exit 1

	mkdir -p "${THISPKG_DIR}"
	mv src/stargun "${THISPKG_DIR}/stargun-${CPU}.prg" || exit 1
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p AUTHORS COPYING README ChangeLog "${THISPKG_DIR}"
cp -pr src/levels src/sounds src/pics src/ariblk.ttf "${THISPKG_DIR}"

make_bin_archive
make_archives
