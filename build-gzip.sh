#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gzip
VERSION=-1.8
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/gzip/zgrep.diff
patches/gzip/zmore.diff
patches/gzip/non-exec-stack.diff
patches/gzip/zdiff.diff
patches/gzip/xz_lzma.patch
patches/gzip/manpage-no-date.patch
patches/gzip/gzip-1.3-mint.patch
patches/gzip/mintelf-config.patch
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
"

MINT_BUILD_DIR="$srcdir"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O3 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --mandir=${prefix}/share/man --config-cache"

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
gl_cv_func_strerror_r_works=yes
EOF
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	STACKSIZE="-Wl,-stack,64k"
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
