#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=fillets-ng
VERSION=-1.0.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/${PACKAGENAME}/${PACKAGENAME}.patch"

EXTRA_DIST="
patches/automake/mintelf-config.sub
patches/${PACKAGENAME}/unpack_data_here.txt
patches/${PACKAGENAME}/options.lua
"

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

rm -f aclocal.m4 acinclude.m4 sdl.m4
aclocal || exit 1
autoconf || exit 1
automake --foreign --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

CONFIGURE_FLAGS="--host=${TARGET} ${CONFIGURE_FLAGS_AMIGAOS}
	--prefix=/
	--datarootdir=/
	--without-x
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s -Wl,--msuper-memory" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	# configure does not allow to use --datadir=.
	sed -i 's/^S\["datadir"\]="\([^"]*\)"$/S\["datadir"\]="."/' config.status
	./config.status

	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}" install

	mv "${THISPKG_DIR}/bin/fillets" "${THISPKG_DIR}/fillets-${CPU}.prg" || exit 1
	rmdir "${THISPKG_DIR}/bin"
	
	${MAKE} clean >/dev/null
done

cd "$MINT_BUILD_DIR"
mkdir -p "${THISPKG_DIR}/doc"
cp -pr AUTHORS COPYING ChangeLog NEWS README TODO "${THISPKG_DIR}/doc"
cp -p "$here/patches/${PACKAGENAME}/unpack_data_here.txt" "${THISPKG_DIR}"
mkdir -p "${THISPKG_DIR}/script"
cp -p "$here/patches/${PACKAGENAME}/options.lua" "${THISPKG_DIR}/script"

make_bin_archive
make_archives
