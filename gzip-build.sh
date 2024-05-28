#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gzip
VERSION=-1.9
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/gzip-zgrep.diff
patches/${PACKAGENAME}/gzip-zmore.diff
patches/${PACKAGENAME}/gzip-non-exec-stack.diff
patches/${PACKAGENAME}/gzip-zdiff.diff
patches/${PACKAGENAME}/gzip-xz_lzma.patch
patches/${PACKAGENAME}/gzip-manpage-no-date.patch
patches/${PACKAGENAME}/gzip-1.9-mint.patch
patches/${PACKAGENAME}/gzip-gnulib-strerror_r.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
"

MINT_BUILD_DIR="$srcdir"

unpack_archive

cd "$srcdir"

autoreconf -fiv
rm -rf autom4te.cache

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" build-aux/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME}
	--config-cache
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
EOF
	append_gnulib_cache
cat <<EOF >>config.cache
ac_cv_func_strerror_r=yes
ac_cv_have_decl_strerror_r=yes
gl_cv_func_working_strerror=yes
gl_cv_func_strerror_r_works=yes
EOF
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	CFLAGS="${CPU_CFLAGS} $COMMON_CFLAGS ${STACKSIZE}" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
