#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mp4v2
VERSION=-2.1.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/mp4v2-mint.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"
BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

autoreconf -fiv
# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" autoaux/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-fvisibility ${CONFIGURE_FLAGS_AMIGAOS}"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1

	# help2man is bogus, it tries to execute the just-compiled binaries
	sed -i "s|S\[\"FOUND_HELP2MAN\"\]=.*|S[\"FOUND_HELP2MAN\"]=\"no\"|" config.status
	./config.status

	# hack_lto_cflags
	${MAKE} V=1 $JOBS || exit 1
	${MAKE} prefix="${THISPKG_DIR}${sysroot}/usr" install || exit 1
	${MAKE} distclean
	
	# remove the empty man pages
	rm -f ${THISPKG_DIR}${sysroot}/usr/share/man/man1/*
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
