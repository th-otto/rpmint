%define pkgname mtm

%rpmint_header

Summary:        mtm is the Micro Terminal Multiplexer, a terminal multiplexer
Name:           %{crossmint}%{pkgname}
Version:        1.2.1
Release:        1
License:        GPL-3.0-or-later
Group:          System/Console

Packager:       %{packager}
URL:            https://github.com/deadpixi/mtm/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.gz

Patch0: patches/mtm/mtm-1.2.1-m68k-atari-mint.patch

%rpmint_essential
BuildRequires:  make
BuildRequires:  ncurses-devel

%rpmint_build_arch

%description
mtm is the Micro Terminal Multiplexer, a terminal multiplexer.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--config-cache
"
COMMON_CFLAGS="-std=c99 -Wall -Wextra -pedantic -Os -fomit-frame-pointer $LTO_CFLAGS"

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

	make CC="${TARGET}-gcc" CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"

	install -Dpm 0755 mtm "%{buildroot}%{_rpmint_bindir}/mtm"
	install -Dpm 0644 mtm.1 "%{buildroot}%{_rpmint_mandir}/man1/mtm.1"
	tic -s -x -o "%{buildroot}%{_rpmint_datadir}/terminfo" mtm.ti
	make clean

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
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
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/share/terminfo/*/*


%changelog
* Sun Apr 09 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
