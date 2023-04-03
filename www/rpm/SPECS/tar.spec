%define pkgname tar

%rpmint_header

Summary:        GNU implementation of ((t)ape (ar)chiver)
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.34
Release:        1
License:        GPL-3.0-or-later
Group:          Productivity/Archiving/Backup

URL:            http://www.gnu.org/software/tar/
Packager:       Thorsten Otto <admin@tho-otto.de>

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.xz
Source1:        patches/automake/mintelf-config.sub

Patch0:         patches/%{pkgname}/tar-wildcards.patch
Patch1:         patches/%{pkgname}/tar-backup-spec-fix-paths.patch
Patch2:         patches/%{pkgname}/tar-paxutils-rtapelib_mtget.patch
# don't print warning about zero blocks
# the patch is used in Fedora and Debian
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=235820
Patch3:         patches/%{pkgname}/tar-ignore_lone_zero_blocks.patch
Patch4:         patches/%{pkgname}/tar-add_readme-tests.patch
Patch5:         patches/%{pkgname}/tar-1.29-extract_pathname_bypass.patch
Patch6:         patches/%{pkgname}/tar-tests-skip-time01-on-32bit-time_t.patch
# PATCH-FIX-UPSTREAM danilo.spinella@suse.com bsc#1200657
# fix race condition while creating intermediate subdirectories
Patch7:         patches/%{pkgname}/tar-fix-race-condition.patch
# PATCH-FIX-UPSTREAM danilo.spinella@suse.com bsc#1203600
# Unexpected inconsistency when making directory
Patch9:         patches/%{pkgname}/tar-avoid-overflow-in-symlinks-tests.patch
Patch10:        patches/%{pkgname}/tar-bsc1200657.patch
Patch11:        patches/%{pkgname}/tar-fix-extract-unlink.patch
# PATCH-FIX-SUSE danilo.spinella@suse.com bsc#1202436
Patch12:        patches/%{pkgname}/tar-go-testsuite-test-hang.patch
# PATCH-FIX-UPSTREAM danilo.spinella@suse.com bsc#1202436
Patch13:        patches/%{pkgname}/tar-bsc1202436.patch
Patch14:        patches/%{pkgname}/tar-bsc1202436-1.patch
Patch15:        patches/%{pkgname}/tar-bsc1202436-2.patch
# PATCH-FIX-UPSTREAM danilo.spinella@suse.com bsc#1207753
# tar has a one-byte out-of-bounds read that results in use of
# uninitialized memory for a conditional jump
Patch16:        patches/%{pkgname}/tar-fix-CVE-2022-48303.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
%if "%{buildtype}" != "cross"
Recommends:     %{pkgname}-rmt = %{version}
Recommends:     mt
Recommends:     xz
Recommends:     zstd
Provides:       base:/bin/tar
%endif

%rpmint_build_arch

%description
GNU Tar is an archiver program. It is used to create and manipulate files
that are actually collections of many other files; the program provides
users with an organized and systematic method of controlling a large amount
of data. Despite its name, that is an acronym of "tape archiver", GNU Tar
is able to direct its output to any available devices, files or other programs,
it may as well access remote devices or files.

#%%package rmt
#Summary:        Remote tape drive control server by GNU
#Group:          Productivity/Archiving/Backup
#Requires(post): update-alternatives
#Requires(postun):update-alternatives
#%%if "%%{buildtype}" != "cross"
#Provides:       rmt
#%endif

#%%description rmt
#Provides remote access to files and devices for tar, cpio
#and similar backup utilities

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1

autoreconf -fiv
rm -f build-aux/config.sub
cp %{S:1} build-aux/config.sub

%build

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_header_pthread_h=no
gl_have_pthread_h=no
EOF
	%rpmint_append_gnulib_cache
}


%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--program-transform-name='s/^rmt$/gnurmt/'
	--libexecdir=%{_rpmint_target_prefix}/lib
	--disable-nls
	--sbindir=/sbin
	--config-cache
"
STACKSIZE="-Wl,-stack,256k"

export RSH=%{_rpmint_target_prefix}/bin/ssh
export DEFAULT_ARCHIVE_FORMAT="POSIX"
export DEFAULT_RMT_DIR=%{_rpmint_target_prefix}/bin


[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 000
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -s ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS}

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# For avoiding file conflicts with dump/restore
	# mv %{buildroot}%{_rpmint_sysroot}/sbin/restore %{buildroot}%{_rpmint_sysroot}/sbin/restore.sh

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	install -D -m 644 scripts/backup-specs %{buildroot}%{_rpmint_sysroot}/etc/backup/backup-specs

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	# according to FHS 3.0, tar must be in /bin
	mkdir -p %{buildroot}%{_isysroot}/bin
	rm -f %{buildroot}%{_isysroot}/bin/tar
	ln -s ../usr/bin/tar %{buildroot}%{_isysroot}/bin

	make distclean
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%rpmint_install_info %{pkgname}

%preun
%rpmint_uninstall_info %{pkgname}

%files
%defattr(-,root,root)
%license COPYING
%doc README* ABOUT-NLS AUTHORS NEWS THANKS ChangeLog TODO COPYING
%config(noreplace) %{_isysroot}/etc/backup/*
%{_isysroot}/bin/tar
%{_isysroot}%{_rpmint_target_prefix}/bin/tar
%{_isysroot}%{_rpmint_target_prefix}/share


%changelog
* Sat Apr 01 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 1.34

* Sun Aug 29 2010 P Slegg
- update to 1.24r4
- removed 2 patch files
- moved info files

* Sun Feb 08 2004 Mark Duckworth <mduckworth@atari-source.com>
- Changed packager due to big changes
- upgraded to latest version
- added some fixes
- fix bug where can't find gzip

* Fri Jan 30 2004 Mark Duckworth <mduckworth@atari-source.com>
- Compiled against latest MiNTlib, version 0.57.4

* Thu Feb 03 2000 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT (version 1.13)
- fixed symlink bug, removed obsolete manpage stuff (specfile)

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
- added %%description de and Summary(de)
