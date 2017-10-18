#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=m4
VERSION=-1.4.18
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/m4/mintelf-config.patch"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--without-included-regex \
	gl_cv_func_isnanl_works=yes \
	gl_cv_func_printf_directive_n=yes \
	gl_cv_func_printf_infinite_long_double=yes"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in 020 v4e 000; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}${multilibdir}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
