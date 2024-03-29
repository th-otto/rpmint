#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=bison
VERSION=-3.6.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""
DISABLED_PATCHES="
patches/${PACKAGENAME}/bison-gcc7-fix.patch
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/man/man1/*
${TARGET_PREFIX#/}/share/doc/packages/bison/*
${TARGET_PREFIX#/}/share/aclocal/*
${TARGET_PREFIX#/}/share/bison/*
"

unpack_archive

cd "$srcdir"

aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" build-aux/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"
STACKSIZE=-Wl,-stack,128k

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME} --config-cache"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
EOF
	append_gnulib_cache
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	${MAKE} || exit 1
	: ${MAKE} -C doc refcard.ps
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} -i clean

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}${multilibdir}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
