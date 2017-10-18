#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=tar
VERSION=-1.29
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/tar/mintelf-config.patch
patches/tar/tar-wildcards.patch
patches/tar/tar-backup-spec-fix-paths.patch
patches/tar/paxutils-rtapelib_mtget.patch
patches/tar/tar-ignore_lone_zero_blocks.patch
patches/tar/add_readme-tests.patch
patches/tar/add-return-values-to-backup-scripts.patch
patches/tar/tar-1.29-extract_pathname_bypass.patch
"
# patches/tar/tar-recursive--files-from.patch

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/doc/${PACKAGENAME}
etc
bin
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--program-transform-name='s/^rmt$/gnurmt/' \
	--libexecdir=${TARGET_LIBDIR} \
	--disable-nls \
	--sbindir=/sbin \
	--config-cache"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

export RSH=${TARGET_BINDIR}/ssh
export DEFAULT_ARCHIVE_FORMAT="POSIX"
export DEFAULT_RMT_DIR=${TARGET_BINDIR}

append_gnulib_cache()
{
cat <<EOF >>config.cache
ac_cv_func_malloc_0_nonnull=yes
ac_cv_func_realloc_0_nonnull=yes
ac_cv_func_chown_works=yes
ac_cv_func_getgroups_works=yes
am_cv_func_working_getline=yes
gl_cv_func_chown_slash_works=yes
gl_cv_func_chown_ctime_works=yes
gl_cv_func_fflush_stdin=yes
gl_cv_func_getcwd_abort_bug=no
gl_cv_func_getcwd_path_max=yes
gl_cv_func_getcwd_null=yes
gl_cv_func_working_getdelim=yes
gl_cv_func_malloc_0_nonnull=1
gl_cv_func_memchr_works=yes
gl_cv_func_working_mktime=yes
gl_cv_func_printf_sizes_c99=yes
gl_cv_func_printf_infinite=yes
gl_cv_func_printf_infinite_long_double=yes
gl_cv_func_printf_directive_a=yes
gl_cv_func_printf_directive_f=yes
gl_cv_func_printf_directive_n=yes
gl_cv_func_printf_directive_ls=yes
gl_cv_func_printf_positions=yes
gl_cv_func_printf_flag_grouping=yes
gl_cv_func_printf_flag_zero=yes
gl_cv_func_printf_enomem=yes
gl_cv_func_snprintf_truncation_c99=yes
gl_cv_func_snprintf_retval_c99=yes
gl_cv_func_snprintf_directive_n=yes
gl_cv_func_vsnprintf_zerosize_c99=yes
gl_cv_func_signbit=yes
gl_cv_func_signbit_gcc=yes
gl_cv_func_stpncpy=yes
gl_cv_func_working_strerror=yes
gl_cv_func_strerror_0_works=yes
gl_cv_func_memchr_works=yes
gl_cv_func_strstr_works_always=yes
gl_cv_func_strstr_linear=yes
gl_cv_func_strtod_works=yes
gl_cv_func_fcntl_f_dupfd_works=no
gl_cv_func_fdopendir_works=yes
gl_cv_func_gettimeofday_clobber=no
gl_cv_func_link_follows_symlink=no
gl_cv_func_lstat_dereferences_slashed_symlink=yes
gl_cv_func_mkdir_trailing_dot_works=yes
gl_cv_func_mkdir_trailing_slash_works=yes
gl_cv_func_readlink_works=yes
gl_cv_func_setenv_works=yes
gl_cv_func_sleep_works=yes
gl_cv_func_snprintf_usable=yes
gl_cv_func_stat_file_slash=yes
gl_cv_func_unsetenv_works=yes
gl_cv_func_vsnprintf_usable=yes
gl_cv_func_working_utimes=yes
gl_cv_struct_dirent_d_ino=yes
EOF
}

# fu_cv_sys_stat_statfs2_fsize

create_config_cache()
{
cat <<EOF >config.cache
EOF
	append_gnulib_cache
}

for CPU in 020 v4e 000; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS}
	hack_lto_cflags
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	install -D -m 644 scripts/backup-specs ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/../etc/backup/backup-specs
	install -D -m 644 -t ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/doc/${PACKAGENAME} README* ABOUT-NLS AUTHORS NEWS THANKS \
							ChangeLog TODO COPYING
	(install -d -m 755 ${THISPKG_DIR}${sysroot}/bin; cd ${THISPKG_DIR}${sysroot}/bin; $LN_S ../${TARGET_BINDIR#/}/tar tar)

	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
