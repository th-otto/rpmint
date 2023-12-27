%define pkgname fdlibm

%rpmint_header

Summary:        Freely Distributable C math library
Name:           %{crossmint}%{pkgname}
Version:        20230210
Release:        1
License:        Public Domain
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/freemint/fdlibm
#URL:            https://www.netlib.org/fdlibm/

Prefix:         %{_prefix}
BuildRoot:      %{_tmppath}/%{name}-root

Source:         %{pkgname}-%{version}.tar.xz

Provides:       %{crossmint}%{pkgname}-headers = %{version}
Conflicts:      %{crossmint}pml

# cannot use rpmint_essential() here, because fdlibm is part of the essential package
BuildRequires:  %{crossmint}gcc

%rpmint_build_arch

%description
FDLIBM (Freely Distributable LIBM) is a C math library 
for machines that support IEEE 754 floating-point arithmetic. 

FDLIBM is intended to provide a reasonably portable (see 
assumptions below), reference quality (below one ulp for
major functions like sin,cos,exp,log) math library 
(libm.a)

%prep
%setup -q -n %{pkgname}-%{version}


%build

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

CFLAGS="$COMMON_CFLAGS" \
LDFLAGS="$COMMON_CFLAGS ${STACKSIZE}" \
"./configure" ${CONFIGURE_FLAGS}

make %{?_smp_mflags}

%install
%if "%{buildtype}" == "cross"
make DESTDIR=${RPM_BUILD_ROOT}%{_rpmint_sysroot} install
%else
make DESTDIR=${RPM_BUILD_ROOT} install
%endif

%rpmint_strip_archives

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/*
%{_rpmint_libdir}/*.a
%{_rpmint_libdir}/*/*.a
%{_rpmint_libdir}/*/*/*.a
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/lib/*.a
%{_rpmint_target_prefix}/lib/*/*.a
%{_rpmint_target_prefix}/lib/*/*/*.a
%endif


%changelog
* Mon Aug 31 2020 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri Jun 04 2010 Keith Scroggins <kws@radix.net>
- Added m5475 target

* Wed Sep 22 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to version 5.3

* Sun Jun 04 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- first release for Sparemint.
