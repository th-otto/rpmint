%define pkgname slang

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        The library and header files for the S-Lang extension language
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.4.9
Release:        2
License:        PGL
Group:          System Environment/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.s-lang.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make
%if "%{buildtype}" == "cross"
Provides:       cross-mint-slang-devel
%else
Provides:       slang-devel
%endif

%rpmint_build_arch

%description
S-Lang is an interpreted language and a programming library. The S-Lang
language was designed so that it can be easily embedded into a program to
provide the program with a powerful extension language. The S-Lang library,
provided in this package, provides the S-Lang extension language.  S-Lang's
syntax resembles C, which makes it easy to recode S-Lang procedures in C if
you need to.

%prep
%setup -q -n %{pkgname}-%{version}


cp %{S:1} autoconf/config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
"

export CC="%{_rpmint_target}-gcc"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir \
	--includedir='${prefix}/include/slang'

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# Remove documentation files.
	rm -rf %{buildroot}%{_rpmint_sysroot}/usr/doc

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

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
%else
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%endif



%changelog
* Sun Mar 19 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Tue Nov 04 2003 Keith Scroggins <kws@radix.net>
- Initial build of Slang for FreeMiNT
