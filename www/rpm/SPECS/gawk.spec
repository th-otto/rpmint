%define pkgname gawk

%rpmint_header

Summary:        GNU awk
Name:           %{crossmint}%{pkgname}
Version:        4.1.4
Release:        1
License:        GPL-3.0-or-later
Group:          Productivity/Text/Utilities

Prereq:         /sbin/install-info

Packager:       %{packager}
URL:            http://www.gnu.org/software/gawk/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/gawk/gawk-ppc64le_ignore_transient_test_time_failure.patch
Patch1: patches/gawk/gawk-4.1.4-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make

%rpmint_build_arch

%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--config-cache
"
STACKSIZE=-Wl,-stack,256k

create_config_cache()
{
cat <<EOF >config.cache
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
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir \
	--libexecdir='${exec_prefix}/libexec'$multilibexecdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/usr/bin/gawk-%{version}

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	# install via macro later
	rm -fv %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}/COPYING*

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
		rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/libexec$multilibexecdir/*
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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%license COPYING*
%doc ABOUT-NLS POSIX.STD NEWS* README_d README AUTHORS ChangeLog*
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/libexec/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/share/info/*
%{_isysroot}%{_rpmint_target_prefix}/share/awk
%{_isysroot}%{_rpmint_target_prefix}/share/locale/*/*/*


%post
%rpmint_install_info %{pkgname}

%preun
%rpmint_uninstall_info %{pkgname}


%changelog
* Fri Apr 07 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 4.1.4

* Tue Mar 20 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 3.0.6

* Mon Sep 20 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- package provide awk now

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
- added Summary(de)
