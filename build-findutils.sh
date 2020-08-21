#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=findutils
VERSION=-4.7.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/findutils/findutils-4.7-xautofs.patch
patches/findutils/findutils-mintelf-config.patch
patches/findutils/findutils-4.7-mint.patch
patches/findutils/findutils-notexinfo-clean.patch
"

DISABLED_PATCHES="
patches/findutils/findutils-sv-bug-48030-find-exec-plus-does-not-pass-all-arguments.patch
patches/findutils/findutils-4.6-mint.patch
"

# patches/findutils/findutils-mktemp.patch

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/libexec/find/*
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man5/*
${TARGET_PREFIX#/}/share/info/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--disable-nls \
	--disable-shared \
	--localstatedir=/var/lib \
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
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache
	STACKSIZE="-Wl,-stack,128k"
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir \
	--libexecdir='${exec_prefix}/libexec/find'$multilibexecdir

	hack_lto_cflags

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
