%define pkgname mintlib

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

Summary:        Header files for MiNTLib
Name:           cross-mint-mintlib-headers
Version:        0.60.1
Release:        1
License:        LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND GPL-2.0-or-later
Packager:       Thorsten Otto <admin@tho-otto.de>
Vendor:         RPMint
Source:         %{pkgname}-%{version}.tar.xz

%rpmint_build_arch

%description
Header files for MiNTLib

%prep
%setup -q -n %{pkgname}-%{version}

%build

%install

%if "%{buildtype}" == "cross"
make prefix=${RPM_BUILD_ROOT}%{_rpmint_sysroot}/usr install-include-recursive
%else
make prefix=${RPM_BUILD_ROOT}/usr install-include-recursive
%endif

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

