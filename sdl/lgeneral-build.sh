#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=lgeneral
VERSION=-1.4.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"

EXTRA_DIST="
patches/automake/mintelf-config.sub
patches/${PACKAGENAME}/pg-data-conv.tar.xz
"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

rm -f aclocal.m4 acinclude.m4 acconfig.h lgeneral-redit/acconfig.h
aclocal || exit 1
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
	--disable-install
	${CONFIGURE_FLAGS_AMIGAOS}
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s -Wl,--msuper-memory" \
	LIBS="-lintl -liconv" \
	./configure ${CONFIGURE_FLAGS} \
	--localstatedir='${datarootdir}' \
	--libdir='${exec_prefix}/lib'$multilibdir

	# configure does not allow to use --datarootdir=.
	${MAKE} $JOBS prefix=data datarootdir=data || exit 1

	mkdir -p "${THISPKG_DIR}/tools"
	
	mv src/lgeneral "${THISPKG_DIR}/lgeneral-${CPU}.prg" || exit 1
	mv tools/ltrextract/ltrextract "${THISPKG_DIR}/tools/ltrextract-${CPU}.ttp"
	mv lgc-pg/lgc-pg "${THISPKG_DIR}/tools/lgc-pg-${CPU}.ttp"
	mv lgc-pg/shptool  "${THISPKG_DIR}/tools/shptool-${CPU}.ttp"
	mv lged/lged "${THISPKG_DIR}/tools/lged-${CPU}.ttp"

	for lang in de en; do
	    mkdir -p "${THISPKG_DIR}/data/locale/$lang/LC_MESSAGES"
	    cp -p po/$PACKAGENAME/$lang.gmo "${THISPKG_DIR}/data/locale/$lang/LC_MESSAGES/$PACKAGENAME.mo"
	    cp -p po/pg/$lang.gmo "${THISPKG_DIR}/data/locale/$lang/LC_MESSAGES/pg.mo"
	done

	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

if test -d "${THISPKG_DIR}."; then
   mv "${THISPKG_DIR}."/* "${THISPKG_DIR}"
   rmdir "${THISPKG_DIR}."
fi

cp -p AUTHORS COPYING ChangeLog TODO README* "${THISPKG_DIR}"

mkdir -p "${THISPKG_DIR}/data"
cp -pr src/ai_modules src/campaigns src/gfx src/maps src/music src/nations src/scenarios src/sounds src/terrain src/themes src/units lgc-pg/convdata "${THISPKG_DIR}/data"
rm -f "${THISPKG_DIR}"/data/*/Makefile* "${THISPKG_DIR}"/data/*/*/Makefile*

cd "${THISPKG_DIR}"/data
tar xf "${scriptdir}/patches/${PACKAGENAME}/pg-data-conv.tar.xz"

make_bin_archive
make_archives
