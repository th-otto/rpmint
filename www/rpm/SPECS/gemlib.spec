%rpmint_header

%define gcc_version %(%{_rpmint_target}-gcc -dumpversion)
%define gcc_major_version %(%{_rpmint_target}-gcc -dumpversion | cut -d . -f 1)

%if %{gcc_major_version} == 2
%define pkgname gemlib-gcc2
%else
%define pkgname gemlib
%endif

Summary:        GEM libraries and header files
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.44.0
Release:        20230212
License:        Public Domain
Group:          System/Libraries

Packager:       %{packager}
URL:            https://github.com/freemint/gemlib
#URL:           http://arnaud.bercegeay.free.fr/gemlib/

Prefix:         %{_prefix}
BuildRoot:      %{_tmppath}/%{name}-root

Source:         gemlib-%{version}.tar.xz

%if "%{buildtype}" == "cross"
Provides:       cross-mint-%{pkgname}-headers = %{version}
%else
Provides:       %{pkgname}-headers = %{version}
%endif

# cannot use rpmint_essential() here, because gemlib is part of the essential package
BuildRequires:  cross-mint-gcc

%rpmint_build_arch

%description
Contains the standard libraries and header files to develop your own GEM
applications.

Attention, starting from version 0.40.0 the gemlib is heavily modernized
and updated. There are incompatible changes that require modifications
of programs that use this lib too.

Package version numbering has been modified to the one used by the
library itself. Please use the --oldpackage option if upgrading from a
0.40.0 or older gemlib and rpm complains about installed package being
newer than this one.

%prep
%setup -q -n gemlib-%{version}

%if %{gcc_major_version} == 2
sed -i 's@PREFIX=$(shell $(CROSSPREFIX)gcc -print-sysroot)/usr@PREFIX=/usr@' CONFIGVARS
sed -i 's@-Wdeclaration-after-statement@@' CONFIGVARS
sed -i 's@-mcpu=5475@-m5200@' Makefile.objs
%endif

%build

%rpmint_cflags

if test "$LTO_CFLAGS" != ""; then
	sed -i "\@^DEFINITIONS =@i OPTS += $LTO_CFLAGS" CONFIGVARS
fi

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export CROSS_TOOL=${TARGET}

# this Makefiles are not yet ready for parallel makes
make -j1

%install

export CROSS_TOOL=${TARGET}

%if %{gcc_major_version} == 2
make PREFIX=${RPM_BUILD_ROOT}%{_rpmint_target_prefix} install
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
%if "%{buildtype}" == "cross"
make PREFIX=${RPM_BUILD_ROOT}%{_rpmint_prefix} install || exit 1
%else
make PREFIX=${RPM_BUILD_ROOT}%{_rpmint_target_prefix} install
%endif
%endif

%rpmint_strip_archives

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


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


%changelog
* Sat Aug 29 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file

* Sun Jan 17 2016 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated to version 0.44.0

* Mon Dec 19 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated to version 0.43.6

* Mon Oct  3 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated to version 0.43.5

* Fri Apr  1 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated to version 0.43.4

* Wed Nov  3 2004 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated to version 0.43.3

* Mon Jan  5 2004 Standa Opichal <opichals@seznam.cz>
- updated to version 0.43.1

* Tue Oct 21 2003 Standa Opichal <opichals@seznam.cz>
- version 0.43.0 - new generation gemlib

* Sun Feb 16 2003 Standa Opichal <opichals@seznam.cz>
- updated to version 0.42.99, betaversion of new generation gemlib

* Mon Jul 15 2002 Xavier Joubert <xavier.joubert@free.fr>
- updated to version 0.42.2, modified version numbering

* Tue Feb 27 2001 Frank Naumann <fnaumann@freemint.de>
- updated to version 0.40.0

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 11 1999 Guido Flohr <guido@freemint.de>
- Changed vendor to Sparemint
