%define pkgname graphite2

%rpmint_header

Summary       : Font rendering capabilities for complex non-Roman writing systems
Name          : %{crossmint}%{pkgname}
Version       : 1.3.14
Release       : 1
License       : GPL-2.0-or-later OR LGPL-2.1-or-later OR MPL-2.0
Group         : Development/Libraries/C and C++

%rpmint_essential
BuildRequires:  cmake >= 3.10.0
BuildRequires:  %{crossmint}cmake >= 3.10.0
BuildRequires:  %{crossmint}gcc-c++
BuildRequires:  %{crossmint}freetype2-devel
BuildRequires:  pkgconfig
Provides:       %{crossmint}libgraphite2-devel

Packager      : %{packager}
URL           : http://graphite.sil.org/

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot     : %{_tmppath}/%{name}-root

Source0: https://github.com/silnrsi/graphite/archive/%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz

%rpmint_build_arch


%description
Graphite2 is a project within SIL's Non-Roman Script Initiative and Language
Software Development groups to provide rendering capabilities for complex
non-Roman writing systems. Graphite can be used to create "smart fonts" capable
of displaying writing systems with various complex behaviors. With respect to
the Text Encoding Model, Graphite handles the "Rendering" aspect of writing
system implementation.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n graphite-%{version}

%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags
COMMON_CFLAGS+=" -fno-strict-aliasing"
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
		-DCMAKE_TOOLCHAIN_FILE="%{_rpmint_target_prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake" \
		..

	make %{?_smp_mflags}
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

	make clean > /dev/null
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
%license LICENSE COPYING
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/%{pkgname}
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}/*.pc
%endif


%changelog
* Mon Nov 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
