Provides:       rpminst
Requires(post): %fillup_prereq
Summary:        The RPM Package Manager
License:        GPL-2.0+
Group:          System/Packages
Version:        4.14.1
Release:        3.1
# quilt patches start here
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#
# avoid bootstrapping problem
%define _binary_payload w9.bzdio

%description
RPM Package Manager is the main tool for managing the software packages
of the SUSE Linux distribution.

RPM can be used to install and remove software packages. With rpm, it
is easy to update packages.  RPM keeps track of all these manipulations
in a central database.	This way it is possible to get an overview of
all installed packages.  RPM also supports database queries.

%package devel
Summary:        Development files for librpm
Group:          Development/Libraries/C and C++
Requires:       rpm = %{version}
# for people confusing the one with the other
Recommends:     rpm-build = %{version}
Requires:       popt-devel

%description devel
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs which
manipulate RPM packages and databases and are intended to make it
easier to create graphical package managers or any other tools that
need an intimate knowledge of RPM packages in order to function.

%package build
Summary:        Tools and Scripts to create rpm packages
Group:          System/Packages
Requires:       rpm = %{version}
Provides:       rpm:%_bindir/rpmbuild
Provides:       rpmbuild
# SUSE's build essentials
Requires:       binutils
Requires:       bzip2
Requires:       coreutils
Requires:       diffutils
Requires:       dwz
Requires:       file
Requires:       findutils
Requires:       gawk
Requires:       gcc
#Requires:       gcc-PIE
Requires:       gettext-tools
Requires:       glibc-devel
Requires:       glibc-locale
Requires:       grep
Requires:       gzip
Requires:       make
Requires:       patch
Requires:       perl-base
Requires:       sed
Requires:       systemd-rpm-macros
Requires:       tar
Requires:       util-linux
Requires:       which
Requires:       xz
# drop candidates
Requires:       cpio
Requires:       file

%description build
If you want to build a rpm, you need this package. It provides rpmbuild
and requires some packages that are usually required.

%prep
%setup -q -n rpm-%{version}

%build
export CFLAGS="%{optflags} -ffunction-sections"
export LDFLAGS="-Wl,-Bsymbolic-functions -ffunction-sections"
%ifarch alpha
export CFLAGS="-g -O0 -fno-strict-aliasing -ffunction-sections"
%endif

%ifarch %arm
BUILDTARGET="--build=%{_target_cpu}-suse-linux-gnueabi"
%else
BUILDTARGET="--build=%{_target_cpu}-suse-linux"
%endif

autoreconf -fi
./configure --disable-dependency-tracking --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
--libdir=%{_libdir} --sysconfdir=/etc --localstatedir=/var --sharedstatedir=/var/lib --with-lua \
--without-external-db \
--with-vendor=suse \
--with-rundir=/run \
--without-archive \
--with-selinux --with-internal-beecrypt \
--with-acl --with-cap --enable-shared %{?with_python: --enable-python} $BUILDTARGET

rm po/de.gmo
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/usr/lib
mkdir -p %{buildroot}/usr/share/locale
ln -s ../share/locale %{buildroot}/usr/lib/locale
%make_install
mkdir -p %{buildroot}/bin
ln -s /usr/bin/rpm %{buildroot}/bin/rpm
install -m 644 db3/db.h %{buildroot}/usr/include/rpm
# remove .la file and the static variant of libpopt
# have to remove the dependency from other .la files as well
for f in %{buildroot}/%{_libdir}/*.la; do
    sed -i -e "s,/%_lib/libpopt.la,-lpopt,g" $f
done
mkdir -p %{buildroot}/usr/sbin
install -m 755 %{SOURCE8} %{buildroot}/usr/sbin
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 %{SOURCE13} %{buildroot}/usr/lib/systemd/system/
cp -a suse_macros %{buildroot}/usr/lib/rpm
mkdir -p %{buildroot}/usr/lib/rpm/macros.d
mkdir -p %{buildroot}/usr/lib/rpm/suse
ln -s ../suse_macros %{buildroot}/usr/lib/rpm/suse/macros
for d in BUILD RPMS SOURCES SPECS SRPMS BUILDROOT ; do
  mkdir -p %{buildroot}/usr/src/packages/$d
  chmod 755 %{buildroot}/usr/src/packages/$d
done
for d in %{buildroot}/usr/lib/rpm/platform/*-linux/macros ; do
  dd=${d%%-linux/macros}
  dd=${dd##*/}
  mkdir %{buildroot}/usr/src/packages/RPMS/$dd
  chmod 755 %{buildroot}/usr/src/packages/RPMS/$dd
done
mkdir -p %{buildroot}/usr/lib/sysimage/rpm
mkdir -p %{buildroot}/var/lib/rpm
gzip -9 %{buildroot}/%{_mandir}/man[18]/*.[18]
export RPM_BUILD_ROOT
%ifarch s390x
[ -f scripts/brp-%_arch-linux ] && sh scripts/brp-%_arch-linux
%endif
chmod 755 doc/manual
rm -rf doc/manual/Makefile*
rm -f %{buildroot}/usr/lib/rpmpopt
rm -rf %{buildroot}%{_mandir}/{fr,ja,ko,pl,ru,sk}
rm -f %{buildroot}%{_prefix}/share/locale/de/LC_MESSAGES/rpm.mo
mkdir -p %{buildroot}%{_fillupdir}
install -c -m0644 %{SOURCE9} %{buildroot}%{_fillupdir}/
rm -f %{buildroot}/usr/lib/rpm/cpanflute %{buildroot}/usr/lib/rpm/cpanflute2
install -m 755 %{SOURCE5} %{buildroot}/usr/lib/rpm
install -m 755 scripts/find-supplements{,.ksyms} %{buildroot}/usr/lib/rpm
install -m 755 scripts/firmware.prov %{buildroot}/usr/lib/rpm
install -m 755 scripts/debuginfo.prov %{buildroot}/usr/lib/rpm
rm -f %{buildroot}/usr/lib/locale %{buildroot}/usr/lib/rpmrc
mkdir -p %{buildroot}/etc/rpm
chmod 755 %{buildroot}/etc/rpm
# remove some nonsense or non-working scripts
pushd %{buildroot}/usr/lib/rpm/
for f in rpm2cpio.sh rpm.daily rpmdiff* rpm.log rpm.xinetd freshen.sh u_pkg.sh \
         magic magic.mgc magic.mime* rpmfile *.pl javadeps brp-redhat \
         brp-strip-static-archive vpkg-provides*.sh http.req sql.req tcl.req \
         brp-sparc64-linux brp-strip-comment-note brp-java-gcjcompile
do
    rm -f $f
done
for i in /usr/share/automake-*/*; do
  if test -f "$i" && test -f "${i##*/}"; then
    rm -f "${i##*/}"
  fi
done
popd
%ifarch aarch64 ppc64le riscv64
install -m 755 config.guess %{buildroot}/usr/lib/rpm
install -m 755 config.sub %{buildroot}/usr/lib/rpm
%endif
rm -rf %{buildroot}/%{_libdir}/python%{py_ver}
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/rpm-plugins/*.la
sh %{buildroot}/usr/lib/rpm/find-lang.sh %{buildroot} rpm
# On arm the kernel architecture is ignored. Not the best idea, but lets stay compatible with other distros
%ifarch armv7hl armv6hl
# rpm is using the host_cpu as default for the platform, but armv6/7hl is not known by the kernel.
# so we need to enforce the platform here.
echo -n "%{_target_cpu}-suse-linux-gnueabi" > %{buildroot}/etc/rpm/platform
%endif

%post
%{fillup_only -an services}

# var/lib/rpm migration: set forwards compatible symlink for /usr/lib/sysimage/rpm so scriptlets in same transaction will still work
if test ! -L var/lib/rpm -a -f var/lib/rpm/Packages -a ! -f usr/lib/sysimage/rpm/Packages ; then
  rmdir usr/lib/sysimage/rpm
  ln -s ../../../var/lib/rpm usr/lib/sysimage/rpm
fi

test -f usr/lib/sysimage/rpm/Packages || rpmdb --initdb

%posttrans
# var/lib/rpm migration
if test ! -L var/lib/rpm ; then
  # delete no longer maintained databases
  rm -f var/lib/rpm/Filemd5s var/lib/rpm/Filedigests var/lib/rpm/Requireversion var/lib/rpm/Provideversion

  if test -f var/lib/rpm/Packages ; then
    echo "migrating rpmdb from /var/lib/rpm to /usr/lib/sysimage/rpm..."

    # remove forwards compatible symlink
    if test -L usr/lib/sysimage/rpm ; then
      rm -f usr/lib/sysimage/rpm
      mkdir -p usr/lib/sysimage/rpm
    fi

    mv -f var/lib/rpm/.[!.]* usr/lib/sysimage/rpm/
    mv -f var/lib/rpm/* usr/lib/sysimage/rpm/
  fi
  rmdir var/lib/rpm && ln -s ../../usr/lib/sysimage/rpm var/lib/rpm
fi

%files -f rpm.lang
%defattr(-,root,root)
%license 	COPYING
%doc 	doc/manual
%doc    RPM-HOWTO
	/etc/rpm
	/bin/rpm
	/usr/bin/*
        %exclude /usr/bin/rpmbuild
	/usr/sbin/rpmconfigcheck
	/usr/lib/systemd/system/rpmconfigcheck.service
	/usr/lib/rpm
	%{_libdir}/rpm-plugins
	%{_libdir}/librpm.so.*
	%{_libdir}/librpmbuild.so.*
	%{_libdir}/librpmio.so.*
	%{_libdir}/librpmsign.so.*
%doc	%{_mandir}/man[18]/*.[18]*
%dir 	/usr/lib/sysimage
%dir 	/usr/lib/sysimage/rpm
%dir 	/var/lib/rpm
%dir 	%attr(755,root,root) /usr/src/packages/BUILD
%dir 	%attr(755,root,root) /usr/src/packages/SPECS
%dir 	%attr(755,root,root) /usr/src/packages/SOURCES
%dir 	%attr(755,root,root) /usr/src/packages/SRPMS
%dir	%attr(755,root,root) /usr/src/packages/RPMS
%dir	%attr(755,root,root) /usr/src/packages/BUILDROOT
%dir	%attr(755,root,root) /usr/src/packages/RPMS/*
	%{_fillupdir}/sysconfig.services-rpm

%files build
%defattr(-,root,root)
/usr/bin/rpmbuild

%files devel
%defattr(644,root,root,755)
	/usr/include/rpm
        %{_libdir}/librpm.so
        %{_libdir}/librpmbuild.so
        %{_libdir}/librpmio.so
        %{_libdir}/librpmsign.so
        %{_libdir}/pkgconfig/rpm.pc

%changelog
* Thu Mar  1 2018 mls@suse.de
- remove no longer needed and now harmful extcond patch
  [bnc#1083539]
  dropped patch: extcond.diff
* Thu Feb 22 2018 fvogt@suse.com
- Use %%license (boo#1082318)
* Thu Feb 22 2018 mls@suse.de
- split riscv64 part from auto-config-update-aarch64-ppc64le.diff
  to make the change rust-proof.
  new patch: auto-config-update-riscv64.diff
* Thu Feb 15 2018 schwab@suse.de
- auto-config-update-aarch64-ppc64le.diff: Update for riscv64 and enable
  it there
* Wed Feb 14 2018 mls@suse.de
- change disk usage handling to take hardlinks into account
  [bnc#720150]
  new patch: hardlinks.diff
* Wed Feb  7 2018 msuchanek@suse.com
- Use ksym-provides tool (bsc#1077692).
* Wed Feb  7 2018 dimstar@opensuse.org
- Update %%remove_and_set: This macro needs no fallback to
  /var/adm/fillup-templates, as it does not work on files provided
  by the packages, but rather constructs temporary files inside
  fillup_dir.
* Mon Feb  5 2018 mls@suse.de
- remove shebang from python-macro-helper
* Wed Jan 31 2018 mls@suse.de
- update to rpm-4.14.1
  * Fix arbitrary code execution when evaluating common
    python-related macros
  * new artifact file marker
  * less strict signature header verification [bnc#1078284]
- dropped patches:
  * bigarchive.diff
  * editdwarf.diff
  * hardlink.diff
  * rofs.diff
  * transfiletriggerpostun.diff
* Mon Jan 22 2018 rguenther@suse.com
- fix debugedit relocation offset computation (boo#1076819)
  new patch: debugedit-bnc1076819.diff
* Fri Jan  5 2018 mls@suse.de
- fix signature header writing if the archive size is bigger
  than 2 GByte
  new patch: bigarchive.diff
* Tue Jan  2 2018 mls@suse.de
- remove shebang from pythondistdeps.py
  new patch: pythondistdeps.diff
* Tue Dec 19 2017 jengelh@inai.de
- Update RPM groups
* Fri Dec 15 2017 mls@suse.de
- patch debugedit so that it also handles the .debug.macro section
  new patch: debugedit-macro.diff
* Thu Dec  7 2017 mls@suse.de
- switch build id generation to "alldebug" mode
* Mon Dec  4 2017 kukuk@suse.com
- Replace PreReq fillup with Requires(post), so that we can
  deinstall it later if we don't need it anymore
* Fri Dec  1 2017 mls@suse.de
- update to rpm-4.14.0
  * new with/without/unless rich dependencies
  * multifile optimized debuginfo packages
  * much improved macro engine
- dropped patches:
  * 0001-set-SOURCE_DATE_EPOCH-from-changelog.patch
  * 0002-Extend-changelog-to-support-full-timestamps-903.patch
  * 0003-Allow-SOURCE_DATE_EPOCH-to-override-file-timestamps.patch
  * 0004-Allow-SOURCE_DATE_EPOCH-to-override-RPMTAG_BUILDTIME.patch
  * buildidprov.diff
  * changes-doc.diff
  * convertdb1static.diff
  * debugedit-canon-fix.diff
  * debugedit-comp-dir.diff
  * debugsource-package.diff
  * find-lang-python.patch
  * nobfd.diff
  * normalize_blocksize.diff
  * perlprov-package.diff
  * perlprov.diff
  * python3-abi-kind.diff
  * rpmrctests.diff
- new patches (backports from master):
  * editdwarf.diff
  * rofs.diff
  * transfiletriggerpostun.diff
  * hardlink.diff
* Thu Nov 23 2017 rbrown@suse.com
- Replace references to /var/adm/fillup-templates with new
  %%_fillupdir macro (boo#1069468)
* Tue Nov  7 2017 rbrown@suse.com
- Introduce new %%_fillupdir macro for fillup-templates location
- Set %%_fillupdir macro to /usr/share/fillup-templates
- Change fillup macros to support new %%_fillupdir in addition
  to old /var/adm/fillup-templates location
* Mon Nov  6 2017 mls@suse.de
- Make %%post compatibility symlink creation more resiliant
* Mon Nov  6 2017 rbrown@suse.com
- Correct %%post compatibility symlink for /usr/lib/sysimage/rpm
* Thu Oct 26 2017 rbrown@suse.com
- Remove usr-lib-rpmdb.patch
- Add usr-lib-sysimage-rpm.patch to locate rpmdb to
  /usr/lib/sysimage/rpm after discussions with upstream
- Migrates existing rpmdb in /var/lib/rpm to /usr/lib/sysimage/rpm
* Thu Oct  5 2017 rbrown@suse.com
- Add usr-lib-rpmdb.patch to locate rpmdb to /usr/lib/rpmdb
- Migrates existing rpmdb in /var/lib/rpm to /usr/lib/rpmdb
* Fri Sep  8 2017 mmarek@suse.com
- Generate ksym() dependencies for SLE if %%is_opensuse is unset
  (bsc#981083).
* Tue Aug 29 2017 mmarek@suse.com
- Drop %%supplements_kernel_module, as it is broken, undocumented
  and is not used by anybody (bsc#981083).
  dropped: modalias-kernel_module.diff
  refreshed: modalias-encode.diff
- Split fileattrs for kernel and kmps, do not pass around %%name and
  simplify the helpers
  refreshed: fileattrs.diff, modalias.diff
  dropped: symset-table, helperenv.diff, modalias-no-kgraft.diff
* Tue Aug 22 2017 fvogt@suse.com
- Change Supplements in rpm-suse_macros to not depend on bundle-lang-other
  anymore, it does not exist in Leap and will likely be dropped from TW.
* Wed Jul 26 2017 rguenther@suse.com
- Amend finddebuginfo.diff to adjust readelf -Wn pattern matching
  to account for fixed readelf no longer emitting spurious newlines
  with -W.
* Mon Jul 10 2017 dimstar@opensuse.org
- Drop net-tools Requires from rpm-build: net-tools only ships
  uninteresting binaries. Most people would probably rather have
  net-tools-depreacted expected (e.g. ifconfig), but as we did not
  pull this in neither, we can just ignore this.
* Wed Jul  5 2017 ngompa13@gmail.com
- Define %%_sharedstatedir as /var/lib, which is the path for
  shared state content in Red Hat/Fedora; Mageia; and Debian/Ubuntu.
  The old path (/usr/com) isn't recognized by FHS, whereas /var/lib
  is recognized as suitable for this purpose.
- Change the RPM binary payload from old-lzma to xz,
  in line with payload settings for RH/Fedora and Mageia
- Backport upstream commit to read changelog entries with full
  timestamps
  New patch: changes-doc.diff
* Thu Jun 15 2017 alarrosa@suse.com
- Added a %%rpm_vercmp macro which accepts two versions as parameters and
  returns -1, 0, 1 if the first version is less than, equal or
  greater than the second version respectively.
- Added a %%pkg_version macro that accepts a package or capability name
  as argument and returns the version number of the installed package. If
  no package provides the argument, it returns the string ~~~
- Added a %%pkg_vcmp macro that accepts 3 parameters. The first parameter
  is a package name or provided capability name, the second argument is an
  operator ( < <= = >= > != ) and the third parameter is a version string
  to compare the installed version of the first argument with.
- Added a %%pkg_version_cmp macro which accepts a package or capability name
  as first argument and a version number as second argument and returns
  - 1, 0, 1 or ~~~ . The number values have the same meaning as in %%rpm_vercmp
  and the ~~~ string is returned if the package or capability can't be found.
* Fri Jun  9 2017 sriedel@suse.com
- Add patch to handle newer package statement variations for Perl
  5.12+
  * perlprov-package.diff
* Mon Apr 10 2017 fvogt@suse.com
- Add patch to handle special case of .qm file paths correctly (boo#1027925):
  * find-lang-qt-qm.patch
* Fri Mar 17 2017 kukuk@suse.com
- Convert rpmconfigcheck init script to systemd unit
* Mon Mar  6 2017 rguenther@suse.com
- Tweak debugsubpkg.diff to no longer use obsoleted RPM interfaces
  and add support for debuginfo compressed by DWZ.
- Add %%_find_debuginfo_dwz_opts and DWZ limits to macrosin.diff.
- Add dwz requires to rpm-build.  [fate#322957]
* Wed Mar  1 2017 mls@suse.de
- Tweak debugedit-comp-dir patch so that debugedit does not crash
  with a NULL comp_dir [bnc#1027228]
* Mon Feb 27 2017 rguenther@suse.com
- Fix debugedit-canon-fix.diff to handle directory table size
  shrinking by 1 byte correctly.
* Wed Feb 22 2017 bwiedemann@suse.com
- Add upstream patches 0001-set-SOURCE_DATE_EPOCH-from-changelog.patch
  0002-Extend-changelog-to-support-full-timestamps-903.patch
  0003-Allow-SOURCE_DATE_EPOCH-to-override-file-timestamps.patch
  0004-Allow-SOURCE_DATE_EPOCH-to-override-RPMTAG_BUILDTIME.patch
  in order to allow for building bit-identical rpms as described in
  https://github.com/rpm-software-management/rpm/pull/144
* Mon Feb 20 2017 mls@suse.de
- update to rpm-4.13.0.1
  * fix several out of bounds reads in the OpenPGP parser
  * fix handling of OpenPGP reserved tag (should be rejected)
  * fix various crashes from malformed packages with invalid tags
  * fix transfiletriggerpostun nondeterministic behavior
* Thu Jan 19 2017 mls@suse.de
- update to rpm-4.13.0
  * support of rich (boolean) dependencies
  * support of file triggers
- new patches:
  * nobfd.diff
  * emptymanifest.diff
- dropped patches:
  * rpm-4.12.0.1-lua-5.3.patch
  * fixsizeforbigendian.diff
  * repackage-nomd5.diff
* Sun Oct 30 2016 jengelh@inai.de
- Correct summary/description of -lang subpackages
* Tue May 31 2016 mls@suse.de
- add is_opensuse and leap_version macros to suse_macros
  [bnc#940315]
* Thu May 19 2016 dimstar@opensuse.org
- Add rpm-findlang-inject-metainfo.patch: allow packagers to inject
  a metainfo.xml file for the -lang package, which can then serve
  AppStream based Software Centers to show -lang packages as
  extensions to applications (boo#980583).
* Mon May  2 2016 mls@suse.de
- work around bug in rpm's macro expandsion [bnc#969381]
* Thu Apr 21 2016 mls@suse.de
- tweak rpm-4.12.0.1-lua-5.3.patch so that it does not need
  the -p1 option
- add option to make postinstall scriptlet errors fatal
  [bnc#967728]
  new patch: enable-postin-scripts-error.diff
- rework nfs-blocksize-free.patch to always normalize big
  blocksizes to 4096 bytes
  [bnc#894610] [bnc#829717] [bnc#965322]
  removed patch: nfs-blocksize-free.patch
  new patch: normalize_blocksize.diff
- drop service_del_preun, service_del_postun macros, they are
  provided by the systemd package
- change restart_on_update and stop_on_removal macros to use
  service_del_preun and service_del_postun
  [bnc#968405] [bnc#969381]
* Fri Jan 15 2016 stefan.bruens@rwth-aachen.de
- add beecrypt-4.1.2-build.diff:
  * make sure debug info is not stripped from internal beecrypt
* Sat Oct 17 2015 schwab@linux-m68k.org
- %%install_info_delete: only delete if package is removed
* Thu Oct  1 2015 fvogt@suse.com
- Add nfs-blocksize-free.patch:
  * Blocksize of NFS shouldn't be used directly
- Fixes bsc#894610 and bsc#829717
* Mon Sep 21 2015 schwab@suse.de
- Add armv6hl to %%arml macro
* Sat Jul 18 2015 i@marguerite.su
- add patch: rpm-4.12.0.1-lua-5.3.patch
  * replace luaL_optint/luaL_checkint w/ (int)luaL_optinteger
    (int)luaL_checkinteger for compatibility w/ lua 5.3
* Sun Jun 21 2015 lmuelle@suse.com
- add a space when printing information about updating a sysconfig file
* Fri Feb 27 2015 coolo@suse.com
- apply db.diff from the subdir to avoid patching through a symlink
  (to please new patch)
- comment gcc-PIE for now
* Fri Feb 20 2015 meissner@suse.com
- add gcc-PIE to requires of rpm-build to make PIE building
  default. bsc#912298
* Sun Nov 30 2014 Led <ledest@gmail.com>
- fix bashisms in brp-compress, symset-table and check-rpaths
  scripts
- fix shebang in find-supplements.ksyms script that contains
  bash-specific constructions
- updated patches:
  * modalias.diff
  * modalias-kernel_module.diff
  * brpcompress.diff
- add patches:
  * rpm-4.12.0.1-fix-bashisms.patch
* Tue Nov 11 2014 mmarek@suse.cz
- Do not generate supplements for kgraft patches (bnc#904848)
  new patch: modalias-no-kgraft.diff
* Mon Oct  6 2014 mls@suse.de
- fix size and payloadsize generation for big endian platforms
  new patch: fixsizeforbigendian.diff
* Thu Sep 18 2014 mls@suse.de
- update to rpm-4.12.0.1
  * fixes archivesize being off a couple of bytes
* Tue Sep 16 2014 mls@suse.de
- update to rpm-4.12.0
  * weakdeps support is now upstream
  * new optional payload format to support files > 4GB
  * lots of cleanups all over the codebase
- dropped patches:
  autodeps.diff, psm-errno.diff, exportoldtags.diff, pythondeps.diff,
  newweakdeps.diff, findsupplements.diff, rpm-gst-provides.patch,
  noposttrans.diff, fontprovides.diff
* Mon Sep  8 2014 mls@suse.de
- update to rpm-4.11.3
  * consists of cherry picked bug fixes
  * fix double-free on malformed signature header (RhBug:1133885)
  * fix curl globbing being enabled on remote retrieval (RhBug:1076277)
  * fix verification of SHA224 signatures (RhBug:1066494)
  * fix buffer overflows on malformed macro define/undefine (RhBug:1087000)
  * fix buffer overflow on unterminated macro options
  * fix file actions sometimes carrying state across multiple
    rpmtsRun() calls (RhBug:1076552, RhBug:1128359)
  * fix %%autopatch options getting expanded twice
  * add support for %%autosetup -S git_am (RhBug:1082038)
- dropped patches: gentlyadjustmacros.diff, rundir.diff,
  m68k.patch, debugedit-m68k.patch
* Mon Aug 18 2014 mls@suse.de
- rename SuSE to SUSE [bnc#888990]
- add correct self-provides to debuginfo subpackages
* Thu May 22 2014 mls@suse.de
- adapt restart_on_update and stop_on_removal to use
  systemctl [bnc#878255]
* Fri May  9 2014 mls@suse.de
- fix macro adjusting in installplatform
  the old code broke macos like GNUconfigure [bnc#874897]
  new patch: gentlyadjustmacros.diff
* Fri Apr 25 2014 mls@suse.de
- make _rundir configurable
  new patch: rundir.diff
* Tue Apr 22 2014 coolo@suse.com
- offer a %%_rundir to avoid hardcoding /run - and packages wanting
  to support older distros, can have /var/run as fallback for the macro
* Mon Mar 10 2014 mls@suse.de
- export the old weak dependency tags so that they are
  accessible from python
  new patch: exportoldtags.diff
* Tue Feb 25 2014 mls@suse.de
- fix bug in weakdepscompa.diff patch
* Fri Feb 21 2014 mls@suse.de
- make the 'douple separator' error a warning
  new patch: checksepwarn.diff
* Thu Feb 20 2014 mls@suse.de
- cherry-pick new weakdeps tags from upstream
  new patch: newweakdeps.diff
  dropped: weakdeps.diff
- add weakdepscompat.diff to support querying the old tags
* Thu Feb 20 2014 mls@suse.de
- drop outdated and non-free RPM-Tips tarball [bnc#849465]
* Thu Feb 20 2014 mls@suse.de
- update to rpm-4.11.2
  * dropped patches: appdata_provides.diff, application_provides.diff,
    beedigest.diff, debug_gdb_scripts.diff, getauxval.diff,
    ignore_poolstr_dummy_entries.diff, ppc64le.diff,
    selfconflicts.diff, strpoolrehash.diff
* Fri Jan 31 2014 lnussel@suse.de
- package /usr/lib/rpm/macros.d
* Mon Dec  2 2013 adrian@suse.de
- activate config.guess and config.sub update also for ppc64le
* Fri Nov 29 2013 dvaleev@suse.com
- Rename and extend auto-config-update-aarch64.diff to
  auto-config-update-aarch64-ppc64le.diff to apply same hack to
  powerpc64le architecture
* Thu Nov 28 2013 schwab@suse.de
- Substitute current values of %%suse_release, %%sles_release, %%ul_release
  into suse_macros (bnc#851877)
* Mon Nov 11 2013 speilicke@suse.com
- Add find-lang-python.patch: Support for finding translations in
  %%python_sitelib/python_sitearch.
* Wed Nov  6 2013 dvaleev@suse.com
- Add support for ppc64le (ppc64le.diff)
  those are upstream commits:
  ef1497b1f81966fed56f008bc8ee8ba42102efd6
  cf07feda05822377d62b973adc4010c0d7f9eaa0
* Wed Oct 30 2013 schwab@suse.de
- debugedit-m68k.patch: Add support for m68k
* Wed Oct  9 2013 schwab@suse.de
- m68k.patch: Add support for m68k
* Wed Oct  2 2013 mls@suse.de
- add application_provides.diff and appdata_provides.diff to
  generate provides for .desktop files
  (both patches are sent to upstream)
* Fri Sep 27 2013 mls@suse.de
- add selfconflicts.diff: fix self-conflicts and self-obsoletes
  handling for verify operations [bnc#838133]
* Tue Sep 24 2013 mail@bernhard-voelker.de
- replace obsoleted "find -perm +NNN" syntax [bnc#842004]
  to "-perm /NNN" in debugsource-package.diff and
  finddebuginfo.diff.
* Wed Sep 11 2013 mls@suse.de
- fix two bugs in the rpmstrPoolRehash() function:
  adding strpoolrehash.diff and ignore_poolstr_dummy_entries.diff
* Thu Sep  5 2013 schwab@linux-m68k.org
- brp-compress-no-img.patch: don't compress image files
* Thu Aug 29 2013 mls@suse.de
- add beedigest.diff to plug memory leaks and support DSA signatures
  with hashes other than sha-1 (already upstream)
* Mon Aug  5 2013 dmueller@suse.com
- weakdeps.diff: readd support for recommends, suggests, enhances
  supplements
* Thu Aug  1 2013 mls@suse.de
- fix typo in .debug_gdb_scripts name [bnc#818502]
* Mon Jul 15 2013 mls@suse.de
- backport noposttrans.diff from rpm master [bnc#773575]
* Fri Jul 12 2013 mls@suse.de
- update to rpm-4.11.1
  * fix bogus file conflict on symlink permissions
  * fix replaced files not getting reported at all during verification
  * fix explicit file conflicts in installed packages being ignored
  * fix multiple corner cases in config file handling
  * fix disk-space accounting bugs
  * report replacing directories with non-directories as file conflict
- package rpmdb_* database tools
- get rid of kernel symbol requires/provides, instead add simple
  package provides/requires like in Fedora
- delete files.diff patch, it caused more harm than good
* Tue Jul  2 2013 dmueller@suse.com
- extend the armv7hl hack also to armv6hl
* Thu Jun 27 2013 dmueller@suse.com
- add support for armv6hl target
* Sun Jun 23 2013 schwab@linux-m68k.org
- psm-errno.patch: avoid losing errno from failures to unpack archive
* Thu Jun 20 2013 coolo@suse.com
- use gettext-devel instead of real package name gettext-tools
  to use the (for bootstrapping) preferred gettext-tools-mini
* Thu Jun 20 2013 coolo@suse.com
- add systemd-rpm-macros to essential list
* Sun May 19 2013 schwab@suse.de
- auto-config-update-aarch64.diff: increase level to 8
* Wed May  8 2013 schwab@suse.de
- Remove unused files
* Wed May  8 2013 dmueller@suse.com
- auto-config-update-aarch64.diff:
  * search up to 5 levels for interesting files to patch
* Mon Apr 22 2013 dmueller@suse.com
- add auto-config-update-aarch64.diff:
  * optionally automatically update config.guess/sub during build
* Fri Apr  5 2013 dmueller@suse.com
- update to 4.10.3.1:
  * Fix install-regression introduced in RPM 4.10.0 which can
  cause creation of real files and directories skipped when
  the path is shared with a %%ghost.
  * translation updates
* Fri Apr  5 2013 idonmez@suse.com
- Add Source URL, see https://en.opensuse.org/SourceUrls
* Sat Mar 30 2013 coolo@suse.com
- which is essential for man packages
* Mon Mar 25 2013 schwab@suse.de
- debugedit-aarch64.diff: handle aarch64 relocation
* Fri Feb 15 2013 dmueller@suse.com
- add ignore-auxv.diff:
  * avoid auxv parsing for any platform other than powerpc
- add config-guess-sub-update.diff:
  * update config.guess/sub for aarch64 support
- update rpmrc.diff, build.diff:
  * Support aarch64
* Thu Jan 10 2013 coolo@suse.com
- remove the macros that were documented to be removed january 2013:
  %%run_permissions, use %%set_permissions instead
  %%run_suseconfig, SuSEconfig is gone
  %%suse_update_config
* Wed Jan  2 2013 dmueller@suse.com
- update to 4.10.2 (bnc#796375):
  * Fix missing error code on unparseable signature in packages,
  regression introduced in rpm 4.10.0. This could result in packages
  with malformed signature falling through signature checking.
  * Fix missing error code on --import on bogus key file (RhBug:869667)
  * Fix installation of packages containing skipped hardlinks (RhBug:864622)
  * Fix --setperms regression introduced in rpm 4.10.0 (RhBug:881835)
  * Fix locale dependent behavior in rpm2cpio.sh (RhBug:878363)
  * Add --undefine cli switch for undefining macros (related to RhBug:876308)
  * Fix warnings when building with gcc >= 4.7
  * Permit key imports on transactions where signature checking is
  disabled, regression of sorts introduced in 4.10.0 (RhBug:856225)
  * Fix RPMPROB_FILTER_FORCERELOCATE aka --badreloc, regression introduced in
  4.9.0 (RhBug:828784)
  * Verify files from non-installed packages again, regression introduced
  in 4.9.0 (RhBug:826589)
  * Fix large (> 4GB) package support, regression introduced in
  4.9.0 (RhBug:844936)
  * Only create the first instance of a file shared between multiple
  packages on install (speedup + improved verification timestamp behavior)
  * Report config and missinok flags too in deptype format extension
  * Fix relative path handling in --whatprovides query
  * Add --noclean and --nocheck options to rpmbuild (RhBug:756531)
  * Permit non-existent %%ghost directories to be packaged (RhBug:839656)
  * Dont silence patch by default (RhBug:678000, RhBug:773503)
  * Accept "owner" as an alias to "user" %%verify attribute (RhBug:838657)
  * Add "power64" arch macro for all supported PowerPC 64 processors (RhBug:818320)
  * Fix bogus "unclosed %%if" error when %%include is used in conditionals
  * Report starting line for unclosed %%if errors in spec
  * Always print out package dependencies on build
  * Restore pre-4.10.0 fdFree() behavior, ie return the fd itself while
  references exist, returning NULL introduced fd leak regressions.
  * Remove up-streamed patches:
  - obsoletesdeptag.diff, fdopen_strncat.diff, powerpc-fix-platform.diff, missingok.diff
* Tue Nov 20 2012 dimstar@opensuse.org
- Change user_group_add macro to not invoke useradd and groupadd
  with -o parameter. Non-unique does not make sense when not
  passing -u/-g (useradd/groupadd) and fails on newer pwdutils/
  shadowurils implementations. The macro does not allow for a
  uid/gid being passed.
* Mon Nov 12 2012 coolo@suse.com
- buildrequire rpm-build - it's ignored otherwise
* Fri Nov  9 2012 coolo@suse.com
- remove pwdutils and timezone from default essentials, timezone
  is only required by very specific test suites, the builds happen
  in UTC anyway - and pwdutils hides packaging bugs
* Sun Nov  4 2012 coolo@suse.com
- insserv is not required any more
* Sun Nov  4 2012 coolo@suse.com
- extend the list of build essentials - 4 drop candidates
* Sun Nov  4 2012 coolo@suse.com
- glibc-locale is build essential too - too many things go wrong
  without locales
* Sun Oct 28 2012 coolo@suse.com
- gawk and file are build essentials too
* Tue Oct 16 2012 ro@suse.de
- new patch: powerpc-fix-platform.diff
  fix platform detection for ppc vs ppc64 (failed on ppc64 with
  personality changed to ppc)
* Wed Oct 10 2012 adrian@suse.de
- follow armv5tel architecture switch from armv5el
* Wed Sep 26 2012 coolo@suse.com
- fix rpm leaking file descriptors of packages:
  patch fix-fd-leak.diff
* Mon Sep 24 2012 coolo@suse.com
- put an end date as echo into
  %%run_permissions
  %%run_suseconfig
  %%suse_update_config
* Mon Sep 17 2012 coolo@suse.com
- disarm the additional links for debuginfos as they break our
  "debuginfo per subpackage" functionality.
* Thu Sep 13 2012 coolo@suse.com
- add net-tools and util-linux as basic build requires
* Tue Aug 28 2012 mls@suse.de
- update to rpm-4.10.0
  * get rid of a couple of patches
* Wed Aug  8 2012 pgajdos@suse.com
- remove %%run_suseconfig_fonts macro (openFATE#313536); new macros
  using fonts-config directly exist in M17N:fonts/fontpackages
* Thu Jul 19 2012 coolo@suse.com
- add tar to the rpm build essentials
* Wed Jul 18 2012 coolo@suse.com
- add an -r option to %%lang_package (bnc#513786)
* Wed Jul  4 2012 fcrozat@suse.com
- Add systemctl daemon-reload call when installing initscript
  (bnc#769973).
* Wed Jun 13 2012 ro@suse.de
- set suse_version to 1220
* Thu May 24 2012 adrian@suse.de
- set armv5tel architecture (similar to armv7hl approach)
* Thu May 10 2012 coolo@suse.com
- remove duplicated rb_ macros - they are in ruby
* Fri Apr 20 2012 mls@suse.de
- fix some more crashes on malformed header data
  [bnc#754281] [bnc#754284] [bnc#754285]
- fix quoting in brp-python-hardlink [bnc#756087]
- change env handling for supplements [bnc#741543]
- fix _fix macros [bnc#728682]
- fix obsoletes handling of installed packages [bnc#714724]
- implement tilde support in version comparison [bnc#466994]
* Mon Mar 26 2012 vuntz@opensuse.org
- Update remove-translations.diff to fix a echo statement that was
  using -n.
* Tue Mar 13 2012 dimstar@opensuse.org
- Add rpm-gcc47.patch: Fix build with gcc 4.7 by correcting a
  strncat call and including missing headers.
* Tue Mar 13 2012 vuntz@opensuse.org
- Add findlang-new-help.diff: patch based on git commit 6047ddf6 to
  make find-lang know about the new gnome help layout.
- Add findlang-new-help-fix.diff: additional fix to above patch, so
  that locales with a territory work too (for instance, fr_FR).
- Rebase langnoc.diff on top of findlang-new-help.diff, so that we
  won't need to rebase it with a future release containing
  findlang-new-help.diff.
- Update remove-translations.diff to also remove help translations
  for languages that are not supported by the filesystem package.
* Tue Jan 31 2012 lnussel@suse.de
- avoid error message if /usr/lib/rpm/brp-suse.d is empty
* Sat Jan 28 2012 coolo@suse.com
- make the buildrequires more inclusive, rpm is special
* Fri Jan 20 2012 mvyskocil@suse.cz
- push Stopgap fix for rhbz#461683 from to SUSE
  set_javacmd preffers JRE over JDK
* Fri Jan 20 2012 dmueller@suse.de
- check exit code of suse brp scripts and abort if false
* Tue Jan 17 2012 saschpe@suse.de
- Spec file cleanup:
  * Removed authors from description
  * Spec-cleaner
* Mon Jan 16 2012 lnussel@suse.de
- fix automatic kernel supplements (bnc#741543)
* Mon Jan 16 2012 werner@suse.de
- Add patch from upstream to reflect changes of perl and python
  fileattrs to file 5.10 magics
* Fri Jan 13 2012 coolo@suse.com
- split rpmbuild into a package of its own, which then requires basic
  tools to build rpms
* Mon Jan  9 2012 dmueller@suse.de
- add a python3-rpm subspecfile
* Sat Jan  7 2012 dmueller@suse.de
- go back to lua 5.1 for now (no easy port to 5.2 possible)
* Mon Dec 19 2011 coolo@suse.de
- define %%suse_update_config as obsolete and make it a wrapper
  around autoreconf --force --install
- show diff in %%suse_update_libdir
* Thu Dec 15 2011 coolo@suse.com
- readd desktop.attr again, moving back from update-desktop-file
* Mon Dec 12 2011 coolo@suse.com
- readd brp-compress
* Fri Dec  9 2011 coolo@suse.com
- do not hardcode brp check list, but call everything below
  /usr/lib/rpm/brp-suse.d - and move our own brp scripts to
  brp-check-suse
* Wed Nov 23 2011 coolo@suse.com
- add libtool as buildrequire to avoid implicit dependency
* Tue Nov 15 2011 crrodriguez@opensuse.org
- The %%configure macro should use --disable-dependency-tracking
  that feature makes no sense when building rpms and only generates
  extra I/O and uglify log files. Fedora uses it since
  redhat-rpm-config version 9.1.0 too.
* Wed Oct 19 2011 mls@suse.de
- update to rpm-4.9.1.2
  * fixes some securities issues
  * makes two local patches obsolete
- add other security checks
- use ~/rpmbuild as topdir is /usr/src/packages in not writeable
  [bnc#658536]
- bump suse_version macro
* Fri Sep 30 2011 adrian@suse.de
- enforce armv7hl plattform by default, despite the kernel only
  reports armv7l via uname.
- make armv7hl backward compatible to armv7l
* Thu Sep 29 2011 dmueller@suse.de
- fix architecture definition for armv5el
* Thu Sep 29 2011 adrian@suse.de
- use -O0 for soft FPU ARM
* Tue Sep 27 2011 adrian@suse.de
- define rpmv7hl architecture for hard fpu support
* Tue Sep  6 2011 vuntz@opensuse.org
- Update findlang.diff: do not mark standard gettext translation
  files as %%doc.
- Rebase langnoc.diff and remove-translations.diff appropriately
  after this change..
* Wed Aug 24 2011 meissner@novell.com
- restore old debugedit behaviour for stabs, otherwise
  binaries with stabs in it will fail the build (e.g. vmlinux images
  on Power)
* Mon Aug 15 2011 ro@suse.de
- workaround in mono-find-requires: use >= as operator when finding
  .NET 1.0 dependencies, the .NET 1.5 libraries are compatible
  (note mono-find-requires and mono-find-provides as used by the
  internal dependency generator are really outdated)
* Wed Aug 10 2011 crrodriguez@opensuse.org
- Do not use -fno-strict-aliasing globally, the code
  already does in places where really needed.
* Tue Jul 26 2011 mls@suse.de
- fix defattr handling for doc files
* Thu Jul 21 2011 mls@suse.de
- fix problem with trailings slashes and recursive file adding
* Wed Jul 20 2011 mls@suse.de
- fix problem with trailing slashes on dir files
* Mon Jul 18 2011 mls@suse.de
- update to rpm-4.9.1
  * fixed a bug in signature checking
  * fixed crash on rpm --import for multiple keys [bnc#704589]
  * got rid of a couple of patches
- fixed dependency generation for suid binaries [bnc#702857]
* Fri Jun 17 2011 fcrozat@suse.com
- update brp.diff to not convert /sbin/init to absolute symlink
  (needed for kiwi and systemd).
* Wed Jun  8 2011 mls@suse.de
- change sigpipe fix so that the code really reads everything
  from the pipe
* Mon Jun  6 2011 coolo@novell.com
- move desktop.attr to update-desktop-files
* Mon Jun  6 2011 mls@suse.de
- ignore SIGPIPE when writing to dependency helpers, so that
  builds don't randomly abort when a helper is missing
* Fri Jun  3 2011 mls@suse.de
- add --assume-exec option to elfdeps, so that the dependency
  generator really works for libs without x-bits
* Mon May 23 2011 mls@suse.de
- do not die if the changelog section is empty [bnc#695400]
* Fri May 20 2011 mls@suse.de
- get rid of "unexpectedly shrank by one" error
* Thu May 19 2011 mls@suse.de
- remove gstreamer from fileattrs
- remove unused var from magic_and_path patch
* Thu May 19 2011 mls@suse.de
- disable perl requires generation completely
* Wed May 18 2011 mls@suse.de
- split elflib from elf fileattrs so that libraries without
  x-bits are also scanned
* Tue May 17 2011 mls@suse.de
- allow macro undef/change while expanding the macro itself
* Mon May 16 2011 mls@suse.de
- update to rpm-4.9.0:
  * use internal dependency generator
  * pluggable autodeps generators
  * update to berkeleydb 4.8.30
  * fixed dependency match corner cases
  * experimental collection implementation
* Wed May  4 2011 mmarek@novell.com
- rpmsort
  + Fix comparison function to match rpm (bnc#644515, thanks to
    Michael Schroeder).
  + Add --test option to verify result against zypper vcmp.
* Sat Feb 19 2011 vuntz@opensuse.org
- Don't call /sbin/conf.d/SuSEconfig.pango in
  %%run_suseconfig_fonts: it has been removed during 11.4
  development.
* Fri Jan 14 2011 coolo@novell.com
- let %%find_lang remove (with a comment) languages not supported.
  Supported languages are in filesystem.rpm's file list (bnc#659001)
* Mon Dec 20 2010 mls@suse.de
- fix depflag_strong filter, all weak deps were shown as
  strong (bnc#359566).
* Thu Dec  9 2010 meissner@novell.com
- fixed two more remaining filenames with spaces issues.
* Wed Dec  8 2010 meissner@novell.com
- handle spaces in manpage filenames (like e.g. in boost).
* Tue Dec  7 2010 coolo@novell.com
- add script to provide sysvinit(<PROV>) from /etc/init.d/*
* Fri Nov 19 2010 chris@computersalat.de
- remove perl macro stuff from suse_macros
  o provided with perl /etc/rpm/macros.perl
* Tue Nov 16 2010 lnussel@suse.de
- fix %%verify_permissions to actually only warn
- introduce %%set_permissions to replace %%run_permissions in the future
* Tue Nov  9 2010 lnussel@suse.de
- don't call /usr/bin/Check at all anymore. superfluous
* Tue Nov  9 2010 lnussel@suse.de
- change %%verify_permissions to use new system mode of chkstat
* Fri Oct 29 2010 mls@suse.de
- add support --with-only-C and --without-C options to find-lang.sh,
  add %%no_lang_C macro to allow compatible builds [bnc#449847]
* Mon Oct  4 2010 cristian.rodriguez@opensuse.org
- Enable libcap support so we can use the %%caps macro in spec
  files to set POSIX capabilities.
* Wed Sep  8 2010 ro@suse.de
- add leading / where appropriate in rpm-suse_macros (bnc#625763)
* Thu Sep  2 2010 dimstar@opensuse.org
- Add rpm-gst-provides.patch to allow rpm to collect provides of
  gstreamer codecs. This will help pk-gstreamer-install to also
  find the codecs it is looking for.
* Thu Aug 12 2010 vuntz@opensuse.org
- Add pkgconfig-0.24.diff: starting with pkg-config 0.24, the
  - -print-requires command was upstreamed, but split in
  - -print-requires and --print-requires-private. We need both in
  pkgconfigdeps.sh, though. If accepted, the patch should get
  upstreamed.
* Tue Jul 20 2010 coolo@novell.com
- make suse_version 1140
* Mon Jun 28 2010 jengelh@medozas.de
- use %%_smp_mflags
* Fri Jun  4 2010 mls@suse.de
- update changelog trim date
* Fri Jun  4 2010 mls@suse.de
- fix sbit removal code [bnc#610941]
- sort permlist file
* Fri Apr  9 2010 mls@suse.de
- do not load keyring if signature checking is disabled [bnc#554552]
- fix nosource/nopatch srpm tag generation
* Thu Apr  8 2010 mls@suse.de
- backport some fixes from upstream
- add generation of python/font/pkgconfig dependencies
* Wed Apr  7 2010 mls@suse.de
- work around spurious tar message [bnc#558475]
- fix defattr reset bug [bnc#594310]
- make 'rpmconfigcheck status' exit with 4 [bnc#592269]
- don't consider prereq deprecated for now
* Fri Mar 26 2010 mls@suse.de
- port sles11-sp1 repackage-nomd5.diff and safeugid.diff
* Fri Mar 26 2010 mls@suse.de
- update to rpm-4.8.0
  * updated python bindings
  * new transaction ordering code
* Wed Feb 24 2010 mls@suse.de
- fix readLine segfault [bnc#582599]
* Sat Dec 12 2009 jengelh@medozas.de
- add baselibs.conf as a source
- add SPARC baselibs
* Wed Nov  4 2009 coolo@novell.com
- set suse_version to 1130
* Wed Nov  4 2009 coolo@novell.com
- do not overwrite the default fuzz factor any longer
- change the payload compression to 5
* Fri Oct 23 2009 mls@suse.de
- add make_install macro definition for real
* Tue Sep  8 2009 crrodriguez@suse.de
- make lang_package(s) Noarch
* Fri Sep  4 2009 mls@suse.de
- do not statfs all filesystems until there is something
  to report
- cherry pick default clean section patch from upstream
- add make_install macro definition
* Wed Sep  2 2009 mls@suse.de
- allow ufdio payload
- pack db.h include file
- fix abs filelist specification [bnc#535594]
- fix query return value [bnc#527191]
* Mon Aug 31 2009 aj@suse.de
- Fix debuginfo handling for monodevelop-debugger-gdb and
  monodevelop-debugger-mdb packages (bnc#535543).
* Wed Aug 26 2009 mls@suse.de
- set fuzz factor back to 2 for now
* Mon Aug 24 2009 mls@suse.de
- update to rpm-4.7.1
* Mon Jul 27 2009 rguenther@suse.de
- add description to debuginfo packages
* Mon Jul 27 2009 rguenther@suse.de
- do not strip .debug suffix during debug-link generation
- do not add requires based on private ELF flags  [bnc#524681]
- remove requires on debuginfo from debugsource package
* Sat Jul 25 2009 rguenther@suse.de
- fix debuginfo package generation for binaries without build-id
* Fri Jul 24 2009 rguenther@suse.de
- revert SUSEBuildCnt patch
- fix debuginfo package generation for build root URLs with macros
* Thu Jul 23 2009 rguenther@suse.de
- add support for SUSEBuildCnt tag
* Thu Jul 23 2009 rguenther@suse.de
- generate debuginfo packages for each sub-package with corresponding
  debug information
* Mon Jul 13 2009 coolo@novell.com
- the correct value for libexecdir is exec_prefix/lib (as the
  comment rightfully already mentioned)
* Tue Jun  9 2009 mmarek@suse.cz
- findksyms.diff: also generate provides for kernel packages.
* Mon Apr  6 2009 ro@suse.de
- fix typo in brp-symlink (bnc#457908)
* Tue Mar 31 2009 mmarek@suse.cz
- findksyms.diff: don't check for /boot/symsets-*, generate ksym()
  requires if not present.
* Thu Mar 19 2009 ro@suse.de
- rpm-suse_macros: suse_version to 1120
* Thu Feb 19 2009 schwab@suse.de
- Add support for xz compressed sources.
* Wed Feb 18 2009 jblunck@suse.de
- Add debuginfo.prov helper script for build-id provides.
* Mon Feb 16 2009 ro@suse.de
- fix sort call in finddebuginfo again
* Wed Feb 11 2009 coolo@suse.de
- sort the result of find to make symlinks stable in finddebuginfo
* Wed Feb 11 2009 coolo@suse.de
- adapt to new API of xz, sticking with the old LZMA format (not XZ)
* Mon Feb  9 2009 ro@suse.de
- define disttag as optional tag with macro just like disturl
* Thu Jan 29 2009 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)
* Tue Jan 27 2009 agruen@suse.de
- find-supplements.ksyms: Fix "Supplements: packageand(
  kernel-$flavor:$package)" dependency (bnc#429254).
* Mon Jan  5 2009 mmarek@suse.cz
- findksyms.diff: make sure that the input files for join are
  sorted properly (bnc#450714)
* Fri Dec 19 2008 mls@suse.de
- add popt-devel and rpm-devel to baselibs config (bnc#445037)
* Thu Dec 11 2008 ro@suse.de
- brp-symlink: whitelist kde4 doc path (bnc#457908)
* Thu Dec 11 2008 agruen@suse.de
- find-supplements.ksyms: Module aliases may contain special
  characters that rpm does not allow in dependencies, such as
  commas. Encode those as %%XX to avoid generating broken
  dependencies (bnc#456695).
* Tue Dec  9 2008 schwab@suse.de
- find-debuginfo.sh: Don't convert to binary.
* Mon Dec  1 2008 ro@suse.de
- add rpm to baselibs.conf (for net-snmp)
- append a "nil" after suse_install_update_script and _message
* Fri Nov 28 2008 dmueller@suse.de
- fix build
- fix stack based buffer overflow in filelist parsing (bnc#397006)
- add macros for update messages and update scripts
* Fri Nov 28 2008 mls@suse.de
- disable debug package requires for now, they cause more harm
  than benefits
* Thu Nov 27 2008 mls@suse.de
- remove '-m64' from ppc64 optflags [bnc#447002]
- add _specfile macro
- set RPMBUILD_ env vars for file helpers
- make find-supplements.ksyms use RPMBUILD_SPECFILE [bnc#443815]
* Tue Nov 25 2008 jblunck@suse.de
- find-debuginfo.sh: fix for handling absolute symlinks
* Fri Nov 21 2008 mls@suse.de
- add firmware.prov provides helper
* Fri Nov 21 2008 mmarek@suse.cz
- fixed sed expression in find-provides.ksyms
* Tue Nov 18 2008 jblunck@suse.de
- find-debuginfo.sh: Create symlinks reflecting the policy from brp-symlink
* Thu Nov 13 2008 agruen@suse.de
- Fix the ksym(...) provides to also include the kernel flavor
  (bnc#444698).
* Fri Nov  7 2008 ro@suse.de
- update gcc flags to current set
* Fri Oct 31 2008 coolo@suse.de
- moved suse_update_desktop_files to package update_desktop_files
* Tue Oct 28 2008 jblunck@suse.de
- debugedit: Don't emit NOPs at the end of the line number program but at the
  beginning (bnc #433182 again)
- debugedit: Fix an uninitialized variable use that lead to segfaults from
  time to time
* Tue Oct 28 2008 mls@suse.de
- fix fingerprint computation for gpg checksums
* Tue Oct 21 2008 jblunck@suse.de
- debugedit: Fix debuginfo problems introduced by last patch (bnc #433182)
* Mon Oct 20 2008 mls@suse.de
- drop static libraries and libtool archives
* Thu Oct  2 2008 vuntz@suse.de
- support the new -t option of suse_update_desktop_file.sh in
  rpm-suse_macros
* Thu Oct  2 2008 mls@suse.de
- fix rpmrc compile options for ia64 [bnc#431345]
* Thu Oct  2 2008 jblunck@suse.de
- debugedit: Fix some compilation warnings and the canonicalization error.
* Tue Sep 16 2008 ro@suse.de
- fix find-debuginfo.sh and debugsource-package.diff to even
  apply (directory depth)
- add hack from jblunck using home made elfcmp
* Mon Sep 15 2008 jblunck@suse.de
- fix find-debuginfo.sh to work on filenames with spaces in
* Fri Sep 12 2008 mls@suse.de
- fix changelog cutter
- fix find-requires script
- add mimetype.diff patch from Scott Reeves
* Thu Sep 11 2008 mls@suse.de
- update to 4.4.2.3 to get rid of >50 patches
- make changelog cutter configurable
- update rpm-suse_macros
* Fri Sep  5 2008 dmueller@suse.de
- strip .comment and .GCC.command.line sections from ELF binaries
* Mon Aug 25 2008 prusnak@suse.cz
- enabled SELinux support [Fate#303662]
* Thu Aug 21 2008 ro@suse.de
- update rpm-suse_macros
* Wed Aug 20 2008 agruen@suse.de
- rpmconfigcheck: set Required-Stop to $null; this init script
  only performs some checks when started.
- /usr/lib/python* belongs to the rpm-python package; remove from
  the main rpm package.
* Mon Jun 30 2008 dmueller@suse.de
- add a requires_ge macro as well
* Thu Jun 26 2008 schwab@suse.de
- Fix db configure script.
* Thu May 15 2008 dmueller@suse.de
- remove references to brp-strip-comment-note (bnc#390163)
* Tue May  6 2008 mls@suse.de
- enable all parts of the noprovides patch again, making our rpm
  compatible to rpm4
* Fri May  2 2008 dmueller@suse.de
- add at least one supplements prefering the right kernel flavour
  if no modalias could be generated (bnc#384084)
* Thu May  1 2008 agruen@suse.de
- For kernel modules, require "kernel(flavor:symset) = version"
  instead of "kernel(symset) = version". This disambiguates
  the case where several kernel flavors end up with the same
  modver checksums (190163, 355628).
* Wed Apr 16 2008 jblunck@suse.de
- Get rid of noise when no debuginfo was generated
- Never strip static libraries in find-debuginfo script
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file for xxbit packages
* Thu Apr 10 2008 jw@suse.de
- added whatrequires-doc.diff
  Adds a hint to the misleading --whatrequires option, pointing to
  the more useful -e --test.
  Motivated by a talk thread started by Hubert.
* Wed Apr  9 2008 mrueckert@suse.de
- revert the last change as it leads to duplicated entries in the
  file list
* Wed Apr  9 2008 jblunck@suse.de
- Fix a bug in last commit that leads to /usr/src/debug not belonging
  to any package.
* Wed Apr  9 2008 jblunck@suse.de
- Put debug sources into separate -debugsource package.
* Fri Mar 28 2008 coolo@suse.de
- leave the rpm package itself with bzip payload to
  avoid blocking updates from within running system
* Thu Mar 27 2008 coolo@suse.de
- switch payload default to lzma -2
- flag GNOME docu as %%doc (bnc#358838)
* Tue Mar 18 2008 mls@suse.de
- make ia32 compatible to ia64, like it was in SLES9 [bnc#367705]
- fix memory leak and endless loops in lzma code
- make rpm provide the right lzma rpmlib name
* Tue Mar 18 2008 schwab@suse.de
- Fix broken db configuration.
* Fri Mar 14 2008 coolo@suse.de
- change it to the "alone" file format used by stable
  distributions of 7zip and lzma
* Fri Mar 14 2008 coolo@suse.de
- daring some more compression time to get an overall picture
* Thu Mar 13 2008 coolo@suse.de
- support lzma payload using liblzma
* Thu Feb 21 2008 mls@suse.de
- do not configure autoreloc or colors
* Thu Jan 31 2008 ro@suse.de
- brp-symlink: whitelist /opt/kde3/share/doc*/HTML/*/common
* Mon Jan 28 2008 ro@suse.de
- finddebuginfo.diff: disable debuginfo for mono at the moment
* Mon Jan 21 2008 mls@suse.de
- change vendor detection so that it works in build service, too
* Sat Jan 19 2008 mls@suse.de
- update rpm-suse_macros so that the build service can build, too
* Thu Jan 17 2008 wberrier@suse.de
- autodeps.diff
  pass .config files to mono-find-requires, not mono-find-provides
* Mon Dec  3 2007 dmueller@suse.de
- list email address completely again (#344147)
* Fri Nov 16 2007 dmueller@suse.de
- shorten changelogs in binary rpms (#308569)
  * saves 4.3MB for the one CD media
* Thu Oct 11 2007 schwab@suse.de
- Add support for lzma compressed archives.
* Sun Sep 30 2007 rguenther@suse.de
- fix build with gcc43
* Mon Sep  3 2007 dmueller@suse.de
- change %%lang_package implementation once again
  to support bundle-lang-other for only one desktop (#302270)
* Fri Aug 31 2007 dmueller@suse.de
- implement supplements for lang_packages (#306412)
* Fri Aug 10 2007 dmueller@suse.de
- package size reduction (#217472)
* Wed Aug  8 2007 dmueller@suse.de
- support optional -n parameter in %%lang_package
- make %%lang_package export a -all provides that
  can be used to resolve conflicts with the bundle
* Thu Aug  2 2007 mls@suse.de
- let the debug_package_requires macro overwrite the
  default requires in the debuginfo package
* Tue Jul 24 2007 dmueller@suse.de
- hardcode rpm in patch name
* Fri Jun 15 2007 dmueller@suse.de
- package size reduction (28%%)
* Sun May 27 2007 schwab@suse.de
- Remove duplicate rpmpopt alias.
* Fri May 25 2007 mls@suse.de
- fix patch-rpm query
- do not link convertdb1 statically [#274694]
- use --wildcards option for tar [#272519]
- fix perl.prov [#255009]
- show pre/posttrans scripts in --scripts query [#253620]
- remove popt version requires [#246871]
- fix missing file error
* Wed May 16 2007 mls@suse.de
- fix autodeps.diff mono logic
* Mon May 14 2007 coolo@suse.de
- correctly mark KDE documentation as %%doc in find-lang.sh
* Fri May 11 2007 coolo@suse.de
- adding %%lang_package to simplify seperating translations
* Fri Apr 27 2007 wberrier@suse.de
- autodeps.diff - bnc #227362
  - Print warning if mono assembiles are found but mono-find-* fails
  (solution is to make sure mono-devel is installed)
  - Also include .config files when searching for mono assemblies.
  (bnc #210224)
* Tue Apr 24 2007 mls@suse.de
- enable noprovides patch again.
  disable part of the patch so that rpm checks the package provides
  again instead of just package name when going through the
  obsoletes list. This makes rpm behaviour consistent with the
  updated libzypp. [#232127]
* Sun Apr 22 2007 dmueller@suse.de
- fix stripping of symbol table
* Tue Apr 17 2007 dmueller@suse.de
- strip comment and gcc command line sections from the packages
- rework SYMTAB_KEEP to accept a file pattern
* Sun Apr  8 2007 schwab@suse.de
- Include compilation directory in debuginfo file list.
* Sat Mar 24 2007 ro@suse.de
- added libbz2-devel to BuildRequires and Requires for -devel
* Fri Mar 23 2007 dmueller@suse.de
- drop custom libpopt so versioning
- move libpopt to /lib(64) for cryptsetup
- adjust installed libtool files
- Fix rpm buildrequires / devel requires
* Thu Mar 22 2007 stbinner@suse.de
- files.diff: when checking %%files list also show unpackaged files
  after "not found" error message [#255780]
* Thu Mar 22 2007 dmueller@suse.de
- remove strangely duplicated libpopt
- remove static popt and corresponding .la file to reduce
  dependencies
- Fix various format string errors in german translation
  which cause crashes
* Mon Mar 19 2007 rguenther@suse.de
- do not require build-key
* Tue Mar  6 2007 rguenther@suse.de
- adjust cflags_profile_generate and cflags_profile_feedback to
  enable tree profiling
* Fri Jan 26 2007 mls@suse.de
- create /var/spool/repackage directory [#230866]
- do not run pre/posttrans scripts in test mode [#235361]
* Thu Nov 30 2006 mls@suse.de
- disable noprovides patch [#224824]
* Fri Nov 24 2006 mls@suse.de
- fix buffer overflow in query function [#218983]
- fix off-by-two error in formatStrong [#210135]
- fix typo in (unused) beecrypt code [#219738]
- add standard buildservice macros
* Tue Nov 14 2006 agruen@suse.de
- Add %%supplements_kernel_module macro for use in firmware and
  similar packages which are related to modules in a
  kernel-$flavor package: RPM then extracts the modaliases from
  the specified module(s) and adds them as Supplements:
  modalias(...) tags, so that the package magaer will add
  such packages automatically when the respective hardware is
  present.
* Wed Nov  8 2006 agruen@suse.de
- Move the Kernel Module specific macros into the kernel-source
  package.
* Fri Oct 20 2006 agruen@suse.de
- Support the distribution-independent macros
  %%kernel_module_package_buildreq, %%kernel_module_package, and
  inside %%kernel_module_package, the macros %%flavors_to_build and
  %%kernel_source.
* Wed Oct 18 2006 mls@suse.de
- split up jumbo patch in 78 small patches
- fix lua directory handling [#201518]
- add /etc/rpm directory to filelist [#208762]
* Mon Oct 16 2006 agruen@suse.de
- Fix the KMP Package spec file template so that whenever the
  initrd contains a module that the KMP includes, the initrd will
  be regenerated (211646).
* Sun Oct 15 2006 schwab@suse.de
- Make sure config.rpath is present.
* Mon Oct  2 2006 agruen@suse.de
- %%suse_kernel_module_package: Abort when trying to build for a
  kernel that doesn't have an associated /boot/symsets-$krel.tar.gz
  file: we cannot generate the appropriate dependencies without.
* Mon Oct  2 2006 agruen@suse.de
- Allow kernel modules in packages even when the dependencies
  between those packages and the matching kernel packages cannot
  be tracked (199474).
* Sat Sep 30 2006 agruen@suse.de
- Make find-*.ksyms more robust.
* Tue Sep 19 2006 rguenther@suse.de
- split rpm-python to separate spec file
- remove python-devel BuildRequires
* Mon Aug 14 2006 ro@suse.de
- workaround for gettext using MKINSTALLDIRS in configure.ac
* Wed Jun 14 2006 mls@suse.de
- make rpmlib provide rpmlib(PatchRPMs) [#184856]
* Wed Apr 26 2006 agruen@suse.de
- rpm-suse-kernel-module-subpackage: Use a temporary file location
  that only root can write to (169378).
* Fri Apr 21 2006 mls@suse.de
- copy suse_macros file back into source rpm
* Mon Apr 10 2006 agruen@suse.de
- rpm-suse-kernel-module-subpackage: Arguments to -p and -f should
  be relative to %%_sourcedir.
* Fri Mar 24 2006 mls@suse.de
- fix uninitialized variable in unused file code [#160434]
* Fri Mar 24 2006 agruen@suse.de
- %%suse_kernel_module_package: Fix -x case when multiple flavors
  to include are specified. Do not build KMP packages without
  modversions or kernel(...) requirements.
* Tue Mar 21 2006 mls@suse.de
- fix PGP signature checking when there is no RSA sig
* Mon Mar 20 2006 agruen@suse.de
- Switch from modalias(foo) to modalias(kernel-flavor:foo)
  supplements to give the resolver enough information to do "the
  right thing".
* Sun Mar 19 2006 agruen@suse.de
- Allow paths relative to %%_sourcedir in
  %%suse_kernel_module_package.
* Sat Mar 18 2006 agruen@suse.de
- Clarify rpm --help texts.
* Fri Mar 17 2006 mls@suse.de
- fix cond queries that return no result
* Fri Mar 17 2006 mls@suse.de
- work around broken patchrpm database entries [#156347]
- add query support for suggests/recommends/enhances/supplements
  [#155301]
* Sun Mar 12 2006 agruen@suse.de
- find-supplements.ksyms: Don't generate too many Supplements;
  anything that does not have a colon in it (like pci:...) is not
  a modalias.
* Sat Mar 11 2006 ro@suse.de
- find-debuginfo: only "strip-debug" for static libs,
  do not use "strip-all" there
* Fri Mar 10 2006 agruen@suse.de
- Make KMP sub-packages require kernel-$flavor instead of kernel
  (mostly cosmetic).
* Fri Mar 10 2006 dmueller@suse.de
- patch for improved debuginfo extraction (#150940)
* Thu Mar  9 2006 agruen@suse.de
- find-scripts.diff: Add support for %%__find_enhances and
  %%__find_supplements scripts (from mls@suse.de).
- modalias.diff: Add modalias(...) Supplements tags that define
  the hardware that kernel module packages support (e.g.,
  modalias(pci:vBADOFBADdDEADBEEFsv*sd*bc*sc*i*)).
* Mon Mar  6 2006 agruen@suse.de
- %%suse_kernel_module_package: Add a -p option for defining
  additional preamble lines in sub-packages, subject to the same
  macro expansion as the sub-package (-s) itself.
* Wed Mar  1 2006 schwab@suse.de
- Fix logic error in find_debuginfo.sh [#144629].
* Fri Feb 24 2006 mls@suse.de
- fix cursor leak in rpmdbGrowIterator [#151953]
- print error message if scriptlet fork fails [#152779]
* Sun Feb 19 2006 agruen@suse.de
- scripts/find-requires.ksyms: Fix bug in last find-requires.ksyms
  fix.
* Sat Feb 18 2006 ro@suse.de
- allow debuginfo packages also for noarch (for mono,java)
* Fri Feb 17 2006 mls@suse.de
- put mono debug files in debuginfo packages [#151353]
- fix off-by-one error in glob code
- define _libexecdir to be _libdir [#136762]
- rename improves to supplements
* Thu Feb 16 2006 agruen@suse.de
- scripts/find-requires.ksyms: Tolerate kernel modules that have
  more than one vermagic info entry (it happened!).
* Mon Feb 13 2006 agruen@suse.de
- rpm-suse-kernel-module-subpackage:
  + Search for the spec file in %%_sourcedir and %%_specdir (150119).
  + If no KMP subpackage exists, use the Group and Summary tags
    of the main package.
* Fri Feb 10 2006 mls@suse.de
- add back missing chunk of srcdefattr patch [#48870]
- add rpmvercmp patch from Peter Bowan
- add -m32 to ix86 optflags to make --target work [#141206]
* Sat Feb  4 2006 agruen@suse.de
- rpm-suse-kernel-module-subpackage: Allow to specify a list of
  kernel flavors to build (-x) instead of specifying an exclude
  list.
* Fri Feb  3 2006 mls@suse.de
- use RPMSENSE_STRONG instead of RPMSENSE_WEAK
- drop support for EssentialFor
* Wed Feb  1 2006 agruen@suse.de
- rpm-suse-kernel-module-subpackage: Allow to specify a custom
  %%files list for the kernel-specific sub-packages. Use the
  Summary and Group tags, and the %%description section from the
  KMP sub-package for the kernel-specific sub-packages.
* Tue Jan 31 2006 agruen@suse.de
- rpm-suse-kernel-module-subpackage: Add version to additional
  Provides tag. We may need this for future Obsoletes.
* Fri Jan 27 2006 mls@suse.de
- added support for EssentialFor and Supports
- enabled support for lua scripts
* Fri Jan 27 2006 agruen@suse.de
- rpm-suse-kernel-module-subpackage: Add "Requires: kernel". Add
  - r option to override the release number. Clean up.
* Thu Jan 26 2006 agruen@suse.de
- rpm-suse_macros: Add -v option to %%suse_kernel_module_package
  to allow specifying a kernel module version different from the
  main package version. Restore the %%version, %%summary, and
  %%group macros of the main package at the end of
  %%suse_kernel_module_package.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 17 2006 agruen@suse.de
- rpm-suse_macros: Add %%suse_kernel_module_package macro for
  building kernel module packages.
* Wed Jan 11 2006 agruen@suse.de
- rpm-4.4.2.diff: find-requires.ksyms must not print "Requires:".
  Remove trailing whitespace.
* Wed Dec 21 2005 mls@suse.de
- make transaction lock --root aware
* Mon Dec 19 2005 mls@suse.de
- don't ignore getcwd return value in build.c
* Mon Dec 19 2005 mls@suse.de
- fix find-lang.sh script
* Sun Dec 18 2005 mls@suse.de
- fix find-debuginfo script
* Sun Dec 18 2005 mls@suse.de
- don't assume root:root defattr
* Sun Dec 18 2005 agruen@suse.de
- fix wrong buildsubdir macro name
* Thu Dec 15 2005 mls@suse.de
- update to version 4.4.2
  for now without lua, rpc, dav support
* Wed Dec  7 2005 agruen@suse.de
- Add find-{requires,provides}.ksyms and invoke them from the
  global find-{requires,provides} scripts. The scripts add
  "kernel(symbol set) = version" and "kver(symbol) = version"
  provides and requires to kernel module packages.
- Add symset-table script used to generate a table of known
  kernel symbol sets from /boot/symsets-*.tar.gz.
- Add rpmsort script to sort a file into RPM version order. Used
  in kernel scripts to sort kernel packages by version.
* Tue Nov 22 2005 ro@suse.de
- change NO_BRP_STRIP_DEBUG to NO_DEBUGINFO_STRIP_DEBUG
- fix patchrpm code not to modify immutable header parts
* Fri Nov 18 2005 ro@suse.de
- honor NO_BRP_STRIP_DEBUG in find-debuginfo.sh
* Fri Oct 28 2005 mls@suse.de
- use lstat instead of stat when globbing (#129434)
- add RPMTAG_PKGID and RPMTAG_HDRID
- make python always return requires/provides/obsoletes/conflicts
  as array
* Mon Oct 24 2005 ro@suse.de
- find-requires/find-provides: fix MONO_PATH
* Thu Oct 20 2005 ro@suse.de
- find-requires/find-provides: update mono hooks
* Wed Sep  7 2005 matz@suse.de
- Make debuginfo packages require exact version of base rpm.
* Fri Sep  2 2005 mls@suse.de
- backport CLOEXEC workaround [#93727]
- fix typo in man page [#114909]
* Thu Aug 25 2005 mls@suse.de
- don't catch ignored signals [#74560]
- unblock all signals when running scripts
* Mon Aug 22 2005 mls@suse.de
- do not try to mmap zero sized files in domd5()
* Fri Aug 12 2005 mls@suse.de
- change -mcpu to -mtune and add -D_FORTIFY_SOURCE=2 [#104241]
* Wed Aug  3 2005 mls@suse.de
- ignore /media when creating fdilesystem list
- allow --ignoresize when erasing packages
* Fri Jul  1 2005 schwab@suse.de
- Fix ppc assembly syntax.
* Wed Jun  8 2005 matz@suse.de
- add STRIP_KEEP_SYMTAB to find-debuginfo.sh
* Sat May 21 2005 schwab@suse.de
- find-debuginfo.sh: make writable before extracting debug info, simplify.
* Thu May 19 2005 schwab@suse.de
- Replace absolute symlinks when copying sources for debuginfo package.
* Wed Apr  6 2005 schwab@suse.de
- Cleanup neededforbuild.
* Wed Apr  6 2005 meissner@suse.de
- Added gettext-devel
* Tue Apr  5 2005 bg@suse.de
- add noarch to valid hppa architectures
* Thu Mar 24 2005 uli@suse.de
- better ARM support
* Sun Feb 20 2005 od@suse.de
- fix debugedit for relocatable files (kernel modules) on ppc
* Fri Feb 18 2005 mls@suse.de
- update debugedit program
* Fri Feb 18 2005 od@suse.de
- make find-debuginfo.sh handle kernel modules
* Wed Feb 16 2005 mls@suse.de
- fix --rebuilddb with --root [#50993]
* Fri Feb 11 2005 mls@suse.de
- update to elfutils-0.97 [#47746], [#48471]
- update to db-4.2.52 [#44193]
- pack brp-symlink
* Fri Feb 11 2005 ro@suse.de
- remove -fsigned-char from rpmrc (#49877)
* Sat Feb  5 2005 schwab@suse.de
- Fix building with gcc 4.
* Fri Feb  4 2005 mls@suse.de
- make python-2.4 work [#49990]
- fix --setguids / --setperms [#47122]
- makd gpgv4 signatures work [#42282]
- add brp-symlink [#49596]
* Fri Feb  4 2005 ro@suse.de
- fix one regexp in find_lang change
* Thu Feb  3 2005 ro@suse.de
- hppa may install noarch
* Wed Feb  2 2005 schwab@suse.de
- Remove compatibility provides on ia64.
* Mon Jan 31 2005 adrian@suse.de
- handle also ??_?? languages in %%find_lang.
* Fri Jan 28 2005 coolo@suse.de
- let the debuginfo packages work again
* Fri Jan 21 2005 skh@suse.de
- changed jpackage macros
* Fri Jan 21 2005 coolo@suse.de
- use binutils for debuginfo packages
* Fri Jan 14 2005 coolo@suse.de
- name the debug package -debuginfo to sync with redhat/fedora
* Mon Dec 13 2004 sndirsch@suse.de
- moved chinese popt mo file to correct directory (Bug #47262)
* Fri Dec  3 2004 mls@suse.de
- fix update of rpm with same name/version/release but different
  architecture
* Thu Nov 25 2004 ro@suse.de
- fix build with python-2.4
* Tue Nov 16 2004 ro@suse.de
- update permissions handling
* Mon Oct 18 2004 ro@suse.de
- locale rename: no -> nb
* Mon Sep 27 2004 mls@suse.de
- move TE type initializaten before the addTE call to make
  relocations work [#34871, #43557]
* Fri Sep 24 2004 mls@suse.de
- check payloadformat for "cpio", print extra deltarpm message
- don't skip directories in the fingerprint check when deleting rpms
* Thu Sep 23 2004 mls@suse.de
- allow database read access in scripts
* Wed Sep 22 2004 mls@suse.de
- only retry locking if errno is EAGAIN [#45704]
* Fri Sep 17 2004 mls@suse.de
- fix isSpecfile fix
- reset SIGILL handler in RPMClass()
* Mon Sep 13 2004 mls@suse.de
- glob.h: add workaround for invalid prototypes
* Thu Sep  9 2004 mls@suse.de
- fix jpackage macros
- change binary payload compression to w9.bzdio
- fix localization of query results [#38474]
- delete unmaintained cpanflute scripts [#39988]
- patch isSpecfile to be less restrictive [#40328]
- wait up to 3 minutes for the package lock [#40961]
* Thu Sep  2 2004 mls@suse.de
- add jpackage macros
* Fri Aug  6 2004 mls@suse.de
- make it build with new automake
* Wed Jun 23 2004 mls@suse.de
- add support for mono provides/requires autodetection.
  limited to *.exe and *.dll for now.
* Sun May 23 2004 schwab@suse.de
- Don't record timestamp in compressed manpages.
* Thu Apr 22 2004 mls@suse.de
- add DISABLE_RESTART_ON_UPDATE and DISABLE_STOP_ON_REMOVAL
  sysconfig variables
* Mon Apr 19 2004 mls@suse.de
- go back to libpopt.so.0.0.0
- also create and pack libpopt.so.1.0.0 for compatibility
* Wed Mar 31 2004 uli@suse.de
- added detection of i686-capable Transmeta Crusoe that reports
  as being i586 (bug #37713). This patch is necessary because YaST
  (rightfully) tries to install an i686 glibc on machines with this CPU, but
  RPM refuses to do so -> BOOM. This patch is safe because it only uses
  cpuid functions already used earlier in RPMClass() and does not do
  anything if the CPU identification string does not end in "ineTMx86".
* Wed Mar 31 2004 ke@suse.de
- remove broken german translation file [#30665],
* Fri Mar 26 2004 mls@suse.de
- use the system's zlib, fixes python segfault [#36810]
* Sun Mar 21 2004 aj@suse.de
- Work around lvalue used as cast problems.
* Thu Mar 18 2004 mls@suse.de
- convert query results to locale encoding [#28347]
- don't check provides if filename doesn't contain '/' [#32078]
- allow interrups if database is RDONLY [#33026]
- added _srcdefattr macro to set defattr for srpms [#33870]
- drop sbits from old files if installing new version [#35376]
- remove bogus entries from .la files [#36346]
- add _docdir_fmt macro to make it possible to create rpms
  for other distributions
* Sat Mar  6 2004 ro@suse.de
- readd lost patch hunk from last change:
  set docdir default back to .../packages/%%name (w/o version)
* Fri Mar  5 2004 mls@suse.de
- backport some fixes from rpm-4.2
- match py_libdir macro definition with python
- clean and re-create buildroot in a safe way
* Sat Feb 28 2004 schwab@suse.de
- Remove anchor from pattern in find-requires.
* Fri Feb 27 2004 schwab@suse.de
- Silence error from find.
* Fri Feb 27 2004 mls@suse.de
- fix definition of _initrddir
- set sysconfdir to /etc
- set localstatedir to /var
* Thu Feb 26 2004 schwab@suse.de
- Handle more cases of filenames with spaces.
* Thu Feb 26 2004 ro@suse.de
- some fixes in linux.prov to survive filenames with spaces
* Thu Feb 12 2004 mls@suse.de
- fixed linux.req soname generation (#21664)
- disable nptl for now
* Mon Feb  9 2004 kukuk@suse.de
- linux.req: Fix finding of interpreters
* Sat Feb  7 2004 olh@suse.de
- disable redhat's uname hack for ppc
* Thu Feb  5 2004 ro@suse.de
- linux.prov: don't block soname in versioned-requires
- linux.req: disable perl-requires, it's broken
* Tue Feb  3 2004 schwab@suse.de
- Readd ia64 64bit provides hack.
* Tue Feb  3 2004 kukuk@suse.de
- Remove all special find-requires scripts and use the default one
* Sat Jan 17 2004 schwab@suse.de
- Filter out linux-gate.so.
* Thu Jan 15 2004 schwab@suse.de
- For ia64 require 64bit symbols and provide them both with and without
  64bit.
* Tue Jan 13 2004 adrian@suse.de
- call ldconfig
- add missing Requires in -devel packages
- add %%defattr
* Fri Jan  9 2004 kukuk@suse.de
- Coompile with "-fno-strict-aliasing"
* Fri Nov 14 2003 bg@suse.de
- added changes for hppa
- fix build for hppa
* Fri Oct 10 2003 sf@suse.de
- added alias 'amd64' for 'x86_64'
* Fri Oct 10 2003 ro@suse.de
- ignore "linux-gate.so" in ldd output (on 2.6 systems)
* Wed Oct  8 2003 schwab@suse.de
- Add popt to prerequires for rpm.
* Tue Sep 23 2003 mls@suse.de
- really disable rpmconfigcheck
* Sat Sep 20 2003 kukuk@suse.de
- Don't enable rpmconfigcheck per default
* Fri Sep 19 2003 schwab@suse.de
- Fix descriptor leak [#31450].
* Mon Sep 15 2003 mls@suse.de
- remove redhat options from popt (#30302)
- check name and arch to find out if two packages are the same
* Fri Sep  5 2003 mls@suse.de
- fix rpmalMakeIndex and off by one error in rpmalAllSatisfiesDepend
* Fri Sep  5 2003 mls@suse.de
- use mkstemp in build.c
- fix --noghost query option
* Fri Sep  5 2003 mls@suse.de
- escape '+' in MIRE_DEFAULT iterator
- use MIRE_STRCMP when going for an exact match
- update rpmrc
* Wed Sep  3 2003 mls@suse.de
- speed up installation by making nofsync local and setting it
  for all databases but Packages
- fix database locking issue (#29407)
- don't open temporary databases in chroot case (may fix #29584)
* Mon Sep  1 2003 schwab@suse.de
- Fix assembler routines to not clobber predicate registers.
* Fri Aug 29 2003 mcihar@suse.cz
- rpm-python require same python version as it was built with
* Fri Aug 22 2003 mls@suse.de
- make usage of / in post section consistent
- don't force the activation of rpmconfigcheck
* Tue Aug  5 2003 coolo@suse.de
- give libpopt a soname > 0 as it's not compatible to the libpopt
  on SL 8.2 (now that we link shared, it does matter)
* Fri Aug  1 2003 mls@suse.de
- fix segfault in rpmdbFindByFile
* Thu Jul 31 2003 mls@suse.de
- added directory tagging to speed up installation/updates
* Tue Jul 29 2003 mls@suse.de
- add support for patch-rpms
- fix --root option (#28266)
- fix erase exit status (#28267)
- fix database open ignoring locks the second time
* Fri Jul 11 2003 mls@suse.de
- add perl_vendorlib and perl_vendorarch
- integrate patches
* Tue Jul  1 2003 coolo@suse.de
- update find-debuginfo.sh to fix permissions of copied files
- give warning on already stripped files
* Fri Jun 27 2003 schwab@suse.de
- Fix configure scripts.
- Don't link rpm statically.
* Fri Jun 20 2003 kukuk@suse.de
- use -fPIC, not -fpic to compile elfutils
* Thu Jun 19 2003 ro@suse.de
- fix build (gettext and definition of mkinstalldirs)
* Mon Jun 16 2003 kukuk@suse.de
- Don't call find on /usr/share/locale if directory does not exist.
* Sat Jun 14 2003 coolo@suse.de
- avoid stale links in /usr/src/debug
* Fri Jun 13 2003 mls@suse.de
- make PreReqs work again if --nodeps is used
- fix rpmconfigcheck
- apply find-debuginfo.sh patch from coolo
* Thu Jun 12 2003 kukuk@suse.de
- Fix find-lang.sh (special /usr/share/locale handling)
* Thu Jun 12 2003 coolo@suse.de
- enhancing find-lang.sh to take KDE/GNOME into account and label
  them correctly
* Wed Jun 11 2003 kukuk@suse.de
- Remove translated manual pages
* Fri Jun  6 2003 mls@suse.de
- fix vendor for s390/s390x
* Thu Jun  5 2003 mls@suse.de
- no longer build rpm static
- add --fileclass and --filecolor macros to rpmpopt
* Thu Jun  5 2003 ro@suse.de
- remove dangling rpmpopt symlink
* Mon Jun  2 2003 mls@suse.de
- convertdb1: call providePackageNVR to retrofit "Provide: name = EVR"
  into converted headers
* Fri May 23 2003 ro@suse.de
- fixed brp-compress to convert bzip2 man pages into gziped ones
  (even if hardlinked). (#21121) (from ma)
* Fri May 16 2003 mls@suse.de
- fixed x86_64 build
* Thu May 15 2003 mls@suse.de
- update to rpm-4.1.1
* Tue May 13 2003 mls@suse.de
- don't obsolete own package when refreshing
- fix parsing of nested conditionals (again)
* Tue May 13 2003 mls@suse.de
- created rpm-python subpackage
- fix check-files/fixowner, second try
* Mon May 12 2003 mls@suse.de
- fix check-files to work without buildroot
* Mon May 12 2003 mls@suse.de
- re-activate fixowner/group/perms
- allow /usr/share/info/dir in check-files
- fix 'head -n 1' in /usr/lib/rpm/find-requires
* Thu May  8 2003 mls@suse.de
- update to rpm-4.1
* Mon Apr  7 2003 ro@suse.de
- fix for new head(1) syntax
* Mon Mar 10 2003 mls@suse.de
- fix exit status if file to be installed is not a rpm package
* Fri Feb 28 2003 mls@suse.de
- use mkstemp instead of tempnam (#24478)
* Thu Feb 20 2003 ma@suse.de
- Work arround rpm2cpio wrongly reporting an error, if the rpm file
  is read from stdin. (#16800)
* Mon Feb 17 2003 mls@suse.de
- made rpmconfigcheck add new files to /var/log/update-messages
* Fri Feb 14 2003 schwab@suse.de
- Save errno inside Fclose, its return value is never checked anyway.
* Fri Feb 14 2003 pthomas@suse.de
- find-provides for elf64 systems used to omit symbol versions
  if they contained the soname, fixed by find_provides_soname.diff.
* Wed Feb 12 2003 mls@suse.de
- removed runlevels '1' and 'S' from rpmconfigcheck
* Fri Feb  7 2003 mls@suse.de
- speed up rpmconfigcheck by just checking the old conflicts if
  no rpm was installed
- rerun gpg if gpg fails with "option file created"
- set LC_ALL to C before calling gpg
* Tue Jan 28 2003 kukuk@suse.de
- Remove wrong Provides "rpm-devel" and "rpm-python" from Provides
* Sun Jan 26 2003 olh@suse.de
- the official arch_canon value for ppc64 is 16, not 5
* Thu Jan 16 2003 ma@suse.de
- update subpackage popt to 1.6.4
* Thu Dec 19 2002 schwab@suse.de
- Update autogen patch.
* Mon Nov 18 2002 stepan@suse.de
- add m68k as chanonical architecture to configure.in
* Mon Nov 18 2002 ro@suse.de
- adapt to latest autoconf
- use host instead of host_alias for %%host_alias since the latter
  is not set
* Mon Nov 11 2002 ma@suse.de
- let linux.prov list vrsion definitions in libraries/plugins without
  soname. (find_provides.diff)  (#21664)
* Fri Oct 25 2002 sf@suse.de
- corrected %%_libdir-macro (rpm-3.0.6-platform.diff)
* Mon Oct 21 2002 schwab@suse.de
- Fix read beyond EOS.
* Mon Oct  7 2002 ro@suse.de
- fixed brp-compress script for current fileutils
  (add LC_TIME=POSIX, this bug lead to broken tcl man pages)
* Wed Oct  2 2002 mls@suse.de
- update unpatched files in patchrpms even if --nodeps is used
  [Bug #20418]
* Sat Aug 24 2002 ro@suse.de
- fix popt-devel requires
* Sun Aug 18 2002 olh@suse.de
- adding -mminimal-toc to each package is a boring job
  use it per default on ppc64
* Thu Aug 15 2002 kukuk@suse.de
- Add insserv PreRequires [Bug #17969]
* Mon Aug 12 2002 bk@suse.de
- rpmrc/s390{,x}: change dummy -fomit-frame-pointer to -fsigned-char
* Sat Aug 10 2002 schwab@suse.de
- Make ia64 arch_compat to i686.
* Sat Aug 10 2002 kukuk@suse.de
- Fix version number of popt-devel
* Fri Aug  9 2002 kukuk@suse.de
- Fix typo
* Fri Aug  9 2002 kukuk@suse.de
- Fix requires of rpm-devel and popt-devel
* Thu Aug  8 2002 ro@suse.de
- adapt automake version in configure
* Fri Jul 26 2002 mls@suse.de
- Added perl/python macros from conectiva
* Fri Jul 26 2002 kukuk@suse.de
- Create rpm-devel and popt-devel subpackages [Bug #17225]
* Fri Jul 26 2002 kukuk@suse.de
- Change Requires for suse-build-key to build-key
* Thu Jul 25 2002 mls@suse.de
- renamed rpmconfigscan to rpmconfigcheck
- fixed elf64-linux.req to ignore scripts without #!
- disabled tag check in rpmdbFindByFile, too dangerous
* Thu Jul 18 2002 mls@suse.de
- fixed double free of header if the postinstall script failed
- return exit status when doing --initdb
* Thu Jul 11 2002 mls@suse.de
- use "officially reserved" value of RPMFILE_UNPATCHED
- added rpmconfigcheck script to search for unresolved config
  file changes
* Mon Jul  8 2002 mls@suse.de
- new version of patchrpm diff: handle patch "freshen" operations
  gracefully
- documented patchrpm options
- taggedindex diff: add directory tags to the fileindex to speed
  up file conflict detection
* Tue Jul  2 2002 ke@suse.de
- Update German program messages using translations by Christian
  Kirsch.  Add as Source7; drop Patch19 [# 8442].
* Thu Jun 20 2002 ro@suse.de
- automake is 1.6.2
* Wed Jun 12 2002 bk@suse.de
- ppc: fix arch for elf64.prov and elf64.req to powerpc(from olh)
- s390x: fix brp-lib64-linux to ignore */lib/ld64.so.1 in lib check
- remove obsolete x64_64 scripts, replaced by generic elf64 scripts
- rpm-3.0.6.pkg_build.diff: remove obsolete diff for sparc-linux.req
* Fri May 31 2002 olh@suse.de
- remove ppc64 hack
* Mon May 27 2002 bk@suse.de
- all lib64 platforms use the same brp, req and prov scripts now.
- merge mips diff to not include private flags into linux.req.suse
- merge last rpm-3.0.6-s390x-lib64.diff into rpm-3.0.6.config.diff
- add (64bit) fix for empty soname in elf64.prov from sles7-s390x
* Fri May 17 2002 olh@suse.de
- add more ppc64 changes, add brp-ppc64-linux
- apply mips, x86_64 and s390x patches on all archs
- rpm-3.0.6.lib64.diff: merged all lib64 stuff and add SUBSTS macros
  for uname->target_cpu handling on ppc64, s390 and x86_64
* Wed May 15 2002 ro@suse.de
- update brp-x86_64-linux
* Wed May 15 2002 mfabian@suse.de
- fix ja.po, it contained some junk which caused mojibake on
  output, especially in ja_JP.UTF-8 locale. Remove a lot
  of fuzzies which had correct translations.
* Mon May 13 2002 olh@suse.de
- do not translate ppc64 to ppc anymore
* Fri Apr 26 2002 sf@suse.de
- fixed brp-x86_64-linux script
- added *.a-files to brp-script
- look _only_ for files or links with names *.a, *.so*
- added /opt/gnome/lib and /opt/kde/lib
* Wed Apr 24 2002 sf@suse.de
- added script to show requires and provides with 64 bit
  (like s390 and sparc64)
- rpm will now stop (on x86_64) if a 64-bit binary
  (or a link to one) is found in
  $RPM_BUILD_ROOT{, /usr, /usr/X11R6}/lib
* Wed Apr 24 2002 ke@suse.de
- patch19: Fix 1 german message (3 strings) in de.po [# 8442].
* Mon Apr 22 2002 kukuk@suse.de
- Remove broken s390x try to fix lib64 library location
* Thu Apr 18 2002 kukuk@suse.de
- x86_64 can also build noarch packages
* Wed Apr 17 2002 sf@suse.de
- install i386-rpms on x86_64
- patch65 only, if not on s390x (doesn't apply)
- patch  to build with new automake (ro)
* Fri Apr 12 2002 kukuk@suse.de
- Don't apply s390x 64bit hacks on sparc64, sparc64 has a working
  libtool
* Thu Apr 11 2002 mls@suse.de
- fixed bug in patchrpm case that prevented the reuse of
  old timestamps in unpatched files in some cases
- fixed patchrpm dependency failure message
* Wed Apr 10 2002 sf@suse.de
- added x86_64 architecture
- added --libdir to autogen.sh to copy the libs depending on
  architecture (lib / lib64)
* Fri Mar 29 2002 schwab@suse.de
- Fix for new autotools.
* Fri Mar 22 2002 mls@suse.de
- added rpmqpack program to speed up susehelp
* Wed Mar 20 2002 ro@suse.de
- modified config.diff for currently used optflags (#15123)
* Mon Mar 18 2002 schwab@suse.de
- Don't lose errno.
* Mon Mar 11 2002 mls@suse.de
- use gpg --keyring when checking keys with uid != 0
- use hardcoded keyring path if _gpg_path is not set and uid == 0
- removed _gpg_path from suse_macros
* Sat Mar  9 2002 bk@suse.de
- brp-s390x-linux: merge lib64 fix: patch .la files when moving
* Fri Mar  8 2002 ma@suse.de
- introduced x86_64 architecture in rpmrc (#14110)
* Fri Mar  8 2002 mls@suse.de
- backported rpm4 fix to get mtime right on s390x
* Mon Feb 25 2002 mls@suse.de
- added patchrpm support
- changed rpm -qi to include the distribution
* Thu Feb 21 2002 schwab@suse.de
- Fix to build with new gettext.
* Mon Feb 18 2002 ro@suse.de
- added requires for suse-build-key
* Mon Feb 11 2002 ro@suse.de
- tar option for bz2 is now "j" (re-added)
* Mon Feb 11 2002 ma@suse.de
- unk_ugname_cached.diff: Upon building a package, unpacking sources
  by calling tar from the spec file, may lead to files with unknown
  user/group names. If those files are to be included in the final
  package, it's not appropriate to simply map unknown user/group names
  to the builders user/group (usg. root). This behaviour has been disabled
  and building the package will fail. There are ample means to propperly
  define file attributes. If a spec file does not use them, although it
  should, it's considered broken.
  Unknown user/group names lead to NULL entries in rpms user/group name cache,
  which may cause a segmentation fault on cache lookup. This has been fixed.
* Sat Jan 26 2002 ro@suse.de
- apply configure-diff also on s390x
* Mon Jan 21 2002 bk@suse.de
- use RPM_OPT_FLAGS for compilation
- add lib64 support for s390x
- update srcdir-supplied rpm-suse_macros file to newest version
  adds: %%_lib handling for ltconfig/-main and macro suse_update_libdir
- sparc64 and s390x: call scripts/brp-%%_arch-linux at the end of install
* Wed Jan 16 2002 schwab@suse.de
- Fix parsing of nested conditionals.
* Wed Jan  2 2002 schwab@suse.de
- Remove wrong assertion.
* Tue Dec 18 2001 adrian@suse.de
- fix find-requires for objdump with private flags finaly
* Mon Dec 17 2001 adrian@suse.de
- apply mips patch only on mips architecture
- fix mips patch
* Sun Dec 16 2001 adrian@suse.de
- fix find-requires script for mips
  ( do not include private flags from objdump to dependencies )
* Wed Dec  5 2001 schwab@suse.de
- Use optind = 0 to reset getopt in glibc.
* Mon Dec  3 2001 schwab@suse.de
- Fix another endian bug due to pointer mismatch.
* Thu Nov 22 2001 mls@suse.de
- reset getopt in grabArgs() macro expansion
* Thu Nov 15 2001 ma@suse.de
- Fixed: copyFile() in rpmchecksig didn't recognize 'No space left on
  device' condition, when creating tempfiles. rpm reported that the
  signature was not ok instead. (#12294)
* Thu Nov  8 2001 adrian@suse.de
- name mips big endian as "mips" instead of "mipseb"
  this is compatible to all GNU tools and to the SGI distribution
* Sat Nov  3 2001 ro@suse.de
- accept automake 1.5 (still needs depcomp added)
* Tue Sep  4 2001 schwab@suse.de
- Accept libtool 1.4.1.
* Fri Aug 17 2001 ro@suse.de
- Exclude /usr/share/doc from Requires
* Sat Jul 21 2001 schwab@suse.de
- Adapt for autoconf 2.52.
- Allow libtool version suffix.
* Tue Jul  3 2001 kukuk@suse.de
- Fix typo in last change
* Mon Jul  2 2001 ma@suse.de
- Change -m486 to -mcpu=i486 in optflags
* Wed Jun 20 2001 ma@suse.de
- Don't define popt version via macro. Abuild does not like it (#8224).
- Patches for rpmrc.in (ia64.dif,ppc64.rpmrc.diff) incorporated
  into config.diff.
- Patches for brp scripts (strip_no_lib.dif) and sparc64-linux.{req,prov}
  scripts (sparc64.dif) incorporated into pkg_build.diff.
* Wed Jun 13 2001 bk@suse.de
- rpm-3.0.6.config.diff: add s390x support
* Mon Jun 11 2001 olh@suse.de
- add ppc64 diff
* Fri Jun  8 2001 schwab@suse.de
- Fix endian bugs.
* Mon Jun  4 2001 kukuk@suse.de
- Fix requires/provides scripts for sparc64
* Fri Jun  1 2001 schwab@suse.de
- Fix for new configure tools.
* Wed May  9 2001 mfabian@suse.de
- bzip2 sources
* Thu May  3 2001 ma@suse.de
- provides script shouldn't block soname as version
* Tue May  1 2001 kukuk@suse.de
- modify spec file for sparc64
* Thu Apr 12 2001 ro@suse.de
- gettextize to compile with new gettext
* Fri Apr  6 2001 kukuk@suse.de
- Make some changes to the changes entries so rpm likes it again
* Thu Mar 29 2001 ro@suse.de
- provides/requires script: add "-n200" to xargs arguments
* Mon Feb 26 2001 ro@suse.de
- no optimization for alpha for now ...
* Wed Feb 14 2001 ma@suse.de
- Fix rpmio (unknown type off64_t) with glibc >= 2.2
- Fix configure.in to recognize SuSE as platform specific vendor
* Tue Feb  6 2001 ro@suse.de
- popt: include float.h to make it compile
* Wed Jan 17 2001 schwab@suse.de
- Mark ia64 as compatible to i386.
* Mon Jan  8 2001 ma@suse.de
- fixed previous fix (error occuring outside %%doc was lost)
* Sat Jan  6 2001 ma@suse.de
- fixed rpm does not abort build if %%doc file is missing (#503)
* Mon Nov 27 2000 ma@suse.de
- wrongly free() after alloca() fixed
* Thu Nov 23 2000 bk@suse.de
- removed old s390 hack(not needed-breaks with new rpm and glibc)
* Tue Nov 14 2000 ro@suse.de
- added patch not to strip all shared libs and
  files with "/lib/modules/" in path
* Fri Nov  3 2000 ma@suse.de
- let 'rpm -e --root ..' remove files/dirs chroot.
* Wed Oct 25 2000 ma@suse.de
- update subpackage popt to 1.6
* Tue Oct 17 2000 ma@suse.de
- fixed missing libpopt.so in popt subpackage
* Fri Oct  6 2000 ma@suse.de
- update to 3.0.6
* Fri Sep 29 2000 schwab@suse.de
- Fix last change to stay compatible with glibc < 2.2.
* Fri Sep 29 2000 schwab@suse.de
- Fix libio cookie function pointer clash in rpmio.
* Fri Jul 28 2000 ma@suse.de
- update to 3.0.5 (handles RPM v4 packages)
- ia64/s309 patches incorporated
* Wed Jul 26 2000 ma@suse.de
- ignore chown() errors eg. if files are installed on a DOS partition
* Fri Jul 14 2000 ma@suse.de
- fixed: ignore dependencies below /usr/share/doc.
- rpmrc: synced s390 entries with those in rpm-4.0.
* Mon Jun 26 2000 bk@suse.de
- build static on s390 too.
* Fri May 26 2000 schwab@suse.de
- For for new libbz2 API.
* Thu May 18 2000 kasal@suse.de
- hope now rpm-3.0.4-macro-grabArgs.patch works
* Wed May 17 2000 kasal@suse.cz
- fixed a typo in rpm-3.0.4-macro-grabArgs.patch (c=='?')
- fixed a problem when
  ifarch someother
  define macro sometext
  endif
  defined macro anyway
* Tue May 16 2000 kasal@suse.cz
- fixed the bug with {?suse_update_config:%%{suse_update_config -f}}
* Fri May 12 2000 schwab@suse.de
- Make ia64 compatible with noarch.
* Wed Apr 26 2000 ma@suse.de
- updated 3.0.4, removed obsolete patches, builds on
  libc5
* Fri Apr 14 2000 ma@suse.de
- Update for RPM-HOWTO
- Fix in config.diff (use Makefile.am not Makefile.in)
* Mon Apr 10 2000 schwab@suse.de
- Fix config patch.
* Thu Apr  6 2000 bk@suse.de
- added /lib/libpopt.so* to filelist on s390
* Tue Apr  4 2000 bk@suse.de
- uses autoconf and automake now
- added /lib/libbz2.so* and /lib/libz.so* to filelist on s390
* Sun Apr  2 2000 bk@suse.de
- add s390 architecture support to rpm
- add required %%suse_update_config for s390
- rpm is NOT linked statically on s390 for now
* Tue Mar 28 2000 ma@suse.de
- rpm.spec: avoid macro usage in 'Version:' entry
* Thu Mar  2 2000 schwab@suse.de
- Fix md5 for ia64.
* Mon Feb 28 2000 ma@suse.de
- remove 'libNoVersion' in find-requires
* Wed Feb 23 2000 schwab@suse.de
- recognize ia64 as architecture.
* Mon Feb  7 2000 ma@suse.de
- rebuilddb fix
- set info/mandir macros to /usr/share/...
* Wed Feb  2 2000 ma@suse.de
- update to 3.0.4 (popt-1.5)
- new subpackage: popt
* Sat Nov 13 1999 kukuk@suse.de
- Add sparc64 directory
- Fix installation into RPM_BUILD_ROOT directory
* Mon Nov  8 1999 kukuk@suse.de
- add directory /usr/src/packages/RPMS/sparc
* Thu Nov  4 1999 bs@suse.de
- fixed bug in find-requires regarding pseudo scripts
  starting with "#! --"
* Thu Oct 28 1999 bs@suse.de
- added directories /usr/src/packages/RPMS/{ppc,noarch}
* Wed Oct 27 1999 ma@suse.de
- place suse_macrofile in source/binary package
- don't check reqires below /usr/doc/
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Thu Sep  9 1999 bs@suse.de
- fixed call of Check at the end of %%install section
* Mon Jul 19 1999 ma@suse.de
- again rebuilddb.patch
* Wed Jul 14 1999 ro@suse.de
- update to 3.0.3
* Sun Jun 27 1999 ro@suse.de
- changed macros.in for libc5 : no "h" parameter for chown,chmod
* Fri Jun 25 1999 ro@suse.de
- update to rpm-3.0.2
- added librpmbuild.a to filelist
- added patch not to generate dependency for libNoVersion
- rebuilddb.patch removed (incorporated in source)
* Thu Jun 17 1999 ma@suse.de
- fixed bug when --rebuilddb and --root where used
  at the same time.
* Wed May 26 1999 ro@suse.de
- update to 3.0.1
* Mon Apr 26 1999 werner@suse.de
- Speed up find-requires for linux
* Mon Apr 26 1999 ro@suse.de
- update to 3.0 (noreplace fix has been incorporated)
* Mon Apr 12 1999 ro@suse.de
- update to 2.93
* Fri Mar 19 1999 ro@suse.de
- update to 2.92
* Thu Mar 18 1999 ro@suse.de
- respect movement of libz to usr/lib
* Sun Feb 28 1999 ro@suse.de
- update to rpm-src from 99/02/25
* Sat Feb 27 1999 ro@suse.de
- install both dirs RPM/i386 and RPM/alpha (since buildarch doesn't
  seem to be defined now ?)
* Tue Feb 23 1999 ro@suse.de
- adapted macros file to SuSE
- fixed segfault when not using BuildRoot
* Tue Feb 23 1999 ro@suse.de
- modified diff-style
- use additional parameter "-h" on chown after unpacking in build
* Mon Feb 22 1999 ro@suse.de
- update to 2.91
- ported ma's fixes
* Wed Nov 25 1998 ma@suse.de
- new version 2.5.5
- fixed in 2.5.5: find-requires/provides bug
- fixed in 2.5.5: rebuilddb
* Wed Nov 18 1998 ma@suse.de
- link rpm.dyn dynamic against libc only
* Mon Nov 16 1998 ma@suse.de
- shared binary (/usr/lib/rpm/rpm.dyn) added
* Tue Nov 10 1998 ro@suse.de
- fixed find-requires (linux.req)
* Mon Nov  9 1998 ro@suse.de
- added %%post: do rpm --initdb if triggerindex.rpm doesn't exist
- do chown root.root for RPM-HOWTO
* Thu Nov  5 1998 ma@suse.de
- new version 2.5.4
- fix for rebuilddb
- fix for %%config(noreplace)
- RPM-Changes html document that describes the important changes
  in RPM since what is documented in Maximum RPM.
* Tue Nov  3 1998 ro@suse.de
- disabled glibc-patch for build in glibc-2.0
* Sun Sep 20 1998 ro@suse.de
- use libdb185.a for rpm in glibc system
* Thu Sep  3 1998 ma@suse.de
- glibc patches
* Thu Feb  5 1998 ro@suse.de
- update to 2.4.12
* Tue Dec  9 1997 bs@suse.de
- skip *.SuSE-dynamic in find-requires
* Wed Nov 12 1997 ma@suse.de
- new version 2.4.10
* Sat Nov  8 1997 ma@suse.de
- patch: rpmdbFindByFile() didn't work for "/". Thus "/" wasn't
    handled correctly in querries and upon updates ("rmdir /").
* Mon Oct 27 1997 ma@suse.de
- new version 2.4.8
- spec file for autobuild provided
  - dirs below /usr/src/packages are installed mode 1777
- obsolete: patch to allow installing rpm v1 packages (from Aug  7 1997)
    Seems to be fixed in 2.4.8
- patch: always 'chdir /' before executing scripts.
- patch: remove empty dirs when installing a symlink
- patch: ignore errors when installing a symlink and called from YaST
- de.po update
* Thu Aug  7 1997 ma@suse.de
- duplicate '--nodeps' entry in rpm manpage deleted.
- quick patch to allow installing rpm v1 packages.
- workaround to skip installing a symlink (Jul 15 1997)
  is disabeled, unless environment variable RPM_IgnoreFailedSymlinks
  is set.
* Tue Jul 15 1997 ro@suse.de
- added workaround to skip installing a symlink when
  impossible to remove an existing directory
* Thu Jun 26 1997 ma@suse.de
- introducing rpm, version 2.4.1
- documentation (ascii,html) in usr/doc/packages/rpm
