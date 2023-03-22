%define pkgname mintlib

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Standard C Libraries for MiNT
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.60.1
Release:        3
License:        LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND GPL-2.0-or-later
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/freemint/mintlib
Source:         %{pkgname}-%{version}.tar.xz

Prefix:         %{_prefix}

%if "%{buildtype}" == "cross"
Provides:       cross-mint-%{pkgname}-headers = %{version}
%else
Provides:       %{pkgname}-headers = %{version}
%endif

BuildRequires:  cross-mint-gcc

%rpmint_build_arch

%description
This is the MiNTLib. The MiNTLib is the standard libc for FreeMiNT. It
will also work to some extent on non-MiNT systems, it tries its best to
emulate MiNT-calls on these systems.

On FreeMiNT systems the MiNTLib provides a programming interface that
is close to real *nix systems. It will either emulate system calls or
map them into GEMDOS- resp. FreeMiNT-calls.

These libraries are needed to develop programs which use the standard C
library.

%package -n timezone
Summary:        Time Zone Descriptions
License:        BSD-3-Clause
Group:          System/Base
# FIXME: needs rpm patch
# Version:        2018e

%description -n timezone
These are configuration files that describe available time zones. You
can select an appropriate time zone for your system running tzselect.


%prep
%setup -q -n %{pkgname}-%{version}

%build

%rpmint_cflags

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export CROSS_TOOL=%{_rpmint_target}

#
# ugly hack until makefiles have been ajusted
#
sed -i "\@^# This is where include@i prefix := ${RPM_BUILD_ROOT}%{_rpmint_prefix}" configvars

make %{?_smp_mflags}

%install

export CROSS_TOOL=%{_rpmint_target}

%if "%{buildtype}" == "cross"
prefix=%{_rpmint_prefix}
%else
prefix=%{_rpmint_target_prefix}
%endif
make prefix=${RPM_BUILD_ROOT}${prefix} install

%if "%{buildtype}" == "cross"
rm -rf ${RPM_BUILD_ROOT}${prefix}/sbin
rm -rf ${RPM_BUILD_ROOT}${prefix}/share/zoneinfo
rm -rf ${RPM_BUILD_ROOT}${prefix}/share/man
%else
%rpmint_gzip_docs
%endif

#
# The Makefile in the include directory
# installs these files to /usr/include, but they don't belonge there
#
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
%{_rpmint_libdir}
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/share/man
%{_rpmint_target_prefix}/lib
%endif

%if "%{buildtype}" != "cross"
%files -n timezone
# %config(missingok,noreplace) /etc/localtime
%{_rpmint_target_prefix}/share/zoneinfo
%{_rpmint_target_prefix}/sbin/*
%endif

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%changelog
* Sun Mar 5 2023 Thorsten Otto <admin@tho-otto.de>
- timezone update 2022g
- Install leapseconds data to %%{_datadir}/zoneinfo/; this is now
  required by some scientific applications.

* Mon Aug 31 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
