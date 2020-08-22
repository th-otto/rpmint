%if "%{?buildtype}" == ""
%define buildtype cross
%endif

Summary:        Atari MiNT cross-compiler tools
%if "%{buildtype}" == "cross"
Name:           cross-mint-essential
%else
Name:           mint-devel-essential
%endif
Version:        1.0
Release:        1
License:        GPL
Packager:       Thorsten Otto <admin@tho-otto.de>
Vendor:         RPMint
BuildArch:      noarch

%description
Atari MiNT cross-compiler tools.
This package depends on all the essential tools
to cross-build Atari MiNT software.

BuildRequires:  cross-mint-binutils
BuildRequires:  cross-mint-mintbin
BuildRequires:  cross-mint-gcc
BuildRequires:  cross-mint-mintlib
BuildRequires:  cross-mint-fdlibm
BuildRequires:  cross-mint-gemlib

%rpmint_build_arch

%prep
mkdir -p ${RPM_BUILD_ROOT}

%build

%install

%files
