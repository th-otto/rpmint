%define pkgname fdlibm

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

Summary:        Header files for fdlibm
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}-headers
%else
Name:           %{pkgname}-headers
%endif
Version:        20200108
Release:        1
License:        Public domain
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
Vendor:         RPMint
URL:            https://www.netlib.org/fdlibm/

Prefix:         %{_prefix}
BuildRoot:      %{_tmppath}/%{name}-root

Source:         %{pkgname}-%{version}.tar.xz

%rpmint_build_arch

%description
Header files for fdlibm.
This package is only needed to boostrap compilation of GCC.

%prep
%setup -q -n %{pkgname}-%{version}

%build

%install

%if "%{buildtype}" == "cross"
prefix=%{_rpmint_prefix}
%else
prefix=%{_rpmint_target_prefix}
%endif
make -f Makefile.in DESTDIR=${RPM_BUILD_ROOT} prefix=${prefix} src_dir=. install-headers || {
	mkdir -p ${RPM_BUILD_ROOT}${prefix}/include/bits/m68k
	cp -a include/math.h include/fenv.h include/fpu_control.h ${RPM_BUILD_ROOT}${prefix}/include
	cp -a include/bits/fenv.h include/bits/fenvinline.h include/bits/huge_val.h include/bits/inf.h include/bits/math-68881.h include/bits/math-cffpu.h include/bits/mathcall.h include/bits/mathdef.h include/bits/nan.h include/bits/fpu_control.h ${RPM_BUILD_ROOT}${prefix}/include/bits
	cp -a include/bits/m68k/fenv.h include/bits/m68k/fpu_control.h ${RPM_BUILD_ROOT}${prefix}/include/bits/m68k
}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/*
%else
%{_rpmint_target_prefix}/include/*
%endif

%changelog
