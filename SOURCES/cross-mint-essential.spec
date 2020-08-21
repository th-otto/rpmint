%if "%{?buildtype}" == ""
%define buildtype cross
%endif

Summary:        Atari MiNT cross-compiler tools
%if "%{buildtype}" == "cross"
Name:           cross-mint-essential
%else
Name:           mint-devel-essential
%endif
Release:        1
Packager:       Thorsten Otto <admin@tho-otto.de>
Vendor:         RPMint

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
