%define pkgname unzip

%rpmint_header

Summary:        A program to unpack compressed files
Name:           %{crossmint}%{pkgname}
Version:        6.0
Release:        1
License:        BSD-3-Clause
Group:          Productivity/Archiving/Compression

URL:            http://www.info-zip.org/UnZip.html
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        ftp://ftp.info-zip.org/pub/infozip/src/unzip60.tgz

Patch0: patches/%{pkgname}/unzip-config.dif
Patch1: patches/%{pkgname}/unzip-iso8859_2.patch
Patch2: patches/%{pkgname}/unzip-optflags.patch
Patch3: patches/%{pkgname}/unzip-5.52-filename_too_long.patch
Patch4: patches/%{pkgname}/unzip-no_file_name_translation.patch
Patch5: patches/%{pkgname}/unzip-open_missing_mode.patch
Patch6: patches/%{pkgname}/unzip-no-build-date.patch
Patch7: patches/%{pkgname}/unzip-dont_call_isprint.patch
Patch8: patches/%{pkgname}/unzip-Fix-CVE-2014-8139-unzip.patch
Patch9: patches/%{pkgname}/unzip-Fix-CVE-2014-8140-and-CVE-2014-8141.patch
Patch10: patches/%{pkgname}/unzip-CVE-2015-7696.patch
Patch11: patches/%{pkgname}/unzip-CVE-2015-7697.patch
Patch12: patches/%{pkgname}/unzip-CVE-2016-9844.patch
Patch13: patches/%{pkgname}/unzip-CVE-2014-9913.patch
Patch14: patches/%{pkgname}/unzip-CVE-2018-1000035.patch
Patch15: patches/%{pkgname}/unzip-atari-chmod-0.patch
Patch16: patches/%{pkgname}/unzip-symlinks.patch
Patch17: patches/%{pkgname}/unzip-no-macosx.patch


%rpmint_essential
BuildRequires:  make

%rpmint_build_arch

%description
UnZip is an extraction utility for archives compressed in .zip format
(known as &quot;zip files&quot;).  Although highly compatible both with PKWARE&apos;s
PKZIP(tm) and PKUNZIP utilities for MS-DOS and with Info-ZIP&apos;s own Zip
program, our primary objectives have been portability and non-MS-DOS
functionality. This version can also extract encrypted archives.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n unzip60
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS="-O3 -fomit-frame-pointer \
-D_GNU_SOURCE -DRCC_LAZY -DWILD_STOP_AT_DIR \
-DUNICODE_WCHAR -DNO_LCHMOD \
-DDATE_FORMAT=DF_YMD -I. -fno-strict-aliasing \
-DUSE_BZIP2 \
"
STACKSIZE=-Wl,-stack,96k

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
		CC="${TARGET}-gcc" \
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		LD="${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
		unix_make
	make -f unix/Makefile \
		prefix=%{_rpmint_target_prefix} \
		CC="${TARGET}-gcc" \
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		LD="${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
		L_BZ2=-lbz2 \
		unzips
	make -f unix/Makefile \
		prefix="%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}" \
		MANDIR='${prefix}/share/man1' \
		INSTALL=install \
		INSTALL_D="install -d" \
		install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	(cd "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin"; rm -f zipinfo; $LN_S unzip zipinfo)

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
%doc BUGS README History.600 WHERE
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share


%changelog
* Mon Apr 03 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 6.0

* Tue Feb 18 2003 Jan Krupka <jkrupka@volny.cz>
- update to 5.50
- added %%description cs and Summary(cs)

* Thu Mar 23 2000 Frank Naumann <fnaumann@freemint.de>
- update to 5.40

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
- added %%description de and Summary(de)
