%define pkgname arc

%rpmint_header

Summary:        Archiving tool for arc achives
Name:           %{crossmint}%{pkgname}
Version:        5.21p
Release:        1
License:        GPL-2.0
Group:          Productivity/Archiving/Compression

URL:            http://arc.sourceforge.net/
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        %{pkgname}-%{version}.tar.gz

Patch0: patches/arc/arc-time.patch


%rpmint_essential
BuildRequires:  make

%rpmint_build_arch

%description
ARC is used to create and maintain file archives. An archive is a group
of files collected together into one file in such a way that the
individual files may be recovered intact.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%patch0 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS+=" -s -Wall"
STACKSIZE=-Wl,-stack,256k

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 000
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	sed -i "s:^PREFIX = .*:PREFIX = %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}:
s:^SYSTEM = .*:SYSTEM = -DBSD=1:
s:^OPT = .*:OPT = ${COMMON_CFLAGS} ${CPU_CFLAGS}:
s:^CC = .*:CC = ${TARGET}-gcc:
s:install -s:install:g" Makefile

	make %{?_smp_mflags}
	make install
	make clean

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license COPYING LICENSE
%doc Arc521.doc Changelog Arcinfo Readme
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share


%changelog
* Mon Apr 03 2023 Thorsten Otto <admin@tho-otto.de>
- Reqritten as RPMint spec file
- Update to 5.21p

* Mon Jun 21 2004 Jan Krupka <jkrupka@volny.cz>
- Initial package.
