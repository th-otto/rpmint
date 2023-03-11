#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=make
VERSION=-4.2.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/make/make-testcases_timeout.diff
patches/make/make-clockskew.patch
"

DISABLED_PATCHES="
patches/make/make-library-search-path.diff
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
"

unpack_archive

cd "$srcdir"

cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--disable-nls \
	--disable-shared \
	--disable-load \
	--disable-nsec-timestamps \
	--config-cache"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
make_cv_sys_gnu_glob=yes
EOF
	append_gnulib_cache
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	STACKSIZE="-Wl,-stack,160k"
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null
	rm -fv ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	rm -fv ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include/gnumake.h
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
