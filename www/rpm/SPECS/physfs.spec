%define pkgname physfs

%rpmint_header

Summary       : PhysicsFS file abstraction layer for games
Name          : %{crossmint}%{pkgname}
Version       : 3.2.0
Release       : 1
License       : (CPL-1.0 OR LGPL-2.1-or-later) AND Zlib
Group         : System/Libraries

%rpmint_essential
BuildRequires:  cmake >= 3.10.0
%if "%{buildtype}" == "cross"
BuildRequires:  %{crossmint}cmake
%endif
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires : %{crossmint}zlib-devel

Packager      : %{packager}
URL           : https://www.icculus.org/physfs/

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: https://github.com/icculus/physfs/archive/refs/tags/%{pkgname}-%{version}.tar.gz
patch0: patches/physfs/physfs-mint.patch

%rpmint_build_arch


%description
PhysicsFS is a library to provide abstract access to various archives.
It is intended for use in video games, and the design was somewhat
inspired by Quake 3's file subsystem. The programmer defines a "write
directory" on the physical filesystem. No file writing done through the
PhysicsFS API can leave that write directory, for security. For
example, an embedded scripting language cannot write outside of this
path if it uses PhysFS for all of its I/O, which means that untrusted
scripts can run more safely. Symbolic links can be disabled as well,
for added safety. For file reading, the programmer lists directories
and archives that form a "search path". Once the search path is
defined, it becomes a single, transparent hierarchical filesystem. This
makes for easy access to ZIP files in the same way as you access a file
directly on the disk, and it makes it easy to ship a new archive that
will override a previous archive on a per-file basis. Finally,
PhysicsFS gives you platform-abstracted means to determine if CD-ROMs
are available, the user's home directory, where in the real filesystem
your program is running, etc.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags
CMAKE_SYSTEM_NAME="${TARGET##*-}"

export prefix=%{_rpmint_target_prefix}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	cmake \
		-DCMAKE_BUILD_TYPE=Release \
		-DCMAKE_INSTALL_PREFIX=%{_rpmint_target_prefix} \
		-DPHYSFS_BUILD_STATIC=TRUE \
		-DPHYSFS_BUILD_SHARED=FALSE \
		-DPHYSFS_BUILD_TEST=FALSE \
		-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME} \
		-DCMAKE_C_COMPILER="${TARGET}-gcc" \
		-DCMAKE_C_FLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		-DPTHREAD_LIBRARY="" \
		-DCMAKE_TOOLCHAIN_FILE="%{_rpmint_target_prefix}/share/cmake/Modules/Platform/${CMAKE_SYSTEM_NAME}.cmake" \
		.

	make %{?_smp_mflags}
	make DESTDIR="%{buildroot}%{_isysroot}" install
	
	if test "$multilibdir" != ""; then
		mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib$multilibdir
		mv %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/*.a %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib$multilibdir
	fi
	
	# compress manpages
	%rpmint_gzip_docs

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
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}/*.pc
%endif


%changelog
* Sat Sep 16 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
- Update to version 3.2.0
