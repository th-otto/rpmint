%define pkgname test

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        The GNU MP Library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        6.1.2
Release:        1
License:        GPL-3.0+ and LGPL-3.0+
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://gmplib.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

BuildRequires:  cross-mint-gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  xz

%if "%{buildtype}" == "cross"
BuildArch:      noarch
%else
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
A library for calculating huge numbers (integer and floating point).

%prep

%build

%install

%if "%{buildtype}" == "cross"
mkdir -p %{buildroot}/%{_rpmint_includedir}
touch %{buildroot}/%{_rpmint_includedir}/test.h
%else
mkdir -p %{buildroot}/%{_rpmint_target_prefix}/include/
touch %{buildroot}/%{_rpmint_target_prefix}/include/test.h
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/*
%else
%{_rpmint_target_prefix}/include/*
%endif


%changelog
* Thu Aug 27 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
