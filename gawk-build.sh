#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gawk
VERSION=-4.1.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/gawk/gawk-ppc64le_ignore_transient_test_time_failure.patch
patches/gawk/gawk-4.1.4-mint.patch
patches/gawk/gawk-libexecdir.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/awk
${TARGET_PREFIX#/}/libexec/awk/*
${TARGET_PREFIX#/}/share/locale
"

MINT_BUILD_DIR="$srcdir"

unpack_archive

cd "$srcdir"

autoreconf -fiv
rm -rf autom4te.cache

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--config-cache
"
STACKSIZE="-Wl,-stack,256k"

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
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache
	CFLAGS="${CPU_CFLAGS} $COMMON_CFLAGS ${STACKSIZE}" \
		"$srcdir/configure" ${CONFIGURE_FLAGS} \
		--libdir='${exec_prefix}/lib'$multilibdir \
		--libexecdir='${exec_prefix}/libexec/awk'$multilibexecdir
	: hack_lto_cflags
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/gawk${VERSION}
	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
