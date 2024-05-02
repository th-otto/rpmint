%define pkgname ninja

%rpmint_header

Summary:        A small build system closest in spirit to Make
Name:           %{crossmint}%{pkgname}
Version:        1.11.1
Release:        1
License:        Apache-2.0
Group:          Development/Tools/Building

URL:            https://ninja-build.org/
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        https://github.com/ninja-build/ninja/archive/v%{version}/%{pkgname}-%{version}.tar.gz
Source1:        patches/%{pkgname}/ninja-macros.ninja

Patch0:         patches/%{pkgname}/ninja-disable-maxprocs-test.patch
Patch1:         patches/%{pkgname}/ninja-re2c-g.patch
Patch2:         patches/%{pkgname}/ninja-mint.patch

%rpmint_essential
BuildRequires:  gcc-c++
BuildRequires:  python3-base
BuildRequires:  re2c

%rpmint_build_arch

%description
Ninja is yet another build system. It takes as input the interdependencies
of files (typically source code and output executables) and orchestrates
building them, quickly.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

python3 ./configure.py --verbose --bootstrap
mv ninja build-ninja
rm -rf build build.ninja

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS ${ELF_CFLAGS}"

STACKSIZE="-Wl,-stack,512k"

for CPU in %{buildtype}
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}

	CXX=%{_rpmint_target}-g++ \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	AR=%{_rpmint_target}-ar \
	LDFLAGS="$STACKSIZE -s" \
	python3 ./configure.py --verbose --host=mint
	./build-ninja -v %{?_smp_mflags}

	install -D -p -m 0755 ninja %{buildroot}%{_rpmint_bindir}/ninja
	install -D -p -m 0644 misc/zsh-completion %{buildroot}%{_rpmint_datadir}/zsh/site-functions/_ninja
	install -D -p -m 0644 misc/ninja.vim %{buildroot}%{_rpmint_datadir}/vim/site/syntax/ninja.vim
	install -D -p -m 0644 misc/bash-completion %{buildroot}%{_rpmint_datadir}/bash-completion/completions/ninja
	install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_rpmint_prefix}/lib/rpm/macros.d/macros.ninja

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	rm -rf build build.ninja
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license COPYING
%{_isysroot}%{_rpmint_target_prefix}/bin/ninja
%{_isysroot}%{_rpmint_target_prefix}/share
%{_isysroot}%{_rpmint_target_prefix}/lib/rpm/macros.d/macros.ninja


%changelog
* Fri Apr 19 2024 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file for version 1.11.1
