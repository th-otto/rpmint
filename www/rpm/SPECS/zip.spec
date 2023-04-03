%define pkgname zip

%rpmint_header

Summary:        File compression program
Name:           %{crossmint}%{pkgname}
Version:        3.0
Release:        1
License:        BSD-3-Clause
Group:          Productivity/Archiving/Compression

URL:            http://www.info-zip.org/Zip.html
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        ftp://ftp.info-zip.org/pub/infozip/src/zip30.tgz

Patch0: patches/zip/zip-3.0-iso8859_2.patch
Patch1: patches/zip/zip-3.0-add_options_to_help.patch
Patch2: patches/zip/zip-3.0-nonexec-stack.patch
Patch3: patches/zip/zip-3.0-optflags.patch
Patch4: patches/zip/zip-3.0-tempfile.patch
Patch5: patches/zip/zip-3.0-nomutilation.patch
Patch6: patches/zip/zip-3.0-atari.patch
Patch7: patches/zip/zip-3.0-no-setbuf.patch


%rpmint_essential
BuildRequires:  make

%rpmint_build_arch

%description
Zip is a compression and file packaging utility. It is compatible with
PKZIP(tm) 2.04g (Phil Katz ZIP) for MS-DOS systems.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n zip30
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS="-O3 -fomit-frame-pointer $LTO_CFLAGS"
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

	make -f unix/Makefile \
		prefix=%{_rpmint_target_prefix} \
		CC="${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
		generic
	make -f unix/Makefile \
		prefix="%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}" \
		BINDIR='${prefix}/bin' \
		MANDIR='${prefix}/share/man1' \
		install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	make -f unix/Makefile clean
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%doc README README.CR CHANGES TODO WHATSNEW WHERE BUGS proginfo/algorith.txt
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share


%changelog
* Mon Apr 03 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 3.0

* Thu Mar 23 2000 Frank Naumann <fnaumann@freemint.de>
- update to 2.3

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
- added %description de and Summary(de)
