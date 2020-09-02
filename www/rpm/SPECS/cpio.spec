%define pkgname cpio

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        2.13
Release:        1
Summary:        A Backup and Archiving Utility
License:        GPL-3.0-only
Group:          Productivity/Archiving/Backup
URL:            https://www.gnu.org/software/cpio/cpio.html
Packager:       Thorsten Otto <admin@tho-otto.de>
Source:         https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.bz2
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

BuildRequires:  autoconf
BuildRequires:  automake
Requires(post): %{install_info_prereq}
Requires(preun): %{install_info_prereq}
Recommends:     rmt

%if "%{buildtype}" == "cross"
BuildArch:      noarch
%else
%define _target_platform %{_rpmint_target_platform}
%if "%{buildtype}" == "v4e"
%define _arch m5475
%else
%if "%{buildtype}" == "020"
%define _arch m68020
%else
%define _arch m68k
%endif
%endif
%endif

%description
GNU cpio is a program to manage archives of files. Cpio copies files
into or out of a cpio or tar archive. An archive is a file that contains
other files plus information about them, such as their pathname, owner,
time stamps, and access permissions. The archive can be another file on
the disk, a magnetic tape, or a pipe.

%prep
%setup -q
# patches 0-5 not applied
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch15 -p1
%patch17 -p1
%patch18 -p1
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

%build
rm -f aclocal.m4 ltmain.sh
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"
STACKSIZE="-Wl,-stack,256k"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
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

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
#UsrMerge
	mkdir -p %{buildroot}/bin
	ln -sf %{_rpmint_bindir}/cpio %{buildroot}/bin
#EndUsrMerge
	%rpmint_make_bin_archive $CPU
	%endif

	make distclean
done

%install

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%rpmint_install_info %{pkgname}

%preun
%rpmint_uninstall_info %{pkgname}

%files
%license COPYING
%doc NEWS ChangeLog
#UsrMerge
/bin/cpio
/usr/bin/mt
/usr/info/cpio.*
/usr/man/man1/cpio.1.gz

%changelog
* Wed Sep 22 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
- Update to version 2.12

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
