#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ltris
VERSION=-1.2.7
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
	${MAKE} $JOBS prefix=. datarootdir=. || exit 1

	mkdir -p ${THISPKG_DIR}
	
	mv "src/ltris" "${THISPKG_DIR}/ltris-${CPU}.prg" || exit 1
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"

cp -p AUTHORS COPYING ChangeLog README "${THISPKG_DIR}"
cp -pr src/gfx src/sounds src/figures "${THISPKG_DIR}"
rm -f "${THISPKG_DIR}"/*/Makefile*

for lang in `cat po/LINGUAS`; do
    mkdir -p "${THISPKG_DIR}/locale/$lang/LC_MESSAGES"
    cp -p po/$lang.gmo "${THISPKG_DIR}/locale/$lang/LC_MESSAGES/$PACKAGENAME.mo"
done

make_bin_archive
make_archives
