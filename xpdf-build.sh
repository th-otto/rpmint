#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=xpdf
VERSION=-4.04
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man5/*
"

unpack_archive

cd "$srcdir"

autoreconf -fi
rm -rf autom4te.cache config.h.in.orig
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" build-aux/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"
case $TARGET in
m68k-atari-mint*)
	STACKSIZE="-Wl,-stack,256k"
	;;
m68k-amigaos*)
	;;
esac

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME}
	--disable-shared
	--disable-multithreaded
	--disable-exceptions
	--disable-cmyk
"


export prefix=${prefix}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1

	${MAKE} clean >/dev/null
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
