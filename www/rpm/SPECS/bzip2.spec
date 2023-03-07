%define pkgname bzip2

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        A file compression utility
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.0.8
Release:        1
License:        BSD
Group:          Productivity/Archiving/Compression

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.bzip.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/bzip2-1.0.6-patch-0001-configure.patch
Patch1: patches/%{pkgname}/bzip2-1.0.8-patch-0002-cygming.patch
Patch2: patches/%{pkgname}/bzip2-1.0.6-patch-0003-debian-bzgrep.patch
Patch3: patches/%{pkgname}/bzip2-1.0.6-patch-0004-unsafe-strcpy.patch
Patch4: patches/%{pkgname}/bzip2-1.0.8-patch-0005-progress.patch
Patch5: patches/%{pkgname}/bzip2-1.0.6-patch-0006-mint.patch
Patch6: patches/%{pkgname}/bzip2-1.0.7-patch-0007-Fix-printfs-of-file-sizes.patch
Patch7: patches/%{pkgname}/bzip2-amigaos.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig

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
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities 
of the best techniques available.  However, bzip2 has the added benefit 
of being approximately two times faster at compression and six times 
faster at decompression than those techniques.  Bzip2 is not the 
fastest compression utility, but it does strike a balance between speed 
and compression capability.

Install bzip2 if you need a compression utility.

%package devel
Summary:        Header files and libraries for developing apps which will use bzip2.
Group:          Development/Libraries/C and C++
Requires:       bzip2 = %{version}
%if "%{buildtype}" != "cross"
Provides:       libbz2-devel = %{version}
%endif

%description devel
Header files and a static library of bzip2 functions, for developing apps
which will use the library.

%package doc
Summary:        Documentation files for bzip2
Group:          Productivity/Archiving/Compression
BuildArch:      noarch

%description doc
Documentation for bzip2

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1


%build
rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1

cp %{S:1} config.sub
%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"
STACKSIZE="-Wl,-stack,256k"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

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

	make distclean
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
%{_rpmint_bindir}/*
%else
%{_rpmint_target_prefix}/bin/*
%endif

%files devel
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/*
%{_rpmint_libdir}/*.a
%{_rpmint_libdir}/*/*.a
%{_rpmint_libdir}/pkgconfig/*.pc
%{_rpmint_cross_pkgconfigdir}/*.pc
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/lib/*.a
%{_rpmint_target_prefix}/lib/*/*.a
%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%endif

%files doc
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%doc %{_rpmint_docdir}/%{pkgname}/LICENSE
%doc %{_rpmint_docdir}/%{pkgname}/README
%doc %{_rpmint_docdir}/%{pkgname}/README.COMPILATION.PROBLEMS
%doc %{_rpmint_docdir}/%{pkgname}/README.XML.STUFF
%doc %{_rpmint_docdir}/%{pkgname}/CHANGES
%doc %{_rpmint_docdir}/%{pkgname}/manual.html
%{_rpmint_mandir}/*/*
%else
%doc %{_rpmint_target_prefix}/share/doc/%{pkgname}/LICENSE
%doc %{_rpmint_target_prefix}/share/doc/%{pkgname}/README
%doc %{_rpmint_target_prefix}/share/doc/%{pkgname}/README.COMPILATION.PROBLEMS
%doc %{_rpmint_target_prefix}/share/doc/%{pkgname}/README.XML.STUFF
%doc %{_rpmint_target_prefix}/share/doc/%{pkgname}/CHANGES
%doc %{_rpmint_target_prefix}/share/doc/%{pkgname}/manual.html
%{_rpmint_target_prefix}/share/man/*/*
%endif



%changelog
* Tue Mar 7 2023 Thorsten Otto <admin@tho-otto.de>
- Update to version 1.0.8

* Thu Aug 27 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file

* Fri Jan 26 2018 Thorsten Otto <admin@tho-otto.de>
- updated to 1.0.6
- updated Packager and Vendor

* Fri Feb  7 2003 Adam Klobukowski <atari@gabo.pl>
- updated to 1.0.2

* Mon Dec 25 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 1.0.1; seperated developer files

* Sun Mar 26 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55
- updated to 0.9.5d

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
