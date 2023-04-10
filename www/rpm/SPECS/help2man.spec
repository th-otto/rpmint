%define pkgname help2man

%rpmint_header

Name:           %{crossmint}%{pkgname}
Version:        1.49.3
Release:        1
Summary:        Script for generating man pages from --help output
License:        GPL-3.0-or-later
Group:          Development/Tools/Doc Generators
URL:            https://www.gnu.org/software/help2man/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        https://ftp.gnu.org/gnu/help2man/%{pkgname}-%{version}.tar.xz

BuildRequires:  perl-gettext
Requires:       perl-gettext

BuildArch:      noarch
%if "%{buildtype}" != "cross"
%define _arch noarch
%endif

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a way
to generate a placeholder man page pointing to that resource while
still providing some useful information.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--disable-nls
"

NO_STRIP=true

for CPU in noarch; do
	CFLAGS="$COMMON_CFLAGS" \
	LDFLAGS="$COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS}

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	make clean >/dev/null
done


%rpmint_cflags

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

%install

%rpmint_cflags

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



%post
%rpmint_install_info %{pkgname}

%preun
%rpmint_uninstall_info %{pkgname}


%files
%license COPYING
%doc NEWS README THANKS debian/changelog
%{_isysroot}%{_rpmint_target_prefix}/bin/help2man
%{_isysroot}%{_rpmint_target_prefix}/share/info/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*

%changelog
* Mon Apr 10 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 1.49.3

