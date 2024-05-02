%define pkgname meson

%rpmint_header

Summary:        Python-based build system
Name:           %{crossmint}%{pkgname}
Version:        1.4.0
Release:        1
License:        Apache-2.0
Group:          Development/Tools/Building

URL:            https://mesonbuild.com/
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        https://github.com/mesonbuild/meson/releases/download/%{version}/meson-%{version}.tar.gz
Source1:        patches/%{pkgname}/meson-m68k-atari-mint.ini
Source2:        patches/%{pkgname}/meson-m68k-atari-mintelf.ini

Patch0:         patches/%{pkgname}/meson-test-installed-bin.patch
Patch1:         patches/%{pkgname}/meson-distutils.patch
Patch2:         patches/%{pkgname}/meson-mint.patch

%rpmint_essential
BuildRequires:  python3 >= 3.7
Provides:       %{name}-vim
Requires:       ninja >= 1.8.2

%rpmint_build_arch

%description
Meson is a build system designed to optimise programmer productivity.
It aims to do this by providing support for software development
tools and practices, such as unit tests, coverage reports, Valgrind,
CCache and the like. Supported languages include C, C++, Fortran,
Java, Rust. Build definitions are written in a non-turing complete
Domain Specific Language.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%rpmint_cflags

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

	python3 setup.py build

	python_version=3.11
	_rpmconfigdir=%{_rpmint_prefix}/lib/rpm
	vim_data_dir=%{_rpmint_prefix}/share/vim
	python_sitelib=%{_rpmint_prefix}/lib/python${python_version}/site-packages

	python3 setup.py install -O1 --skip-build --force --root %{buildroot} --prefix %{_rpmint_prefix}
	install -Dpm 0644 data/macros.meson %{buildroot}${_rpmconfigdir}/macros.d/macros.meson
	install -Dpm 0644 data/syntax-highlighting/vim/ftdetect/meson.vim -t %{buildroot}${vim_data_dir}/site/ftdetect/
	install -Dpm 0644 data/syntax-highlighting/vim/indent/meson.vim -t %{buildroot}${vim_data_dir}/site/indent/
	install -Dpm 0644 data/syntax-highlighting/vim/syntax/meson.vim -t %{buildroot}${vim_data_dir}/site/syntax/
	echo """#!%{_rpmint_target_prefix}/bin/python3
from mesonbuild.mesonmain import main
import sys

sys.exit(main())
""" > %{buildroot}%{_rpmint_prefix}/bin/meson
	chmod +x %{buildroot}%{_rpmint_prefix}/bin/meson

	cp -r meson.egg-info %{buildroot}${python_sitelib}/meson-%{version}-py${python_version}.egg-info

# Fix missing data files with distutils
	while read line; do
	  if [[ "$line" = %{_name}/* ]]; then
	    [[ "$line" = *.py ]] && continue
	    cp "$line" "%{buildroot}${python_sitelib}/$line"
	  fi
	done < meson.egg-info/SOURCES.txt

# remove linux-specific polkit
	rm -rf %{buildroot}%{_rpmint_prefix}/share/polkit-1

	# only include the cross configurations in the *-dev archive
	%if "%{buildtype}" == "cross"
		rm -rf "%{buildroot}%{prefix}"
	%endif
	
	install -Dpm 0644 "%{S:1}" "%{buildroot}%{prefix}/share/meson/cross/m68k-atari-mint.ini"
	install -Dpm 0644 "%{S:2}" "%{buildroot}%{prefix}/share/meson/cross/m68k-atari-mintelf.ini"

	python3 setup.py clean

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	python3 setup.py clean
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{prefix}/share/meson/cross
%else
%license COPYING
%doc data/syntax-highlighting/vim/README
%{_isysroot}%{_rpmint_target_prefix}/bin/meson
%{_isysroot}%{_rpmint_target_prefix}/share
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%endif


%changelog
* Fri Apr 19 2024 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file for version 1.4.0
