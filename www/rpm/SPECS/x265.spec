%define pkgname x265

%rpmint_header

Summary       : A free h265/HEVC encoder - encoder binary
Name          : %{crossmint}%{pkgname}
Version       : 3.5
Release       : 1
License       : GPL-2.0-or-later
Group         : Productivity/Multimedia/Video/Editors and Convertors

%rpmint_essential
BuildRequires:  cmake >= 3.10.0
BuildRequires:  %{crossmint}cmake
BuildRequires:  %{crossmint}gcc-c++
BuildRequires:  pkgconfig

Packager      : %{packager}
URL           : https://bitbucket.org/multicoreware/x265_git

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot     : %{_tmppath}/%{name}-root

Source0: https://bitbucket.org/multicoreware/x265_git/downloads/%{pkgname}_%{version}.tar.gz
patch0: patches/x265/x265-arm.patch
patch1: patches/x265/x265-fix_enable512.patch
patch2: patches/x265/x265-mint.patch

%rpmint_build_arch


%description
x265 is a free library for encoding next-generation H265/HEVC video
streams.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}_%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags
CMAKE_SYSTEM_NAME="${TARGET##*-}"

export prefix=%{_rpmint_target_prefix}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	mkdir -p build/${TARGET}
	cd build/${TARGET}
	
	cmake \
		-Wno-dev \
		-DCMAKE_BUILD_TYPE=Release \
		-DCMAKE_INSTALL_PREFIX=%{_rpmint_target_prefix} \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_C_COMPILER="${TARGET}-gcc" \
		-DCMAKE_CXX_COMPILER="${TARGET}-g++" \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DCMAKE_CXX_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DENABLE_PIC=OFF \
		-DENABLE_CLI=ON \
		-DCMAKE_TOOLCHAIN_FILE="%{_rpmint_target_prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake" \
		../../source

	# parallel does not work? creates truncated objects in libx265.a
	make
	make DESTDIR="%{buildroot}%{_rpmint_sysroot}" install
	
	if test "$multilibdir" != ""; then
		mkdir -p %{buildroot}%{_rpmint_libdir}$multilibdir
		mv %{buildroot}%{_rpmint_libdir}/*.a %{buildroot}%{_rpmint_libdir}$multilibdir
	fi
	
	# compress manpages
	%rpmint_gzip_docs

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
	%endif

	make clean
	cd ../..
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
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}/*.pc
%endif


%changelog
* Mon Sep 18 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
- Update to version 3.5
