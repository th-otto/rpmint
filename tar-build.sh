#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=tar
VERSION=-1.29
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/tar/tar-mintelf-config.patch
patches/tar/tar-wildcards.patch
patches/tar/tar-backup-spec-fix-paths.patch
patches/tar/tar-paxutils-rtapelib_mtget.patch
patches/tar/tar-ignore_lone_zero_blocks.patch
patches/tar/tar-add_readme-tests.patch
patches/tar/tar-add-return-values-to-backup-scripts.patch
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
