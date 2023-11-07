%define pkgname libaom

%rpmint_header

Summary:        AV1 codec library
Name:           %{crossmint}%{pkgname}
Version:        3.7.0
Release:        1
License:        BSD-2-Clause
Group:          Productivity/Multimedia/Other

Packager:       %{packager}
URL:            https://aomedia.googlesource.com/aom/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/libaom/libaom-0001-Do-not-disable-_FORTIFY_SOURCE.patch
Patch1: patches/libaom/libaom-mint.patch

%rpmint_essential
BuildRequires:  cmake >= 3.6
BuildRequires:  %{crossmint}cmake >= 3.10.0
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  %{crossmint}libyuv-devel
Provides:       %{crossmint}%{pkgname}-devel = %{version}

%rpmint_build_arch

%description
This is a library for AOMedia Video 1 (AV1), an open, royalty-free
video coding format designed for video transmissions over the Internet.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%patch0 -p1
%patch1 -p1

%build

%rpmint_cflags
COMMON_CFLAGS+=" -fno-strict-aliasing"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CMAKE_SYSTEM_NAME="${TARGET##*-}"

export prefix=%{_rpmint_target_prefix}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	mkdir -p build
	cd build
	
	cmake -G "Unix Makefiles" \
		-DCMAKE_BUILD_TYPE=Release \
		-DBUILD_SHARED_LIBS=OFF \
		-DCMAKE_INSTALL_PREFIX=%{_rpmint_target_prefix} \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_C_COMPILER="${TARGET}-gcc" \
		-DCMAKE_CXX_COMPILER="${TARGET}-g++" \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DCMAKE_CXX_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DENABLE_PIC=OFF \
		-DENABLE_DOCS=no \
		-Dgtest_disable_pthreads=1 \
		-DENABLE_TESTS=OFF \
		-DCMAKE_TOOLCHAIN_FILE="%{_rpmint_target_prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake" \
		..

	echo '#undef HAVE_PTHREAD_H' >> ./config/aom_config.h
	echo '#undef CONFIG_MULTITHREAD' >> ./config/aom_config.h

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	if test "$multilibdir" != ""; then
		mkdir -p %{buildroot}%{_rpmint_libdir}$multilibdir
		mv %{buildroot}%{_rpmint_libdir}/*.a %{buildroot}%{_rpmint_libdir}$multilibdir
	fi
	
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
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
	%endif

	make clean
	cd ..
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
%license LICENSE PATENTS
%doc AUTHORS CHANGELOG
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/bin
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Mon Nov 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
