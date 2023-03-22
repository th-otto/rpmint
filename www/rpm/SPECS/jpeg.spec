%define pkgname jpeg

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        A library for manipulating JPEG image files
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        8d
Release:        3
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.ijg.org/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://www.ijg.org/files/jpegsrc.v%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/jpeg/jpeg-8d-0007-mintslb.patch 

BuildRequires:  autoconf
BuildRequires:  automake
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libjpeg-devel
%else
Provides:       libjpeg-devel
%endif

%rpmint_build_arch

%description
This package is a library of functions that manipulate jpeg images, along
with simple clients for manipulating jpeg images.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
cp %{S:1} config.sub

%build

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

mkdir -p "%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}"
cp -a README usage.txt "%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}"

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
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib
%doc %{_isysroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}/README
%doc %{_isysroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}/usage.txt
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*



%changelog
* Wed Mar 22 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Thu Jun 10 2010 Peter Slegg <>
- remove mint and c++ patches
- remove install-lib
- tidy-up to work with better structure of v8

* Sat Dec 23 2000 Frank Naumann <fnaumann@freemint.de>
- added c++ header patch

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55
