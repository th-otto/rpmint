%define pkgname fdlibm

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

Summary:        Freely Distributable C math library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
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

%if "%{buildtype}" == "cross"
Provides:       cross-mint-%{pkgname}-headers = %{version}
%else
Provides:       %{pkgname}-headers = %{version}
%endif

BuildRequires:  cross-mint-gcc

%rpmint_build_arch

%description
FDLIBM (Freely Distributable LIBM) is a C math library 
for machines that support IEEE 754 floating-point arithmetic. 

FDLIBM is intended to provide a reasonably portable (see 
assumptions below), reference quality (below one ulp for
major functions like sin,cos,exp,log) math library 
(libm.a)

%package devel
Summary:        Include Files and Libraries Mandatory for Development
Group:          Development/Libraries/C and C++
Requires:       fdlibm = %{version}

%description devel
These libraries are needed to develop programs which use the standard math
library.

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
