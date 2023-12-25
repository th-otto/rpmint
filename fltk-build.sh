#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=fltk
VERSION=-1.3.9
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/fltk-mint.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"
BINFILES="
"

unpack_archive

cd "$srcdir"

autoconf --force || exit 1
automake --force --copy --add-missing
rm -rf autom4te.cache

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-threads
	--disable-localpng
	--disable-localzlib
	--disable-largefile
	--disable-fluid
	--disable-test
	--disable-xdbe
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	# hack_lto_cflags
	${MAKE} V=1 $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
