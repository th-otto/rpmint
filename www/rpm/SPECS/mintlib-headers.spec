%define pkgname mintlib

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Header files for MiNTLib
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}-headers
%else
Name:           %{pkgname}-headers
%endif
Version:        0.60.1
Release:        2
License:        LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND GPL-2.0-or-later
Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/freemint/mintlib
Source:         %{pkgname}-%{version}.tar.xz

%rpmint_build_arch

%description
Header files for MiNTLib.
This package is only needed to bootstrap compilation of GCC.

%prep
%setup -q -n %{pkgname}-%{version}

%build

%install

%if "%{buildtype}" == "cross"
prefix=%{_rpmint_prefix}
%else
prefix=%{_rpmint_target_prefix}
%endif
make prefix=${RPM_BUILD_ROOT}${prefix} install-include-recursive

pushd ${RPM_BUILD_ROOT}
find . \( -name 00README \
	-o -name COPYING \
	-o -name COPYING.LIB \
	-o -name COPYMINT \
	-o -name BINFILES \
	-o -name MISCFILES \
	-o -name SRCFILES \
	-o -name EXTRAFILES \
	-o -name Makefile \
	-o -name clean-include \) -delete -printf "rm %%p\n"
popd

%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/*
%else
%{_rpmint_target_prefix}/include/*
%endif

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

