%define pkgname fribidi

%rpmint_header

Summary:        An implementation of the Unicode BiDi algorithm
Name:           %{crossmint}%{pkgname}
Version:        1.0.13
Release:        1
License:        LGPL-2.1-only
Group:          Development/Libraries/C and C++

Packager:       %{packager}
URL:            https://github.com/fribidi/fribidi

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://github.com/fribidi/fribidi/releases/download/v%{version}/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  pkgconfig
BuildRequires:  make
Provides:       %{crossmint}lib%{pkgname}-devel = %{version}

%rpmint_build_arch

%description
This library implements the algorithm as described in "Unicode
Standard Annex #9, the Bidirectional Algorithm,
http://www.unicode.org/unicode/reports/tr9/". FriBidi is
tested against the Bidi Reference Code and, to the best of the
developers' knowledge, does not contain any conformance bugs.

The API was inspired by the document "Bi-Di languages support - BiDi
API proposal" by Franck Portaneri, which he wrote as a proposal for
adding BiDi support to Mozilla.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

autoreconf -fiv
cp %{S:1} config.sub

%build

%rpmint_cflags
COMMON_CFLAGS+=" -fno-strict-aliasing"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-static
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
%license COPYING
%doc NEWS README
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/bin
%{_isysroot}%{_rpmint_target_prefix}/share/man
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Mon Nov 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
