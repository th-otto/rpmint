%define pkgname essential

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Atari MiNT cross-compiler tools
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           mint-devel-%{pkgname}
%endif
Version:        1.0
Release:        1
License:        GPL
Packager:       Thorsten Otto <admin@tho-otto.de>
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

%if "%{buildtype}" == "cross"
BuildArch:      noarch
Requires:       cross-mint-binutils
Requires:       cross-mint-mintbin
Requires:       cross-mint-gcc
Requires:       cross-mint-mintlib
Requires:       cross-mint-fdlibm
Requires:       cross-mint-gemlib

%else
Requires:       binutils
Requires:       mintbin
Requires:       gcc
Requires:       mintlib
Requires:       fdlibm
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

%prep
mkdir -p ${RPM_BUILD_ROOT}

%build

%install

%files
