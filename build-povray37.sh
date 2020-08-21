#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=povray
VERSION=-3.7.0.8
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/povray-3.6.9.7-ini.patch
patches/${PACKAGENAME}/povray-3.6.9.7-fix.patch
patches/${PACKAGENAME}/povray-3.6.9.7-boost-link.patch
patches/${PACKAGENAME}/povray-reproducible.patch
"
DISABLED_PATCHES="
patches/${PACKAGENAME}/povray37-autoconf.patch
patches/${PACKAGENAME}/povray37-mintelf-config.patch
"

BINFILES="
etc/povray
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share/*
"

unpack_archive

cd "$srcdir"

# fix wrong newline encoding
dos2unix -k unix/scripts/*.sh

patch -p1 "$BUILD_DIR/patches/${PACKAGENAME}/autoconf.patch" || exit 1

# remove inline copies of shared libraries
rm -rf libraries
( cd unix && ./prebuild.sh )

# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/povray37-mintelf-config.patch"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS"
STACKSIZE="-Wl,-stack,256k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --sysconfdir=/etc --with-boost=no --with-boost-thread=no"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
    COMPILED_BY="Thorsten Otto for MiNT" \
	--libdir='${exec_prefix}/lib'$multilibdir

	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
