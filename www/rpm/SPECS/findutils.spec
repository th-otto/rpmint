%define pkgname findutils

%rpmint_header

Summary:        The GNU versions of find utilities (find and xargs)
Name:           %{crossmint}%{pkgname}
Version:        4.7.0
Release:        1
License:        GPL-3.0-or-later
Group:          Productivity/File utilities

Prereq:         /sbin/install-info

Packager:       %{packager}
URL:            http://www.gnu.org/software/findutils/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://ftp.gnu.org/pub/gnu/%{pkgname}/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Source2: patches/findutils/findutils-updatedb.cron

Patch0:  patches/findutils/findutils-4.7-xautofs.patch
Patch1:  patches/findutils/findutils-4.7-mint.patch
Patch2:  patches/findutils/findutils-notexinfo-clean.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make

%rpmint_build_arch

%description
The findutils package contains programs which will help you locate
files on your system.  The find utility searches through a hierarchy
of directories looking for files which match a certain set of criteria
(such as a file name pattern).  The xargs utility builds and executes
command lines from standard input arguments (usually lists of file
names generated by the find command).

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--disable-nls
	--disable-shared
	--localstatedir=/var/lib
	--config-cache
"
STACKSIZE="-Wl,-stack,128k"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_header_pthread_h=no
gl_have_pthread_h=no
EOF
	%rpmint_append_gnulib_cache
}

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
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir \
	--libexecdir='${exec_prefix}/libexec/find'$multilibexecdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
		rm -f %{buildroot}%{_rpmint_sysroot}/usr/libexec/find${multilibexedir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make clean >/dev/null
done


%install

%rpmint_cflags

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

mkdir -p %{buildroot}%{_isysroot}/etc/cron.daily
install -m 644 %{S:2} %{buildroot}%{_isysroot}/etc/cron.daily/updatedb.cron

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS NEWS README TODO THANKS ChangeLog
%config %{_isysroot}/etc/cron.daily/updatedb.cron
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/libexec/find
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/share/info/*


%post
%rpmint_install_info %{pkgname}

%preun
%rpmint_uninstall_info %{pkgname}

%changelog
* Thu Apr 06 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 4.7.0

* Fri Sep 14 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 4.1.7

* Wed Apr 19 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
