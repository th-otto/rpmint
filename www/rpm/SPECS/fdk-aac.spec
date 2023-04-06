%define pkgname fdk-aac

%rpmint_header

Summary:        A standalone library of the Fraunhofer FDK AAC code
Name:           %{crossmint}%{pkgname}
Version:        2.0.2
Release:        1
License:        FDK-AAC
Group:          Development/Libraries/C and C++

Packager:       %{packager}
URL:            https://github.com/mstorsjo/fdk-aac

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/${PACKAGENAME}/fdk-aac-mint.patch

%rpmint_essential
BuildRequires:  %{crossmint}gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
Provides:       %{crossmint}libfdk-aac-devel

%rpmint_build_arch

%description
A standalone library of the Fraunhofer FDK AAC code from Android.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

autoreconf -fiv
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-example
"

for CPU in ${ALL_CPUS}
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make clean >/dev/null
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
%doc ChangeLog NOTICE OWNERS
%{_isysroot}/%{_rpmint_target_prefix}/bin/*
%{_isysroot}/%{_rpmint_target_prefix}/include/*
%{_isysroot}/%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}/%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}/%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif


%changelog
* Thu Apr 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
