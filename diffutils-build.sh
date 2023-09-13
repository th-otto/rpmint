#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=diffutils
VERSION=-3.6
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/diffutils/diffutils-diff-3.6-mint.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
"

unpack_archive

cd "$srcdir"

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" build-aux/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--sysconfdir=/etc
	--disable-nls
	--disable-shared
	--config-cache
"
STACKSIZE="-Wl,-stack,128k"

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
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	hack_lto_cflags

	# ignore any PR program found on the build system
cat << EOF >> lib/config.h
#undef PR_PROGRAM
#define PR_PROGRAM "/usr/bin/pr"
EOF

	# make sure man-pages are not regenerated using help2man,
	# it tries to execute the just build programs
	touch man/*.1

	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
