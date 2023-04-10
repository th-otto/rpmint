%define pkgname tiff

%rpmint_header

Summary:        Library for the Portable Network Graphics Format (PNG)
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        4.5.0
Release:        3
License:        HPND
Group:          Productivity/Graphics/Convertors

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://libtiff.gitlab.io/libtiff/

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://download.osgeo.org/libtiff/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/tiff-4.0.3-seek.patch
Patch1: patches/%{pkgname}/tiff-4.0.3-compress-warning.patch
Patch2: patches/%{pkgname}/tiff-disable-assertions.patch
Patch3: patches/%{pkgname}/tiff-CVE-2022-48281.patch
Patch4: patches/%{pkgname}/tiff-CVE-2023-0795.patch
Patch5: patches/%{pkgname}/tiff-CVE-2023-0800.patch

%rpmint_essential
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-zlib
BuildRequires:  cross-mint-zstd-devel
BuildRequires:  cross-mint-libjpeg-devel
%else
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  libjpeg-devel
%endif

%rpmint_build_arch

%description
This package contains the library and support programs for the TIFF
image format.

%package devel
Summary:        Development Tools for Programs which will use the libtiff Library
Group:          Development/Libraries/C and C++
%if "%{buildtype}" == "cross"
Provides      : cross-mint-lib%{pkgname}-devel = %{version}
%else
Provides      : lib%{pkgname}-devel = %{version}
%endif
Requires      : %{name} = %{version}

%description devel
This package contains the header files and static libraries for
developing programs which will manipulate TIFF format image files using
the libtiff library.



%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

cp %{S:1} config/config.sub

%build

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--datadir=%{_rpmint_target_prefix}/share
	--with-doc-dir=%{_rpmint_target_prefix}/share/doc/%{pkgname}
	--disable-nls
	--disable-shared
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
	%endif

	make clean
done


%install

%rpmint_cflags

%rpmint_strip_archives
%{_rpmint_target_strip} %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/bin/* || :

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
%{_isysroot}%{_rpmint_target_prefix}/bin/*

%files devel
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%{_isysroot}%{_rpmint_target_prefix}/share/*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}/*.pc
%endif


%changelog
* Tue Feb 28 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 4.5.0

* Sat Dec 23 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 3.5.5

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55
