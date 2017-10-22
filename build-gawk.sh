#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gawk
VERSION=-4.1.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/gawk/gawk_ppc64le_ignore_transient_test_time_failure.patch
patches/gawk/gawk-4.1.4-mint.patch
patches/gawk/mintelf-config.patch
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/awk
"

MINT_BUILD_DIR="$srcdir"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --config-cache"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_func_working_mktime=yes
EOF
	append_gnulib_cache
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache
	STACKSIZE="-Wl,-stack,128k"
	CFLAGS="${CPU_CFLAGS} $COMMON_CFLAGS ${STACKSIZE}" \
		"$srcdir/configure" ${CONFIGURE_FLAGS} \
		--libdir='${exec_prefix}/lib'$multilibdir \
		--libexecdir='${exec_prefix}/libexec'$multilibexecdir
	hack_lto_cflags
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
