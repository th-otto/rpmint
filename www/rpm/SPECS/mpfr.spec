%define pkgname mpfr

%rpmint_header

Summary:        The GNU multiple-precision floating-point library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        3.1.4
Release:        1
License:        LGPL-3.0+
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.mpfr.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        http://www.mpfr.org/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.xz
Source1:        patches/automake/mintelf-config.sub

BuildRequires:  cross-mint-gcc-c++
BuildRequires:  cross-mint-gmp
%if "%{buildtype}" == "cross"
Requires:       cross-mint-gmp
%else
Requires:       gmp
%endif

%rpmint_build_arch

%description
The MPFR library is a C library for multiple-precision floating-point
computations with exact rounding (also called correct rounding). It is
based on the GMP multiple-precision library.

%package doc
Summary:        Documentation files for multiple-precision floating-point library
Group:          System/Libraries
BuildArch:      noarch

%description doc
Documentation for multiple-precision floating-point library.

%prep
%setup -q -n %{pkgname}-%{version}
cp %{S:1} config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O3 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}"
STACKSIZE="-Wl,-stack,256k"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
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

# already done in loop above
# make install DESTDIR=%{buildroot}%{_rpmint_sysroot}

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
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/lib/*.a
%{_rpmint_target_prefix}/lib/*/*.a
%endif

%files doc
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%doc %{_rpmint_infodir}
%{_rpmint_docdir}/%{pkgname}
%else
%doc %{_rpmint_target_prefix}/share/info
%{_rpmint_target_prefix}/share/doc/%{pkgname}
%endif

%post doc
%rpmint_install_info %{pkgname}

%preun doc
%rpmint_uninstall_info %{pkgname}


%changelog
* Thu Aug 27 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file

* Thu May 27 2010 Keith Scroggins <kws@radix.net>
- Initial build of MPFR RPM with the latest patch from the developers for
- the 68000 target.
- Currently 3 tests fail out of 148.  
- tset_ld seems to just hang, it ran for 4 hours without returning results.
- tcmp_ld returns ERROR for NAN (1)
- tsprintf gets the following reasults (but the test might not be correct)
- Error in mpfr_sprintf (s, "%'Rf", x);
- expected: "100000000000000000.000000"
- got:      "100,000,000,000,000,000.000000"
