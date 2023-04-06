%define pkgname ctris

%rpmint_header

Summary:        ctris is a curses based Tetris game
Name:           %{crossmint}%{pkgname}
Version:        0.42
Release:        1
License:        GPL-2.0-or-later
Group:          Amusements/Games/Action/Arcade

Packager:       %{packager}
URL:            http://hackl.dhs.org/ctris/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.bz2


%rpmint_essential
BuildRequires:  make
BuildRequires:  %{crossmint}ncurses-devel

%rpmint_build_arch

%description
ctris is a curses based Tetris game.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS+=" -fcommon"

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

	make CC=%{_rpmint_target_gcc} CFLAGS="${CPU_CFLAGS} $COMMON_CFLAGS ${LTO_CFLGS} -s"
	make MANDIR="%{buildroot}%{_rpmint_mandir}/man6" BINDIR="%{buildroot}%{_rpmint_prefix}/games" install || exit 1

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make clean
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
%license COPYING
%doc TODO README AUTHORS
%{_isysroot}%{_rpmint_target_prefix}/games/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*



%changelog
* Thu Apr 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
