#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=cpio
VERSION=-2.13
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/cpio/cpio-2.12-util.c_no_return_in_nonvoid_fnc.patch
patches/cpio/cpio-check_for_symlinks.patch
patches/cpio/cpio-close_files_after_copy.patch
patches/cpio/cpio-dev_number.patch
patches/cpio/cpio-eof_tape_handling.patch
patches/cpio/cpio-fix_truncation_check.patch
patches/cpio/cpio-open_nonblock.patch
patches/cpio/cpio-pattern-file-sigsegv.patch
patches/cpio/cpio-paxutils-rtapelib_mtget.patch
patches/cpio/cpio-use_new_ascii_format.patch
patches/cpio/cpio-use_sbin_rmt.patch
patches/cpio/cpio-no-mtiocget.patch
patches/cpio/cpio-filemode.patch
"
DISABLED_PATCHES="
patches/cpio/cpio-2.3-lstat.patch
patches/cpio/cpio-2.4.2-svr4compat.patch
patches/cpio/cpio-2.4.2-glibc.patch
patches/cpio/cpio-2.4.2-glibc21.patch
patches/cpio/cpio-2.4.2-longlongdev.patch
patches/cpio/cpio-2.4.2-mtime.patch
patches/cpio/cpio-default_tape_dev.patch
patches/cpio/cpio-2.12-CVE-2019-14866.patch
patches/cpio/cpio-2.12-CVE-2016-2037-out_of_bounds_write.patch
"

BINFILES="
bin/*
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/*
${TARGET_PREFIX#/}/share/info/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--libexecdir=${TARGET_LIBDIR} \
	--disable-nls \
	--with-rmt=/usr/bin/rmt \
	--sbindir=/sbin"

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
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -s" ./configure ${CONFIGURE_FLAGS}
	hack_lto_cflags
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias

	mkdir -p ${THISPKG_DIR}${sysroot}/bin
	ln -sf ${TARGET_BINDIR}/cpio ${THISPKG_DIR}${sysroot}/bin
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
