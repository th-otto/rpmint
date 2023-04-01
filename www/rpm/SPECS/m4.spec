%define pkgname m4

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        GNU m4
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.4.18
Release:        1
License:        GPL-3.0-or-later
Group:          Development/Languages/Other

URL:            https://www.gnu.org/software/m4/m4.html
Packager:       Thorsten Otto <admin@tho-otto.de>

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        ftp://ftp.gnu.org/gnu/%{name}/%{pkgname}-%{version}.tar.xz
Source1:        patches/automake/mintelf-config.sub

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
Prereq		: /sbin/install-info

%rpmint_build_arch

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

rm -f build-aux/config.sub
cp %{S:1} build-aux/config.sub

%build

create_config_cache()
{
cat <<EOF >config.cache
gl_cv_func_isnanl_works=yes
gl_cv_func_printf_directive_n=yes
gl_cv_func_printf_infinite_long_double=yes
EOF
	%rpmint_append_gnulib_cache
}


%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--without-included-regex
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

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
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
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share



%changelog
* Sat Apr 01 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 1.4.18

* Thu Oct 21 2010 Keith Scroggins <kws@radix.net>
- Updated to 1.4.15

* Mon May 05 2003 Marc-Anton Kehr <m.kehr@ndh.net>
- updated to 1.4.1
