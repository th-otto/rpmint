#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=gettext
VERSION=-0.19.8.1-1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/gettext-gnulib.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
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

(
 cd m4
 rm -f init.m4 amversion.m4 ar-lib.m4 cond.m4 depend.m4 depout.m4 auxdir.m4 install-sh.m4 lispdir.m4 make.m4 missing.m4 options.m4 prog-cc-c-o.m4 runlog.m4 sanity.m4 silent.m4 strip.m4 substnot.m4 tar.m4
)

./autogen.sh || exit 1

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" build-aux/config.sub || exit 1

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

WHOLE_LIBINTL=
if test "$LTO_CFLAGS" != ""; then
	WHOLE_LIBINTL=--enable-whole-libintl
fi
CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME} \
	--disable-shared \
	--disable-threads \
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
