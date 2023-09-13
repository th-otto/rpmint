#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libmad
VERSION=-0.15.1b
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/libmad-0.15.1b-automake.patch
patches/${PACKAGENAME}/libmad-0.15.1b-pkgconfig.patch
patches/${PACKAGENAME}/libmad-0.15.1b-gcc43.patch
patches/${PACKAGENAME}/libmad-Provide-Thumb-2-alternative-code-for-MAD_F_MLN.diff
patches/${PACKAGENAME}/libmad-thumb.diff
patches/${PACKAGENAME}/libmad-0.15.1b-ppc.patch
patches/${PACKAGENAME}/libmad-frame_length.diff
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

BINFILES="
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS} ${CFLAGS_AMIGAOS}"
case $TARGET in
m68k-atari-mint*)
	STACKSIZE="-Wl,-stack,256k"
	;;
m68k-amigaos*)
	;;
esac

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
