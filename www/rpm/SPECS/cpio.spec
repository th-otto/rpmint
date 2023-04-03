%define pkgname cpio

%rpmint_header

Summary:        A Backup and Archiving Utility
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        2.13
Release:        1
License:        GPL-3.0-only
Group:          Productivity/Archiving/Backup

URL:            https://www.gnu.org/software/cpio/cpio.html
Packager:       Thorsten Otto <admin@tho-otto.de>

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.bz2
Source1:        patches/automake/mintelf-config.sub

Patch0:         cpio-2.3-lstat.patch
Patch1:         cpio-2.4.2-glibc.patch
Patch2:         cpio-2.4.2-mtime.patch
Patch3:         cpio-2.4.2-svr4compat.patch
Patch4:         cpio-2.4.2-glibc21.patch
Patch5:         cpio-2.4.2-longlongdev.patch

Patch6:         cpio-use_new_ascii_format.patch
Patch7:         cpio-use_sbin_rmt.patch
#PATCH-FIX-UPSTREAM cpio-2.12 cpio-open_nonblock.patch bnc#94449,
#https://savannah.gnu.org/patch/?9263 -- open device with O_NONBLOCK option
Patch8:         cpio-open_nonblock.patch
Patch15:        cpio-eof_tape_handling.patch
# make possible to have device nodes with major number > 127
# Red Hat Bugzilla #450109
Patch17:        cpio-dev_number.patch
Patch18:        cpio-default_tape_dev.patch
#PATCH-FIX-UPSTREAM cpio-2.10-close_files_after_copy.patch
Patch20:        cpio-close_files_after_copy.patch
Patch21:        cpio-pattern-file-sigsegv.patch
Patch23:        cpio-paxutils-rtapelib_mtget.patch
Patch24:        cpio-check_for_symlinks.patch
Patch25:        cpio-fix_truncation_check.patch
Patch26:        cpio-2.12-util.c_no_return_in_nonvoid_fnc.patch
Patch27:        cpio-2.12-CVE-2016-2037-out_of_bounds_write.patch
Patch28:        cpio-2.12-CVE-2019-14866.patch
Patch29:        cpio-no-mtiocget.patch
Patch30:        cpio-filemode.patch
Patch40:        patches/cpio/cpio-revert-CVE-2015-1197-fix.patch
Patch41:        patches/cpio/cpio-fix-CVE-2021-38185.patch
Patch42:        patches/cpio/cpio-fix-CVE-2021-38185_2.patch
Patch43:        patches/cpio/cpio-fix-CVE-2021-38185_3.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
Recommends:     rmt

%rpmint_build_arch

%description
GNU cpio is a program to manage archives of files. Cpio copies files
into or out of a cpio or tar archive. An archive is a file that contains
other files plus information about them, such as their pathname, owner,
time stamps, and access permissions. The archive can be another file on
the disk, a magnetic tape, or a pipe.

%prep
%setup -q -n %{pkgname}-%{version}
# patches 0-5 not applied
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch15 -p1
%patch17 -p1
#%patch18 -p1
%patch20 -p1
%patch21 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
# patch27 -p1 already applied in 2.13
# patch28 -p1 already applied in 2.13
%patch29 -p1
%patch30 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1

cp %{S:1} build-aux/config.sub

%build

create_config_cache()
{
cat <<EOF >config.cache
EOF
	%rpmint_append_gnulib_cache
}


%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
	--libexecdir=%{_rpmint_target_prefix}/lib \
	--disable-nls \
	--with-rmt=/usr/bin/rmt \
	--sbindir=/sbin
"
STACKSIZE="-Wl,-stack,256k"

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
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	# according to FHS 3.0, cpio must be in /bin
	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	mkdir -p %{buildroot}/bin
	rm -f %{buildroot}/bin/cpio
	ln %{buildroot}%{_rpmint_target_prefix}/bin/cpio %{buildroot}/bin
	%else
	mkdir -p %{buildroot}%{_rpmint_sysroot}/bin
	rm -f %{buildroot}%{_rpmint_sysroot}/bin/cpio
	ln %{buildroot}%{_rpmint_bindir}/cpio %{buildroot}%{_rpmint_sysroot}/bin
	%endif

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
%doc NEWS ChangeLog
%if "%{buildtype}" == "cross"
%{_rpmint_sysroot}/bin/cpio
%{_rpmint_bindir}/cpio
%{_rpmint_datadir}
%else
/bin/cpio
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/share
%endif


%changelog
* Fri Mar 03 2023 Thorsten Otto <admin@tho-otto.de>
- Update to version 2.13

* Tue Sep 22 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
- Update to version 2.12

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
