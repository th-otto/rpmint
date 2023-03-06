%define pkgname nghttp2

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Implementation of Hypertext Transfer Protocol version 2 in C
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.26.0
Release:        1
License:        MIT
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://nghttp2.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/nghttp2-remove-python-build.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-zlib
BuildRequires:  cross-mint-libiconv
BuildRequires:  cross-mint-openssl
BuildRequires:  cross-mint-libxml2
%else
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libxml-2.0)
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
nghttp2 is an implementation of HTTP/2 and its header compression algorithm HPACK in C.

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

# autoreconf may have overwritten config.sub
cp %{S:1} config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname}
    --disable-shared
    --enable-static
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
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}
%{_rpmint_datadir}
%else
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%endif



%changelog
* Mon Mar 6 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
