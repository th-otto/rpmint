%define pkgname libmetalink

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Metalink library written in C
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.1.3
Release:        1
License:        MIT
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://launchpad.net/libmetalink

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://github.com/metalink-dev/%{pkgname}/releases/download/release-%{version}/libmetalink-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Patch0: libmetalink-autotools.patch
Patch1: libmetalink-skip-libxml2-script-crap.patch

BuildRequires:  cross-mint-gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(pkg-config)
BuildRequires:  m4
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-zlib
BuildRequires:  cross-mint-libiconv
BuildRequires:  cross-mint-libxml2
BuildRequires:  cross-mint-liblzma5
%else
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  libiconv
%endif

%rpmint_build_arch

%description
Libmetalink is a Metalink library written in C language. It is intended to
provide the programs written in C to add Metalink functionality such as parsing
Metalink XML files.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

cp %{S:1} config.sub


sed -i -e 's@AM_CONFIG_HEADER@AC_CONFIG_HEADERS@g' configure.ac
rm -f m4/libtool.m4 m4/lt*
rm -f aclocal.m4 ltmain.sh
libtoolize --force
aclocal -I m4
autoconf
autoheader
automake --force --copy --add-missing
# autoreconf may have overwritten config.sub
#%patch2 -p1

%build

%rpmint_cflags

export LIBXML2_CFLAGS=-I%{_rpmint_includedir}/libxml2
export LIBXML2_LIBS="-lxml2 -lz -llzma -liconv -lm"

COMMON_CFLAGS="-O3 -fomit-frame-pointer $LIBXML2_CFLAGS"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} --docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname}
${CONFIGURE_FLAGS_AMIGAOS}
--without-libexpat
--disable-shared
--enable-static
--config-cache
"

create_config_cache()
{
cat <<EOF >config.cache
EOF
	%rpmint_append_gnulib_cache
}


[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${LIBXML2_LIBS}" \
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
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}
%{_rpmint_mandir}
%else
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share/man
%endif



%changelog
* Wed Mar 1 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
