%define pkgname tree

%rpmint_header

Summary:        File listing as a tree
Name:           %{crossmint}%{pkgname}
Version:        1.8.0
Release:        1
License:        GPL-2.0-or-later
Group:          Productivity/File utilities

URL:            http://mama.indstate.edu/users/ice/tree/
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        http://mama.indstate.edu/users/ice/tree/src/%{pkgname}-%{version}.tgz
Source1:        patches/automake/mintelf-config.sub

Patch0:         patches/%{pkgname}/tree-makefile.patch
Patch1:         patches/%{pkgname}/tree-mint.patch


%rpmint_essential
BuildRequires:  make

%rpmint_build_arch

%description
Tree is a recursive directory listing command that produces a depth
indented listing of files, which is colorized ala dircolors if the
LS_COLORS environment variable is set and output is to tty.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

STACKSIZE="-Wl,-stack,128k"

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

	make \
		CC=${TARGET}-gcc \
		CPU_CFLAGS="${CPU_CFLAGS}"
	make \
		prefix="%{buildroot}%{_rpmint_sysroot}/%{_rpmint_target_prefix}" \
		MANDIR='${prefix}/share/man/man1' \
		install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	make clean
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%rpmint_install_info %{pkgname}

%preun
%rpmint_uninstall_info %{pkgname}

%files
%defattr(-,root,root)
%license LICENSE
%doc README CHANGES
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share


%changelog
* Mon Apr 03 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 1.8.0

* Wed Sep 01 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpage

* Sat Aug 28 1999 Edgar Aichinger <eaiching@t0.or.at>
- added german translations, Packager, Vendor, Requires to spec-file
- #include <limits.h> instead of <linux/limits.h>
- added pseudo opcode for S_IFSOCK to make compile

