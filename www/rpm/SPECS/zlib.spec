%define pkgname zlib

%rpmint_header

Summary:        Library implementing the DEFLATE compression algorithm
Name:           %{crossmint}%{pkgname}
Version:        1.3
Release:        1
License:        Zlib
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.zlib.net/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://www.zlib.net/%{pkgname}-%{version}.tar.xz
Patch0: zlib-pkgconfig.patch
Patch1: zlib-shared.patch
Patch2: zlib-1.2.12-0013-segfault.patch

%rpmint_essential
Provides:       %{crossmint}zlib-devel

%rpmint_build_arch

%description
zlib is a general-purpose lossless data-compression library,
implementing an API for the DEFLATE algorithm, the latter of
which is being used by, for example, gzip and the ZIP archive
format.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%rpmint_cflags

export CHOST=$TARGET

COMMON_CFLAGS="-O3 -fomit-frame-pointer"
CONFIGURE_FLAGS="--prefix=%{_rpmint_target_prefix}
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
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
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Wed Nov 15 2023 Thorsten Otto <admin@tho-otto.de>
- Update to 1.3
- update header file with sharedlib version

* Wed Mar 1 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to 1.2.13

* Fri May 21 2010 Keith Scroggins <kws@radix.net>
- updated to 1.2.5 and built for 68000/68020-60/5475

* Sat Jan 16 2010 Keith Scroggins <kws@radix.net>
- updated to 1.2.3 and built for 68000/68020-60/5475

* Sat Jan 04 2003 Matthias Alles <alles@rhrk.uni-kl.de>
- updated to 1.2.1

* Wed Mar 13 2002 Frank Naumann <fnaumann@freemint.de>
- updated to 1.1.4

* Sat Mar 25 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compress manpage
- correct Packager and Vendor
- added %description de and Summary(de)
