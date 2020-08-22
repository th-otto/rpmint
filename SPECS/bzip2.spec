%define pkgname bzip2

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

Summary:        A file compression utility.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.0.6
Release:        1
License:        BSD
Group:          Productivity/Archiving/Compression

Packager:       Thorsten Otto <admin@tho-otto.de>
Vendor:         RPMint
URL:            http://www.bzip.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz
Patch0: bzip2-1.0.6-patch-0001-configure.patch
Patch1: bzip2-1.0.6-patch-0002-cygming.patch
Patch2: bzip2-1.0.6-patch-0003-debian-bzgrep.patch
Patch3: bzip2-1.0.6-patch-0004-unsafe-strcpy.patch
Patch4: bzip2-1.0.6-patch-0005-progress.patch
Patch5: bzip2-1.0.6-patch-0006-mint.patch
Patch6: bzip2-1.0.6-patch-0007-Fix-printfs-of-file-sizes.patch
Patch7: bzip2-amigaos.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig

%rpmint_build_arch

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
%patch2 -p1
%patch3 -p1
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

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"
STACKSIZE="-Wl,-stack,256k"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	make
	make DESTDIR=${RPM_BUILD_ROOT}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f ${RPM_BUILD_ROOT}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make distclean
done


%install

%rpmint_cflags

# already done in loop above
# make install DESTDIR=${RPM_BUILD_ROOT}%{_rpmint_sysroot}

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}%{_rpmint_sysroot}
rmdir ${RPM_BUILD_ROOT}%{_rpmint_installdir} || :
rmdir ${RPM_BUILD_ROOT}%{_prefix} 2>/dev/null || :
%endif

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


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
%{_rpmint_libdir}/m68020-60/*.a
%{_rpmint_libdir}/m5475/*.a
%{_rpmint_libdir}/pkgconfig/*.pc
%{_rpmint_cross_pkgconfigdir}/*.pc
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/lib/*.a
%{_rpmint_target_prefix}/lib/m68020-60/*.a
%{_rpmint_target_prefix}/lib/m5475/*.a
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
