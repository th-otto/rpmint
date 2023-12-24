%define pkgname libxmp

%rpmint_header

Summary:        Module Player library for MOD, S3M, IT and others
Name:           %{crossmint}%{pkgname}
Version:        4.6.0
Release:        1
License:        LGPL-2.1
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://xmp.sourceforge.net/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/%{pkgname}/libxmp.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make
Provides:       %{crossmint}libxmp-devel

%rpmint_build_arch

%description
Libxmp is a library that renders module files to PCM data. It supports
over 90 mainstream and obscure module formats including Protracker (MOD),
Scream Tracker 3 (S3M), Fast Tracker II (XM), and Impulse Tracker (IT).

Many compressed module formats are supported, including popular Unix, DOS,
and Amiga file packers including gzip, bzip2, SQSH, Powerpack, etc.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
"

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

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

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
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Fri Dec 22 2023 Thorsten Otto <admin@tho-otto.de>
- Update to version 4.6.0

* Sat Apr 01 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
