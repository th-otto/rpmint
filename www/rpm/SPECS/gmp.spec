%define pkgname gmp

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        The GNU MP Library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        6.2.1
Release:        1
License:        GPL-3.0+ and LGPL-3.0+
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://gmplib.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://gmplib.org/download/%{pkgname}/%{pkgname}-%{version}.tar.xz
Patch0: gmp-coldfire.patch
Patch1: gmp-mintelf-config.patch

%rpmint_essential
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-gcc-c++
%else
BuildRequires:  gcc-c++
%endif
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  xz

%if "%{buildtype}" == "cross"
BuildArch:      noarch
%else
%define _target_platform %{_rpmint_target_platform}
%if "%{buildtype}" == "v4e"
%define _arch m5475
%else
%if "%{buildtype}" == "020"
%define _arch m68020
%else
%define _arch m68k
%endif
%endif
%endif

%description
A library for calculating huge numbers (integer and floating point).

%package devel
Summary:        Include Files and Libraries for Development with the GNU MP Library
Group:          Development/Libraries/C and C++
Requires:       %{pkgname} = %{version}

%description devel
These libraries are needed to develop programs which calculate with
huge numbers (integer and floating point).

%package doc
Summary:        Documentation files for GNU MP Library
Group:          System/Libraries
BuildArch:      noarch

%description doc
Documentation for GNU MP Library

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

rm -f aclocal.m4 ltmain.sh
libtoolize --force
aclocal
autoconf
autoheader
automake --force --copy --add-missing
%patch1 -p1

%build

%rpmint_cflags

COMMON_CFLAGS="-O3 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS} --enable-cxx --enable-fat"
STACKSIZE="-Wl,-stack,256k"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	# disable assembly for ColdFire for now; does not work yet
	assembly=
	if test $CPU = v4e; then
		assembly="--disable-assembly --disable-fat"
	fi
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} $assembly \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make clean
done


%install

%rpmint_cflags

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/*
%{_rpmint_libdir}/*.a
%{_rpmint_libdir}/*/*.a
%{_rpmint_cross_pkgconfigdir}
%{_rpmint_libdir}/pkgconfig
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/lib/*.a
%{_rpmint_target_prefix}/lib/*/*.a
%{_rpmint_target_prefix}/lib/pkgconfig
%endif

%files doc
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%doc %{_rpmint_infodir}
%else
%doc %{_rpmint_target_prefix}/share/info
%endif

%post doc
%rpmint_install_info %{pkgname}

%preun doc
%rpmint_uninstall_info %{pkgname}



%changelog
* Tue Feb 28 2023 Thorsten Otto <admin@tho-otto.de>
- Update to version 6.2.1

* Thu Aug 27 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
