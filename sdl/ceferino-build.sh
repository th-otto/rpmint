#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ceferino
VERSION=-0.97.8
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"

EXTRA_DIST="
patches/automake/mintelf-config.sub
patches/${PACKAGENAME}/config.rpath
"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

cp "${BUILD_DIR}/patches/${PACKAGENAME}/config.rpath" .

rm -f aclocal.m4 acinclude.m4 config.cache config.status config.log
aclocal || exit 1
autoconf || exit 1
automake --foreign --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub
rm -rf intl
mkdir intl
echo "all:" > intl/Makefile.in
echo "clean:" >> intl/Makefile.in

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=/usr
	--disable-shared
	${CONFIGURE_FLAGS_AMIGAOS}
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s -Wl,--msuper-memory" \
	./configure ${CONFIGURE_FLAGS} || exit 1

	${MAKE} $JOBS datadir=. pkgdatadir=data || exit 1

	mkdir -p "${THISPKG_DIR}"
	mv src/ceferino "${THISPKG_DIR}/ceferino-${CPU}.prg" || exit 1
	mv src/ceferinoeditor "${THISPKG_DIR}/ceferinoeditor-${CPU}.prg" || exit 1
	mv src/ceferinosetup "${THISPKG_DIR}/ceferinosetup-${CPU}.prg" || exit 1
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p AUTHORS COPYING README ChangeLog "${THISPKG_DIR}"
cp -pr data "${THISPKG_DIR}"
find "${THISPKG_DIR}"/data -name "Makefile*" | xargs rm

mkdir -p "${THISPKG_DIR}/locale/ca_CA/LC_MESSAGES"
cp -p po/ca.gmo "${THISPKG_DIR}/locale/ca_CA/LC_MESSAGES/ceferino.mo"
mkdir -p "${THISPKG_DIR}/locale/es_ES/LC_MESSAGES"
cp -p po/es.gmo "${THISPKG_DIR}/locale/es_ES/LC_MESSAGES/ceferino.mo"
mkdir -p "${THISPKG_DIR}/locale/fr_FR/LC_MESSAGES"
cp -p po/fr.gmo "${THISPKG_DIR}/locale/fr_FR/LC_MESSAGES/ceferino.mo"

make_bin_archive
make_archives
