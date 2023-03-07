%define pkgname isl

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Integer Set Library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.18
Release:        1
License:        LGPL-3.0+
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://isl.gforge.inria.fr/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        http://isl.gforge.inria.fr/%{pkgname}-%{version}.tar.xz
Source1:        patches/automake/mintelf-config.sub

BuildRequires:  cross-mint-gcc-c++
BuildRequires:  cross-mint-gmp
%if "%{buildtype}" == "cross"
Requires:       cross-mint-gmp
%else
Requires:       gmp
%endif

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
ISL is a library for manipulating sets and relations of integer points
bounded by linear constraints.
It is used by Cloog and the GCC Graphite optimization framework.

%package doc
Summary:        Documentation files for ISL
Group:          System/Libraries
BuildArch:      noarch

%description doc
Documentation for ISL.

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
%{_rpmint_libdir}/pkgconfig/*.pc
%{_rpmint_cross_pkgconfigdir}/*.pc
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/lib/*.a
%{_rpmint_target_prefix}/lib/*/*.a
%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%endif


%changelog
* Thu Aug 27 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
