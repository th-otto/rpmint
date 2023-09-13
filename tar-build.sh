#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=tar
VERSION=-1.34
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/tar/tar-wildcards.patch
patches/tar/tar-backup-spec-fix-paths.patch
patches/tar/tar-paxutils-rtapelib_mtget.patch
patches/tar/tar-ignore_lone_zero_blocks.patch
patches/tar/tar-add_readme-tests.patch
patches/tar/tar-tests-skip-time01-on-32bit-time_t.patch
patches/tar/tar-fix-race-condition.patch
patches/tar/tar-avoid-overflow-in-symlinks-tests.patch
patches/tar/tar-bsc1200657.patch
patches/tar/tar-fix-extract-unlink.patch
patches/tar/tar-go-testsuite-test-hang.patch
patches/tar/tar-bsc1202436.patch
patches/tar/tar-bsc1202436-1.patch
patches/tar/tar-bsc1202436-2.patch
patches/tar/tar-fix-CVE-2022-48303.patch
"
DISABLED_PATHES="
patches/tar/tar-1.29-extract_pathname_bypass.patch
patches/automake/mintelf-config.sub
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

cd "$srcdir"

autoreconf -fiv
rm -f build-aux/config.sub
cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" build-aux/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--program-transform-name='s/^rmt$/gnurmt/'
	--libexecdir=${TARGET_LIBDIR}
	--disable-nls
	--sbindir=/sbin
	--config-cache
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

export RSH=${TARGET_BINDIR}/ssh
export DEFAULT_ARCHIVE_FORMAT="POSIX"
export DEFAULT_RMT_DIR=${TARGET_BINDIR}

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_header_pthread_h=no
gl_have_pthread_h=no
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
	./configure ${CONFIGURE_FLAGS}
	hack_lto_cflags
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	# For avoiding file conflicts with dump/restore
	# mv ${THISPKG_DIR}${sysroot}/sbin/restore ${THISPKG_DIR}${sysroot}/sbin/restore.sh

	install -D -m 644 scripts/backup-specs ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/../etc/backup/backup-specs
	install -D -m 644 -t ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/doc/${PACKAGENAME} README* ABOUT-NLS AUTHORS NEWS THANKS \
							ChangeLog TODO COPYING
	(install -d -m 755 ${THISPKG_DIR}${sysroot}/bin; cd ${THISPKG_DIR}${sysroot}/bin; $LN_S -f ../${TARGET_BINDIR#/}/tar tar)

	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
