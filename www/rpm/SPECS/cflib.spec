%define pkgname cflib

%rpmint_header

Summary:        CFLIB is Christian Felsch's GEM utility library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        21
Release:        20181123
License:        LGPL-2.1-or-later
Group:          System/Libraries

Packager:       %{packager}
URL:            https://github.com/freemint/cflib

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source:         %{pkgname}-%{version}.tar.xz

%if "%{buildtype}" == "cross"
Provides:       cross-mint-%{pkgname}-headers = %{version}
%else
Provides:       %{pkgname}-headers = %{version}
%endif

BuildRequires:  cross-mint-gcc

%rpmint_build_arch

%description
CFLIB is Christian Felsch's GEM utility library. It provide advanced controls,
such as check boxes, radio buttons, combo boxes... It also allows windowed
dialogs.
BUG: On plain TOS, CFLIB makes intensive use of the GEM USERDEF feature.
Due to bad GEM design, USERDEF callbacks are called in supervisor mode using
the very small internal AES stack. Unfortunately, some GemLib functions such
as v_gtext() needs an insane amout of stack (more than 2 KB). So some USERDEF
callbacks quickly produces an AES internal stack overflow, and crash the entire
system.
Concretely, due to this issue, programs using CFLIB work fine on XaAES
and TOS 4.04, but crash on TOS 1.62 and early versions of EmuTOS.

%prep
%setup -q -n %{pkgname}-%{version}

%build

%rpmint_cflags

if test "$LTO_CFLAGS" != ""; then
	sed -i "\@^DEFINITIONS =@i OPTS += $LTO_CFLAGS" CONFIGVARS
fi

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export CROSS_TOOL=${TARGET}

make %{?_smp_mflags}

%install
%if "%{buildtype}" == "cross"
install_prefix=${RPM_BUILD_ROOT}%{_rpmint_prefix}
%else
install_prefix=${RPM_BUILD_ROOT}%{_rpmint_target_prefix}
%endif

mkdir -p ${install_prefix}/include
mkdir -p ${install_prefix}/lib
mkdir -p ${install_prefix}/lib/mshort
mkdir -p ${install_prefix}/lib/m68020-60
mkdir -p ${install_prefix}/lib/m68020-60/mshort
mkdir -p ${install_prefix}/lib/m5475
mkdir -p ${install_prefix}/lib/m5475/mshort
mkdir -p ${install_prefix}/stguide
make PREFIX=${install_prefix} install

%rpmint_strip_archives

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/*
%{_rpmint_libdir}
%{_rpmint_prefix}/stguide
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/stguide
%endif


%changelog
* Wed Sep 2 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
