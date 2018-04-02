#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gettext
VERSION=-0.19.8.1-1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/gettext/mintelf-config.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/libexec/${PACKAGENAME}/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/doc/*
${TARGET_PREFIX#/}/share/man/*
${TARGET_PREFIX#/}/share/${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

./autogen.sh || exit 1

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

WHOLE_LIBINTL=
if test "$LTO_CFLAGS" != ""; then
	WHOLE_LIBINTL=--enable-whole-libintl
fi
CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME} \
	--disable-shared \
	--enable-silent-rules \
	--disable-curses \
	--enable-relocatable \
	--with-included-gettext \
	$WHOLE_LIBINTL \
	--config-cache"

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
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	RANLIB="$ranlib" \
	./configure ${CONFIGURE_FLAGS} \
		--libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags . gettext-runtime gettext-runtime/libasprintf gettext-tools 

	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	${MAKE} clean

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}${multilibdir}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
