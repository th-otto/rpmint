#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=rpm
VERSION=-4.14.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/rpm/rpm-4.12.0.1-fix-bashisms.patch
patches/rpm/usr-lib-sysimage-rpm.patch
patches/rpm/debugedit.patch
patches/rpm/localetag.patch
patches/rpm/ignore-auxv.patch
patches/rpm/nameversioncompare.patch
patches/rpm/dbfsync.patch
patches/rpm/dbrointerruptable.patch
patches/rpm/refreshtestarch.patch
patches/rpm/waitlock.patch
patches/rpm/suspendlock.patch
patches/rpm/brp.patch
patches/rpm/brpcompress.patch
patches/rpm/checkfilesnoinfodir.patch
patches/rpm/finddebuginfo.patch
patches/rpm/findksyms.patch
patches/rpm/findlang.patch
patches/rpm/macrosin.patch
patches/rpm/modalias.patch
patches/rpm/platformin.patch
patches/rpm/rpmpopt.patch
patches/rpm/rpmrc.patch
patches/rpm/taggedfileindex.patch
patches/rpm/rpmqpack.patch
patches/rpm/build.patch
patches/rpm/rpm-shorten-changelog.patch
patches/rpm/whatrequires-doc.patch
patches/rpm/requires-ge-macro.patch
patches/rpm/finddebuginfo-absolute-links.patch
patches/rpm/firmware.patch
patches/rpm/specfilemacro.patch
patches/rpm/modalias-encode.patch
patches/rpm/disttag-macro.patch
patches/rpm/debugsubpkg.patch
patches/rpm/debuglink.patch
patches/rpm/debuginfo-mono.patch
patches/rpm/lazystatfs.patch
patches/rpm/safeugid.patch
patches/rpm/noprereqdeprec.patch
patches/rpm/initscriptsprov.patch
patches/rpm/remove-translations.patch
patches/rpm/headeradddb.patch
patches/rpm/dbprivate.patch
patches/rpm/nobuildcolor.patch
patches/rpm/fileattrs.patch
patches/rpm/nomagiccheck.patch
patches/rpm/assumeexec.patch
patches/rpm/mono-find-requires.patch
patches/rpm/rpm-deptracking.patch
patches/rpm/langnoc.patch
patches/rpm/headerchk2.patch
patches/rpm/brp-compress-no-img.patch
patches/rpm/weakdepscompat.patch
patches/rpm/checksepwarn.patch
patches/rpm/enable-postin-scripts-error.patch
patches/rpm/rpm-findlang-inject-metainfo.patch
patches/rpm/emptymanifest.patch
patches/rpm/find-lang-qt-qm.patch
patches/rpm/debugedit-macro.patch
patches/rpm/pythondistdeps.patch
patches/rpm/debugedit-bnc1076819.patch
patches/rpm/hardlinks.patch
patches/rpm/auto-config-update-aarch64-ppc64le.patch
patches/rpm/mint.patch
"
DISABLED_PATCHES="
patches/rpm/remove-brp-strips.patch
"

POST_INSTALL_SCRIPTS="
patches/rpm/RPM-HOWTO.tar.bz2
patches/rpm/rpm-suse_macros
patches/rpm/rpm-mint_macros
patches/rpm/rpmsort
patches/rpm/rpmconfigcheck
patches/rpm/sysconfig.services-rpm
patches/rpm/rpmconfigcheck.service
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/doc/${PACKAGENAME}
"

unpack_archive

cd "$MINT_BUILD_DIR"

rm -rf sqlite
rm -rf beecrypt
rm -f rpmdb/db.h
rm -f m4/libtool.m4
rm -f m4/lt*.m4
autoreconf -fi

sed -e 's/@suse_version@/%{?suse_version}%{!?suse_version:0}/' \
    -e 's/@sles_version@/%{?sles_version}%{!?sles_version:0}/' \
    -e 's/@ul_version@/%{?ul_version}%{!?ul_version:0}/' \
    -e '/@is_opensuse@%{?is_opensuse:nomatch}/d' \
    -e 's/@is_opensuse@/%{?is_opensuse}%{!?is_opensuse:0}/' \
    -e '/@leap_version@%{?leap_version:nomatch}/d' \
    -e 's/@leap_version@/%{?leap_version}%{!?leap_version:0}/' \
  < "${BUILD_DIR}/patches/rpm/rpm-suse_macros" > suse_macros


COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--mandir=${prefix}/share/man \
	--infodir=${prefix}/share/info \
	--libdir=${prefix}/lib \
	--sysconfdir=${TARGET_SYSCONFDIR} \
	--localstatedir=/var \
	--sharedstatedir=/var/lib \
	--with-rundir=/run \
	--with-lua \
	--with-external-db \
	--docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME} \
	--with-vendor="${VENDOR}" \
	--without-archive \
	--with-selinux \
	--with-crypto=beecrypt \
	--without-internal-beecrypt \
	--with-acl \
	--with-cap \
	--disable-shared \
	--disable-python \
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

ALL_CPUS=020
for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} \
		--libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags

	rm -rf autom4te.cache config.h.in.orig

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
