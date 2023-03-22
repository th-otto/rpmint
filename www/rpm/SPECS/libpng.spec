%define pkgname libpng

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Library for the Portable Network Graphics Format (PNG)
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.6.39
Release:        1
License:        Zlib
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.libpng.org/pub/png/libpng.html

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp-osl.osuosl.org/pub/%{pkgname}/src/libpng16/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/libpng-1.6.34-0001-config.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-zlib
Provides:       cross-mint-libpng-devel = %{version}
%else
BuildRequires:  pkgconfig(zlib)
Provides:       libpng = %{version}
Provides:       libpng-devel = %{version}
%endif

%rpmint_build_arch

%description
libpng is the official reference library for the Portable Network
Graphics format (PNG).

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

cp %{S:1} config.sub

sed -i 's/^option CONSOLE_IO.*/\0 disabled/' scripts/pnglibconf.dfa

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname}
    --disable-shared
    --config-cache
    --without-binconfigs
"

create_config_cache()
{
cat <<EOF >config.cache
EOF
}

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	create_config_cache

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
	rm -f %{buildroot}%{_rpmint_bindir}/libpng*-config

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
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}
%{_rpmint_datadir}
%else
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%endif



%changelog
* Tue Feb 28 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
