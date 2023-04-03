%rpmint_header

%define gcc_version %(%{_rpmint_target}-gcc -dumpversion)
%define gcc_major_version %(%{_rpmint_target}-gcc -dumpversion | cut -d . -f 1)

%if %{gcc_major_version} == 2
%define pkgname pml-gcc2
%else
%define pkgname pml
%endif

Summary:        Portable Math-Lib for C programs 
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        2.03
Release:        5
License:        Public Domain
Group:          Development/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/freemint/pml

Source:         pml-%{version}.tar.xz
Patch1:         patches/%{pkgname}/pml-2.03-mint-20171006.patch
Patch2:         patches/%{pkgname}/pml-gcc2.patch

Prefix:         %{_prefix}

%if "%{buildtype}" == "cross"
Provides:       cross-mint-%{pkgname}-headers = %{version}
Conflicts:      cross-mint-fdlibm
%else
Provides:       %{pkgname}-headers = %{version}
Conflicts:      fdlibm
%endif

BuildRequires:  cross-mint-gcc

%rpmint_build_arch

%description
These are the header files and static libraries from the Mathlib
distribution.

If you want to develop software for MiNT or you want to use C++
you have to install this package.

Note: this package is obsolete. Use fdlibm instead.

%prep
%setup -q -n pml-%{version}

# Patch1 (the MiNT patch) is already applied in archive
%if %{gcc_major_version} == 2
%patch2 -p1
%endif

%build
cd pmlsrc

%rpmint_cflags

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export CROSS_TOOL=%{_rpmint_target}

make %{?_smp_mflags}

%install

export CROSS_TOOL=%{_rpmint_target}

make DESTDIR=${RPM_BUILD_ROOT} install

%if %{gcc_major_version} == 2
mkdir -p ${RPM_BUILD_ROOT}%{_rpmint_target_prefix}/%{_rpmint_target}/sys-include
mv ${RPM_BUILD_ROOT}%{_rpmint_target_prefix}/include/* ${RPM_BUILD_ROOT}%{_rpmint_target_prefix}/%{_rpmint_target}/sys-include
rmdir ${RPM_BUILD_ROOT}%{_rpmint_target_prefix}/include
%define gccsubdir %{_rpmint_target_prefix}/lib/gcc-lib/%{_rpmint_target}/%{gcc_version}
mv ${RPM_BUILD_ROOT}%{_rpmint_target_prefix} ${RPM_BUILD_ROOT}/uu
mkdir -p ${RPM_BUILD_ROOT}%{gccsubdir}
mv ${RPM_BUILD_ROOT}/uu/lib/* ${RPM_BUILD_ROOT}%{gccsubdir}
mv ${RPM_BUILD_ROOT}/uu/%{_rpmint_target} ${RPM_BUILD_ROOT}%{_rpmint_target_prefix}/
rmdir ${RPM_BUILD_ROOT}/uu/lib
rmdir ${RPM_BUILD_ROOT}/uu
%else
sysroot=`%{_rpmint_target}-gcc -print-sysroot`
mv ${RPM_BUILD_ROOT}${sysroot}%{_rpmint_target_prefix}/* ${RPM_BUILD_ROOT}%{_rpmint_target_prefix}
rmdir ${RPM_BUILD_ROOT}${sysroot}%{_rpmint_target_prefix} || :
rmdir ${RPM_BUILD_ROOT}${sysroot} || :
rmdir ${RPM_BUILD_ROOT}%{_rpmint_target_prefix}/%{_rpmint_target} || :
%endif

%files
%defattr(-,root,root)
%if %{gcc_major_version} == 2
%{_rpmint_target_prefix}/%{_rpmint_target}/sys-include
%{gccsubdir}
%else
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/*
%{_rpmint_libdir}
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/lib
%endif
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%changelog
* Mon Mar 13 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Tue Jun 01 2010 Keith Scroggins <kws@radix.net>
- Rebuild of PML to include math.h and also Coldfire support.  mshort 
- support has also been removed as noted from previous release.

* Sat Apr 01 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55
- splitted of mshort libs
- added m68020-60 target libs
- renamed all libs to the required libm names
- enhanced description, added description -l de

* Mon Oct 25 1999 Marc-Anton Kehr <m.kehr@ndh.net>
- first release for Sparemint
