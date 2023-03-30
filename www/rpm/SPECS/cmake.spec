%define pkgname cmake

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Cross-platform, open-source make system
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        3.10.2
Release:        1
License:        BSD-3-Clause
Group:          Development/Tools/Building

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.cmake.org/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://www.cmake.org/files/v3.10/%{pkgname}-%{version}.tar.gz
Source1: patches/cmake/cmake.macros
Source2: patches/cmake/cmake.attr
Source3: patches/cmake/cmake.prov
Source4: patches/cmake/cmake-mint.cmake
Source5: patches/cmake/cmake-mint-cross.cmake
Source6: patches/cmake/cmake-mintelf.cmake
Source7: patches/cmake/cmake-mintelf-cross.cmake
Patch0: patches/cmake/cmake-fix-ruby-test.patch
Patch1: patches/cmake/cmake-mint-rules.patch
Patch2: patches/cmake/cmake-form.patch
Patch3: patches/cmake/cmake-system-libs.patch
Patch4: patches/cmake/cmake-3.10.1_boost-1.66.patch
Patch5: patches/cmake/cmake-feature-python-interp-search-order.patch
Patch6: patches/cmake/cmake-c17-default.patch
Patch7: patches/cmake/cmake-0001-Cannot-use-C-reference-in-C-code.patch
Patch8: patches/cmake/cmake-0001-No-SA_SIGINFO.patch
Patch9: patches/cmake/cmake-mint-c++-math.patch
Patch10: patches/cmake/cmake-no-isystem.patch
Patch11: patches/cmake/cmake-replace-find_package-with-pkgconfig.patch


%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make
Provides:       cmake(%_rpmint_target)
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-libuv-devel
BuildRequires:  cross-mint-librhash-devel
%else
BuildRequires:  libuv-devel
BuildRequires:  librhash-devel
%endif

%rpmint_build_arch

%description
CMake is a cross-platform, open-source build system

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
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

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

STACKSIZE="-Wl,--stack,512k"
CMAKE_SYSTEM_NAME="${TARGET##*-}"
JOBS=%{?_smp_mflags}

gcc=`which ${TARGET}-gcc`
gxx=`which ${TARGET}-g++`
# This is not autotools configure
CONFIGURE_FLAGS="
	--prefix=%{_rpmint_target_prefix} \
	--datadir=/share/%{pkgname} \
	--docdir=/share/doc/%{pkgname} \
	--mandir=/share/man \
	--system-libs \
	--no-system-jsoncpp \
	--verbose \
	--no-qt-gui \
	${JOBS/-j/--parallel=} \
	-- \
	-DCMAKE_USE_SYSTEM_LIBRARY_LIBUV=ON \
	-DCMAKE_TOOLCHAIN_FILE=$MINT_BUILD_DIR/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake \
"

#
# For some obscure reason, bootstrapping seems
# to require absolute paths for the compiler
#
sed -e 's,CMAKE_C_COMPILER [^)]*),CMAKE_C_COMPILER '"$gcc"'),' \
    -e 's,CMAKE_CXX_COMPILER [^)]*),CMAKE_CXX_COMPILER '"$gxx"'),' \
    "%{S:5}" > "Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake"

$LN_S -f ${CMAKE_SYSTEM_NAME}.cmake "Modules/Platform/${TARGET#-}.cmake"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	./configure ${CONFIGURE_FLAGS} \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DCMAKE_CXX_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $CXX_EXCEPTIONS" \
		-DCMAKE_EXE_LINKER_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS $CXX_EXCEPTIONS $STACKSIZE"

	make %{?_smp_mflags}

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	buildroot="%{buildroot}%{_rpmint_sysroot}"
	make DESTDIR="${buildroot}" install
	mkdir -p "${buildroot}%{_rpmint_target_prefix}/lib/%{pkgname}"
	find "${buildroot}%{_rpmint_target_prefix}/share/%{pkgname}" -type f -print0 | xargs -0 chmod 644
	# rpm macros
	install -m644 %{S:1} -D ${buildroot}/etc/rpm/macros.cmake
	install -m644 %{S:2} -D ${buildroot}%{_rpmint_target_prefix}/lib/rpm/fileattrs/cmake.attr
	install -m644 %{S:3} -D ${buildroot}%{_rpmint_target_prefix}/lib/rpm/cmake.prov
	install -m644 %{S:4} -D ${buildroot}%{_rpmint_target_prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake
	if test "${CMAKE_SYSTEM_NAME}" = mint; then
		ln -sf ${CMAKE_SYSTEM_NAME}.cmake "${buildroot}%{_rpmint_target_prefix}/share/cmake/Modules/Platform/FreeMiNT.cmake"
	fi
	
	%if "%{buildtype}" == "cross"
	install -m644 %{S:5} -D "%{buildroot}%{_prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake"
	$LN_S -f ${CMAKE_SYSTEM_NAME}.cmake "%{buildroot}%{_prefix}/share/cmake/Modules/Platform/${TARGET#-}.cmake"
	if test "${CMAKE_SYSTEM_NAME}" = mint; then
		ln -sf ${CMAKE_SYSTEM_NAME}.cmake "%{buildroot}%{_prefix}/share/cmake/Modules/Platform/FreeMiNT.cmake"
	fi
	%endif
	
	make clean >/dev/null

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
%{_isysroot}/etc
%{_isysroot}%{_rpmint_target_prefix}/bin
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share
%if "%{buildtype}" == "cross"
%{_prefix}/share/cmake/Modules/Platform/*
%endif



%changelog
* Thu Mar 30 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
