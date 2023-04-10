%define pkgname ldg

%rpmint_header

Summary:        GEM Dynamic Libraries
Name:           %{crossmint}%{pkgname}
Version:        20171014
Release:        1
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++

Packager:       %{packager}p
URL:            http://ldg.sourceforge.net/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root


Source0: %{pkgname}-%{version}.tar.xz

Patch0: patches/ldg/ldg-cross.patch

%rpmint_essential
BuildRequires:  make
Provides:       %{crossmint}libldg-devel = %{version}

%rpmint_build_arch

%description
LDG stands for GEM Dynamic Libraries (actually Librairies Dynamiques
GEM in French). It&apos;s a system allowing GEM applications to load and to
share external modules. 

Only the libraries are compiled. To use modules, you also have to
install the auto folder programs from http://ldg.sourceforge.net/#download.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS="-W -Wall -O2 -fomit-frame-pointer -I../../include -I.. -I. $LTO_CFLAGS"


for CPU in ${ALL_CPUS}; do
	cd src/devel
	make -f gcc.mak clean >/dev/null

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	make -f gcc.mak CROSS_PREFIX=${TARGET}- CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	mkdir -p "%{buildroot}%{_rpmint_libdir}$multilibdir"

	cd ../..
	cp -a lib/gcc/libldg.a "%{buildroot}%{_rpmint_libdir}$multilibdir"

	mkdir -p "%{buildroot}%{_rpmint_includedir}"
	cp -a include/ldg.h "%{buildroot}%{_rpmint_includedir}"

	mkdir -p %{buildroot}%{_rpmint_mandir}/man1
	mkdir -p %{buildroot}%{_rpmint_mandir}/man3
	cp -a man/cat1/* %{buildroot}%{_rpmint_mandir}/man1
	cp -a man/cat3/* %{buildroot}%{_rpmint_mandir}/man3
	cp -a man/cat3l/* %{buildroot}%{_rpmint_mandir}/man3

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif
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
%license COPYRIGHT
%doc README* TODO
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*



%changelog
* Sat Apr 08 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 2.35

* Tue Aug 17 2010 Keith Scroggins <kws@radix.net>
- Added 68020-60 library and support for Coldfire, but some assembly needs to
- be patched for the Coldfire build.

* Wed Nov 02 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- Initial version of the ldg-dev package
