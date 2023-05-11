%define pkgname mpc

%rpmint_header

Summary:        MPC multiple-precision complex shared library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.1.0
Release:        1
License:        LGPL-3.0+
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.multiprecision.org/mpc/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.gz
Source1:        patches/automake/mintelf-config.sub

BuildRequires:  cross-mint-gcc-c++
BuildRequires:  cross-mint-gmp
BuildRequires:  cross-mint-mpfr
%if "%{buildtype}" == "cross"
Requires:       cross-mint-gmp
Requires:       cross-mint-mpfr
%else
Requires:       gmp
Requires:       mpfr
%endif

%rpmint_build_arch

%description
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as MPFR.

%package doc
Summary:        Documentation files for MPC multiple-precision complex shared library
Group:          System/Libraries
BuildArch:      noarch

%description doc
Documentation for MPC multiple-precision complex shared library.

%prep
%setup -q -n %{pkgname}-%{version}
rm -f config.sub
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
%else
%doc %{_rpmint_target_prefix}/share/info
%endif

%post doc
%rpmint_install_info %{pkgname}

%preun doc
%rpmint_uninstall_info %{pkgname}


%changelog
* Thu Aug 27 2020 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri May 28 2010 Keith Scroggins <kws@radix.net>
- Initial build of MPC RPM
