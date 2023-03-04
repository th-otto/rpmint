%define pkgname libidn2

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Support for Internationalized Domain Names (IDN) based on IDNA2008
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        2.0.4
Release:        1
License:        MIT
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://www.gnu.org/software/libidn/#libidn2

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: ftp://ftp.gnu.org/gnu/libidn/%{pkgname}-%{version}.tar.lz
Patch1: patches/%{pkgname}/libidn2-mintelf-config.patch

%rpmint_essential
BuildRequires:  pkgconfig
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-libiconv
%else
BuildRequires:  libiconv
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
Libidn2 is an implementation of the IDNA2008 + TR46 specifications (RFC
5890, RFC 5891, RFC 5892, RFC 5893, TR 46). Libidn2 is a standalone
library, without any dependency on Libidn. Libidn2 is believed to be a
complete IDNA2008 / TR46 implementation, but has yet to be as
extensively used as the original Libidn library.

%prep
%setup -q -n %{pkgname}-%{version}
%patch1 -p1

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname}
    --disable-shared
    --enable-static
    --disable-doc
    --disable-gtk-doc
"

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
%if "%{buildtype}" == "cross"
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}
%else
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%endif



%changelog
* Fri Mar 03 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
