%define pkgname libsolv

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Package dependency solver using a satisfiability algorithm
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.6.33
Release:        1
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/openSUSE/libsolv

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

# https://github.com/openSUSE/%%{pkgname}/archive/refs/tags%%{version}.tar.gz
Source0: %{pkgname}-%{version}.tar.bz2
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/libsolv-mint.patch
Patch1: patches/%{pkgname}/libsolv-lto.patch

%rpmint_essential
BuildRequires:  cmake
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-cmake
Provides:       cross-mint-libsolv-devel
%else
Provides:       libsolv-devel
%endif

%rpmint_build_arch

%description
libsolv is a library for solving packages and reading repositories.
The solver uses a satisfiability algorithm.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS+=" -fno-strict-aliasing"
STACKSIZE="-Wl,--stack,512k"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	 --docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname}
"
gcc=`which ${TARGET}-gcc`
gxx=`which ${TARGET}-g++`
CMAKE_SYSTEM_NAME="${TARGET##*-}"


for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	find . -type f -name CMakeCache.txt -delete
	find . -type d -name CMakeFiles -print0 | xargs -0 rm -rf

	export CC="$gcc"
	export CXX="$gxx"
	
	cmake \
		-DCMAKE_INSTALL_PREFIX=%{_rpmint_target_prefix} \
		-DCMAKE_BUILD_TYPE=RelWithDebInfo \
		-DSUSE=1 \
		-DENABLE_SUSEREPO=1 \
		-DENABLE_APPDATA=1 \
		-DENABLE_HELIXREPO=1 \
		-DENABLE_COMPS=1 \
		-DUSE_VENDORDIRS=1 \
		-DCMAKE_SKIP_RPATH=1 \
		-DWITH_LIBXML2=1 \
		-DENABLE_STATIC=1 \
		-DDISABLE_SHARED=1 \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_TOOLCHAIN_FILE="%{_prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake" \
		-DCMAKE_C_COMPILER="$gcc" \
		-DCMAKE_CXX_COMPILER="$gxx" \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS" \
		-DCMAKE_CXX_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS" \
		-DCMAKE_EXE_LINKER_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS $STACKSIZE" \
		.
	
	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	if test "$multilibdir" != ""; then
		mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib$multilibdir
		mv %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/*.a %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib$multilibdir
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
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%{_isysroot}%{_rpmint_target_prefix}/share
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Wed Mar 29 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
