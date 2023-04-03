%define pkgname gemma

%rpmint_header

Summary:        Support library for GEM application programs
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        20230303
Release:        1
License:        GPL-2.0-or-later
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/freemint/gemma

Prefix:         %{_prefix}
BuildRoot:      %{_tmppath}/%{name}-root

Source:         %{pkgname}-%{version}.tar.xz

%if "%{buildtype}" == "cross"
Provides:       cross-mint-%{pkgname}-headers = %{version}
%else
Provides:       %{pkgname}-headers = %{version}
%endif

# cannot use rpmint_essential() here, because fdlibm is part of the essential package
BuildRequires:  cross-mint-gcc

%rpmint_build_arch

%description
Gemma is a support library for GEM application programs.

%prep
%setup -q -n %{pkgname}-git

if test "$LTO_CFLAGS" != ""; then
	sed -i "\@^DEFINITIONS =@i OPTS += $LTO_CFLAGS" CONFIGVARS
fi
sed -i "\@^DEFINITIONS =@i PREFIX := %{buildroot}%{_rpmint_prefix}" CONFIGVARS

%build

%rpmint_cflags

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export CROSS_TOOL=%{_rpmint_target}
make

%install
%if "%{buildtype}" == "cross"
make PREFIX=${RPM_BUILD_ROOT}%{_rpmint_prefix} install
cd ${RPM_BUILD_ROOT}%{_rpmint_prefix}/../mint/slb && mkdir m68000 && mv gemma32.slb kernel32.slb m68000
%else
make PREFIX=${RPM_BUILD_ROOT}%{_rpmint_target_prefix} install
cd ${RPM_BUILD_ROOT}%{_rpmint_target_prefix}/../mint/slb && mkdir m68000 && mv gemma32.slb kernel32.slb m68000
%endif

%rpmint_strip_archives

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_sysroot}/mint/slb
%else
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
/mint/slb
%endif


%changelog
