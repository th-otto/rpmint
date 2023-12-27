%define pkgname essential

%rpmint_header

Summary:        Atari MiNT cross-compiler tools
if "%{_rpmint_target}" == "m68k-atari-mintelf" \
%if "%{buildtype}" == "cross"
Name:           cross-mintelf-%{pkgname}
%else
Name:           mintelf-devel-%{pkgname}
%endif
%else
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           mint-devel-%{pkgname}
%endif
%endif
Version:        1.0
Release:        1
License:        GFDL-1.3-only AND GPL-3.0-or-later AND GPL-3.0+
Packager:       Thorsten Otto <admin@tho-otto.de>

BuildRequires:  %{crossmint}binutils
BuildRequires:  %{crossmint}gcc
BuildRequires:  %{crossmint}mintlib
BuildRequires:  %{crossmint}fdlibm
BuildRequires:  %{crossmint}mintbin
BuildRequires:  %{crossmint}gemlib

%if "%{buildtype}" == "cross"
BuildArch:      noarch
Requires:       %{crossmint}binutils
Requires:       %{crossmint}gcc
Requires:       %{crossmint}mintlib
Requires:       %{crossmint}fdlibm
Requires:       %{crossmint}mintbin
Requires:       %{crossmint}gemlib

%else
Requires:       binutils
Requires:       gcc
Requires:       mintlib
Requires:       fdlibm
Requires:       mintbin
Requires:       gemlib

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
Atari MiNT cross-compiler tools.
This package depends on all the essential tools
to cross-build Atari MiNT software.

%prep
mkdir -p ${RPM_BUILD_ROOT}

%build

%install

%files
