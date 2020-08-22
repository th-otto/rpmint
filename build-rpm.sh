#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=rpm
VERSION=-4.14.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/rpm/rpm-0001-Fix-bashisms.patch
patches/rpm/rpm-0002-Change-db-path-to-usr-lib-sysimage-rpm.patch
patches/rpm/rpm-0003-Make-debugedit-build-without-dwarf.h.patch
patches/rpm/rpm-0004-Convert-output-to-the-current-locale.-Assumes-utf8-i.patch
patches/rpm/rpm-0005-Ignore-auxv.patch
patches/rpm/rpm-0006-Also-compare-the-name-arch-and-not-only-the-version-.patch
patches/rpm/rpm-0007-Support-a-database-local-fsync-setting.-Needs-berkel.patch
patches/rpm/rpm-0008-Make-db-r-o-interruptible.patch
patches/rpm/rpm-0009-Also-test-architecture-in-refresh-test-when-not-colo.patch
patches/rpm/rpm-0010-Fix-global-DB_PRIVATE-lock-code-fix-recursion-counte.patch
patches/rpm/rpm-0011-Suspend-exclusive-database-lock-when-scriptlets-get-.patch
patches/rpm/rpm-0012-brp-compress.patch
patches/rpm/rpm-0013-Exclude-usr-share-info-dir-from-check-files.patch
patches/rpm/rpm-0014-find-debuginfo.patch
patches/rpm/rpm-0015-find-ksyms.patch
patches/rpm/rpm-0016-find-lang.patch
patches/rpm/rpm-0017-Adjust-default-values-in-macros.in.patch
patches/rpm/rpm-0018-modalias-find-supplements.patch
patches/rpm/rpm-0019-Adjust-default-values-in-platform.in.patch
patches/rpm/rpm-0020-Add-distribution-name-to-rpmpopt.patch
patches/rpm/rpm-0021-Adjust-some-flags-in-rpmrc.patch
patches/rpm/rpm-0022-This-used-to-be-the-taggedfileindex-patch-but-it-s-g.patch
patches/rpm/rpm-0023-rpmqpack.patch
patches/rpm/rpm-0024-build.patch
patches/rpm/rpm-0025-rpm-short-changelog.patch
patches/rpm/rpm-0026-whatrequires-doc.patch
patches/rpm/rpm-0027-requires-ge-macro.patch
patches/rpm/rpm-0028-From-Jan-Blunck-jblunck-suse.de.patch
patches/rpm/rpm-0029-Add-firmware-files-in-lib-firmware-into-RPM-provides.patch
patches/rpm/rpm-0030-specfilemacro.patch
patches/rpm/rpm-0031-Module-aliases-modinfo-F-alias-module-may-contain-sp.patch
patches/rpm/rpm-0032-Hmm-SUSE-doesn-t-use-it-so-what-s-the-purpose-of-thi.patch
patches/rpm/rpm-0033-debugsubpkg.patch
patches/rpm/rpm-0034-debuglink.patch
patches/rpm/rpm-0035-debuginfo-mono.patch
patches/rpm/rpm-0036-Prefer-sys-vfs.h-as-statvfs-stats-all-filesystems-ag.patch
patches/rpm/rpm-0037-safeugid.patch
patches/rpm/rpm-0038-no-prereq-deprec.patch
patches/rpm/rpm-0039-sysvinitdeps.patch
patches/rpm/rpm-0040-remove-translations.patch
patches/rpm/rpm-0041-Add-rpmtsHeaderAddDB-and-rpmtsHeaderRemoveDB-so-that.patch
patches/rpm/rpm-0042-db-private.patch
patches/rpm/rpm-0043-Disable-file-coloring-for-SUSE-systems.patch
patches/rpm/rpm-0044-fileattrs.patch
patches/rpm/rpm-0045-Don-t-let-rpm-complain-about-a-missing-etc-magic.mgc.patch
patches/rpm/rpm-0046-assumeexec.patch
patches/rpm/rpm-0047-mono-find-requires.patch
patches/rpm/rpm-0048-Disable-dependency-tracking-for-build.patch
patches/rpm/rpm-0049-lang-no-c.patch
patches/rpm/rpm-0050-headerchk2.patch
patches/rpm/rpm-0051-brp-compress-no-img.patch
patches/rpm/rpm-0052-weak-deps-compat.patch
patches/rpm/rpm-0053-check-sep-warn.patch
patches/rpm/rpm-0054-enable-postin-scripts-error.patch
patches/rpm/rpm-0055-rpm-findlang-inject-metainfo.patch
patches/rpm/rpm-0056-empty-manifest.patch
patches/rpm/rpm-0057-find-lang-qt-qm.patch
patches/rpm/rpm-0058-debugedit-macro.patch
patches/rpm/rpm-0059-python-dist-deps.patch
patches/rpm/rpm-0060-debugedit-bnc1076819.patch
patches/rpm/rpm-0061-hardlinks.patch
patches/rpm/rpm-0062-auto-config-update-aarch64-ppc64le.patch
patches/rpm/rpm-0063-brp.patch
patches/rpm/rpm-0064-Define-possible-missing-constants-for-pathconf-sysco.patch
patches/rpm/rpm-0065-Check-wether-nanosleep-is-available.patch
patches/rpm/rpm-0066-Check-wether-mkdtemp-is-available.patch
patches/rpm/rpm-0067-Fix-detection-of-__progname.patch
patches/rpm/rpm-0068-Remove-dependance-on-__errno_location.patch
patches/rpm/rpm-0069-Move-library-dependant-cppflags-to-globals.patch
patches/rpm/rpm-0070-Do-not-blindly-add-fPIC-to-RPMCFLAGS-libtool-takes-c.patch
patches/rpm/rpm-0071-Fix-tests-wether-lzma-supports-multi-threading.patch
patches/rpm/rpm-0072-Fix-test-for-lmagic-which-might-need-zlib.patch
patches/rpm/rpm-0073-Only-use-pthreads-if-available.patch
patches/rpm/rpm-0074-Add-missing-include-of-rpmug.h.patch
patches/rpm/rpm-0075-Add-detection-of-default-machine-m68k.patch
patches/rpm/rpm-0076-Add-missing-include-of-signal.h.patch
patches/rpm/rpm-0077-Fix-type-of-callback-functions.patch
patches/rpm/rpm-0078-Avoid-a-warning-using-64bit-constant.patch
patches/rpm/rpm-0079-MiNT-attribute-visibility-is-not-available.patch
patches/rpm/rpm-0080-Only-use-dlopen-if-available.patch
patches/rpm/rpm-0082-coldfire.patch
patches/rpm/rpm-0083-Fix-some-mismatch-between-open-mode-permissions.patch
patches/rpm/rpm-0084-Remove-fstack-protector-as-it-requires-all-packages-.patch
patches/rpm/rpm-0085-Remove-i18n-translation-in-rpmmalloc.c-as-it-is-refe.patch
patches/rpm/rpm-mintelf-config.patch
patches/rpm/rpm-tools.patch
"
DISABLED_PATCHES="
patches/rpm/rpm-remove-brp-strips.patch
patches/rpm/rpm-lua-compat.patch
"

POST_INSTALL_SCRIPTS="
patches/rpm/rpm-howto.tar.bz2
patches/rpm/rpm-suse_macros
patches/rpm/rpm-mint_macros
patches/rpm/rpm-rpmsort
patches/rpm/rpm-rpmconfigcheck
patches/rpm/rpm-sysconfig.services-rpm
patches/rpm/rpm-rpmconfigcheck.service
"

BINFILES="
bin/*
var
${TARGET_SYSCONFDIR#/}
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/lib/rpm
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/doc/packages/${PACKAGENAME}
${TARGET_PREFIX#/}/sbin/*
${TARGET_PREFIX#/}/src/packages
"

unpack_archive

cd "$MINT_BUILD_DIR"

rm -rf sqlite
rm -rf beecrypt
rm -f rpmdb/db.h
rm -f m4/libtool.m4
rm -f m4/lt*.m4
autoreconf -fi
# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/rpm/rpm-mintelf-config.patch"

sed -e 's/@suse_version@/%{?suse_version}%{!?suse_version:0}/' \
    -e 's/@sles_version@/%{?sles_version}%{!?sles_version:0}/' \
    -e 's/@ul_version@/%{?ul_version}%{!?ul_version:0}/' \
    -e '/@is_opensuse@%{?is_opensuse:nomatch}/d' \
    -e 's/@is_opensuse@/%{?is_opensuse}%{!?is_opensuse:0}/' \
    -e '/@leap_version@%{?leap_version:nomatch}/d' \
    -e 's/@leap_version@/%{?leap_version}%{!?leap_version:0}/' \
  < "${BUILD_DIR}/patches/rpm/rpm-mint_macros" > ${VENDOR}_macros

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--mandir=${prefix}/share/man \
	--infodir=${prefix}/share/info \
	--libdir=${prefix}/lib \
	--sysconfdir=${TARGET_SYSCONFDIR} \
	--localstatedir=/var \
	--sharedstatedir=/var/lib \
	--with-rundir=/var/run \
	--with-lua \
	--with-external-db \
	--docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME} \
	--with-vendor="${VENDOR}" \
	--without-archive \
	--without-selinux \
	--with-crypto=beecrypt \
	--without-internal-beecrypt \
	--without-acl \
	--without-cap \
	--disable-shared \
	--disable-python \
	--disable-plugins \
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -DLUA_COMPAT_MODULE=1" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} \
		--libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags

	rm -rf autom4te.cache config.h.in.orig

	${MAKE} || exit 1
	buildroot="${THISPKG_DIR}${sysroot}"
	_fillupdir=/var/adm/fillup-templates
	
	${MAKE} DESTDIR="${buildroot}" install
	mkdir -p ${buildroot}/bin
	ln -s ${TARGET_PREFIX}/bin/rpm ${buildroot}/bin/rpm
	ln -s ../db4/db.h ${buildroot}${TARGET_PREFIX}/include/rpm/db.h
	mkdir -p ${buildroot}/usr/sbin
	mkdir -p ${buildroot}/var/run

	install -m 755 ${BUILD_DIR}/patches/rpm/rpm-rpmconfigcheck ${buildroot}/usr/sbin/rpmconfigcheck
	mkdir -p ${buildroot}/usr/lib/systemd/system
	install -m 644 ${BUILD_DIR}/patches/rpm/rpm-rpmconfigcheck.service ${buildroot}/usr/lib/systemd/system/rpmconfigcheck.service
	cp -a ${VENDOR}_macros ${buildroot}/usr/lib/rpm
	mkdir -p ${buildroot}/usr/lib/rpm/macros.d
	mkdir -p ${buildroot}/usr/lib/rpm/${VENDOR}
	ln -s ../${VENDOR}_macros ${buildroot}/usr/lib/rpm/${VENDOR}/macros
	for d in BUILD RPMS SOURCES SPECS SRPMS BUILDROOT ; do
	  mkdir -p ${buildroot}/usr/src/packages/$d
	  chmod 755 ${buildroot}/usr/src/packages/$d
	done
	for d in ${buildroot}/usr/lib/rpm/platform/*-mint/macros ; do
	  dd=${d%%-mint/macros}
	  dd=${dd##*/}
	  mkdir ${buildroot}/usr/src/packages/RPMS/$dd
	  chmod 755 ${buildroot}/usr/src/packages/RPMS/$dd
	done
	mkdir -p ${buildroot}/usr/lib/sysimage/rpm
	mkdir -p ${buildroot}/var/lib/rpm
	chmod 755 doc/manual
	mkdir -p ${buildroot}${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME}
	cp -pvr doc/manual ${buildroot}${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME}
	rm -rf ${buildroot}${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME}/manual/Makefile*
	( cd ${buildroot}${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME}/ ;
	  tar xvf ${BUILD_DIR}/patches/rpm/rpm-howto.tar.bz2
	)
	  
	rm -f ${buildroot}/usr/lib/rpmpopt
	rm -rf ${buildroot}/usr/share/man/{fr,ja,ko,pl,ru,sk}
	mkdir -p ${buildroot}${_fillupdir}
	install -c -m 644 ${BUILD_DIR}/patches/rpm/rpm-sysconfig.services-rpm ${buildroot}${_fillupdir}/sysconfig.services-rpm
	rm -f ${buildroot}/usr/lib/rpm/cpanflute ${buildroot}/usr/lib/rpm/cpanflute2
	install -m 755 ${BUILD_DIR}/patches/rpm/rpm-rpmsort ${buildroot}/usr/lib/rpm/rpmsort
	install -m 755 scripts/find-supplements{,.ksyms} ${buildroot}/usr/lib/rpm
	: install -m 755 scripts/firmware.prov ${buildroot}/usr/lib/rpm
	install -m 755 scripts/debuginfo.prov ${buildroot}/usr/lib/rpm
	rm -f ${buildroot}/usr/lib/locale ${buildroot}/usr/lib/rpmrc
	mkdir -p ${buildroot}/etc/rpm
	chmod 755 ${buildroot}/etc/rpm
# remove some nonsense or non-working scripts
	pushd ${buildroot}/usr/lib/rpm/
	for f in rpm2cpio.sh rpm.daily rpmdiff* rpm.log rpm.xinetd freshen.sh u_pkg.sh \
	         magic magic.mgc magic.mime* rpmfile *.pl javadeps brp-redhat \
	         brp-strip-static-archive vpkg-provides*.sh http.req sql.req tcl.req \
	         brp-sparc64-linux brp-strip-comment-note brp-java-gcjcompile
	do
	    rm -f $f
	done
	popd
	rm -rf ${buildroot}/${TARGET_LIBDIR}/python*
	sh ${buildroot}/usr/lib/rpm/find-lang.sh ${buildroot} rpm
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir/charset.alias

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
