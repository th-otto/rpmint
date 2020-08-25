#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gnucobol
VERSION=-3.0-rc1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/gnucobol/gnucobol-CFLAGS.patch
patches/gnucobol/gnucobol-ltdl.patch
patches/gnucobol/gnucobol-mintelf-config.patch
"

DISABLED_PATCHES="
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/*
${TARGET_PREFIX#/}/include/*
${TARGET_PREFIX#/}/lib/*
"

unpack_archive

cd "$srcdir"

aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/gnucobol-mintelf-config.patch"

export LANG=POSIX
export LC_ALL=POSIX

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--datadir=${prefix}/share \
	--disable-nls \
	--without-dl \
	--disable-shared"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	STACKSIZE="-Wl,-stack,128k"
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
		./configure ${CONFIGURE_FLAGS} || exit 1
	hack_lto_cflags
	${MAKE} HELP2MAN=true || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" HELP2MAN=true install
	rm -f "${THISPKG_DIR}${sysroot}${prefix}/lib/"*.la
	if test -n "$multilibdir"; then
		mkdir -p "${THISPKG_DIR}${sysroot}${prefix}/lib$multilibdir"
		mv "${THISPKG_DIR}${sysroot}${prefix}/lib/"*.a "${THISPKG_DIR}${sysroot}${prefix}/lib$multilibdir"
	fi

	mv "${THISPKG_DIR}${sysroot}/${TARGET_BINDIR}" "${THISPKG_DIR}/bin-${CPU}"

	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
done

for CPU in ${ALL_CPUS}; do
	mv  "${THISPKG_DIR}/bin-${CPU}" "${THISPKG_DIR}${sysroot}/${TARGET_BINDIR}"
	make_bin_archive $CPU
	rm -rf "${THISPKG_DIR}${sysroot}/${TARGET_BINDIR}"
done

move_prefix
configured_prefix="${prefix}"

mkdir "${THISPKG_DIR}${sysroot}/${TARGET_BINDIR}"
touch "${THISPKG_DIR}${sysroot}/${TARGET_BINDIR}/dummy"
make_archives
