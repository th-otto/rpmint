%define pkgname libssh2

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        A library implementing the SSH2 protocol
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.8.0
Release:        1
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.libssh2.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://www.libssh2.org/download/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/libssh2-zlib-static.patch

%rpmint_essential
BuildRequires:  pkgconfig
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-openssl
%else
BuildRequires:  pkgconfig(openssl)
Provides:       pkgconfig(libssh2) = %{version}
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
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS, SECSH-USERAUTH, SECSH-CONNECTION,
SECSH-ARCH, SECSH-FILEXFER, SECSH-DHGEX, SECSH-NUMBERS, and
SECSH-PUBLICKEY.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

sed -i -e 's@AM_CONFIG_HEADER@AC_CONFIG_HEADERS@g' configure.ac
rm -v m4/libtool.m4 m4/lt*
rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub

%build

%rpmint_cflags

CONFIGURE_FLAGS="--host=%{_rpmint_target} --prefix=%{_rpmint_target_prefix} --docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-rpath
	--disable-examples-build
	--disable-shared
	--enable-static
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

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

	make distclean
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
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}/*.pc
%{_rpmint_datadir}
%else
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%endif




%changelog
* Sun Mar 5 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
