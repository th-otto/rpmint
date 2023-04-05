%define pkgname autoconf-archive

%rpmint_header

Summary:        A Collection of macros for GNU autoconf
Name:           %{crossmint}%{pkgname}
Version:        2023.02.20
Release:        1
License:        GPL-3.0-or-later WITH Autoconf-exception-3.0
Group:          Development/Tools/Building

Packager:       %{packager}
URL:            https://savannah.gnu.org/projects/autoconf-archive

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.gnu.org/pub/gnu/autoconf-archive/%{pkgname}-%{version}.tar.xz

BuildArch:      noarch
%if "%{buildtype}" != "cross"
%define _arch noarch
%endif

%description
The GNU Autoconf Archive is a collection of more than 450 macros for `GNU
Autoconf <http://www.gnu.org/software/autoconf>` that have been contributed as
free software by friendly supporters of the cause from all over the Internet.
Every single one of those macros can be re-used without imposing any
restrictions whatsoever on the licensing of the generated `configure` script. In
particular, it is possible to use all those macros in `configure` scripts that
are meant for non-free software. This policy is unusual for a Free Software
Foundation project. The FSF firmly believes that software ought to be free, and
software licenses like the GPL are specifically designed to ensure that
derivative work based on free software must be free as well. In case of
Autoconf, however, an exception has been made, because Autoconf is at such a
pivotal position in the software development tool chain that the benefits from
having this tool available as widely as possible outweigh the disadvantage that
some authors may choose to use it, too, for proprietary software.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
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

	# install via macro later
	rm -fv %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}/COPYING*

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	make clean >/dev/null
done


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
%defattr(-,root,root)
%license COPYING*
%doc AUTHORS README
%dir %{_isysroot}%{_rpmint_target_prefix}/share/aclocal
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal/*
%{_isysroot}%{_rpmint_target_prefix}/share/info/*



%changelog
* Wed Apr 05 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
