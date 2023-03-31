%define pkgname lua53
%define major_version 5.3

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Small Embeddable Language with Procedural Syntax
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        5.3.4
Release:        1
License:        MIT
Group:          Development/Languages/Other

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.lua.org

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://www.lua.org/ftp/lua-%{version}.tar.gz
Patch0:  patches/lua53/lua53-build-system.patch
Patch1:  patches/lua53/lua53-buildconf.patch

%rpmint_essential
BuildRequires:  make
%if "%{buildtype}" == "cross"
Provides:       cross-mint-lua53-devel
Provides:       cross-mint-lua-devel
%else
Provides:       lua53-devel
Provides:       lua-devel
%endif

%rpmint_build_arch

%description
Lua is a programming language originally designed for extending
applications, but is also frequently used as a general-purpose,
stand-alone language.

Lua combines procedural syntax (similar to Pascal) with
data description constructs based on associative arrays and extensible
semantics. Lua is dynamically typed, interpreted from byte codes, and
has automatic memory management, making it suitable for configuration,
scripting, and rapid prototyping. Lua is implemented as a small library
of C functions, written in ANSI C.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n lua-%{version}
%patch0 -p1
%patch1 -p1

cat doc/lua.1  | sed 's/TH LUA 1/TH LUA${major_version} 1/' > doc/lua%{major_version}.1
cat doc/luac.1 | sed 's/TH LUAC 1/TH LUAC${major_version} 1/' > doc/luac%{major_version}.1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	make %{?_smp_mflags} -C src \
		CC="${TARGET}-gcc" \
		AR="${TARGET}-ar rcu " \
		RANLIB=${TARGET}-ranlib \
		MYCFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -std=gnu99 -D_GNU_SOURCE $LTO_CFLAGS" \
		MYLIBS="$CPU_CFLAGS $LTO_CFLAGS ${STACKSIZE}" \
		V=%{major_version} \
		all

	make \
		V=%{major_version} \
		INSTALL_TOP="%{buildroot}%{_rpmint_prefix}" \
		INSTALL_LIB="%{buildroot}%{_rpmint_libdir}"$multilibdir \
		install
	ln -s liblua%{major_version}.a "%{buildroot}%{_rpmint_libdir}"$multilibdir/liblua.a
	ln -sf lua%{major_version} %{buildroot}%{_rpmint_bindir}/lua
	ln -sf luac%{major_version} %{buildroot}%{_rpmint_bindir}/luac

	install -D -d -m 755 %{buildroot}%{_rpmint_libdir}/lua/%{major_version}

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

# create pkg-config file
mkdir -p %{buildroot}%{_rpmint_libdir}/pkgconfig
cat > %{buildroot}%{_rpmint_libdir}/pkgconfig/lua%{major_version}.pc <<-EOF
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include/lua%{major_version}
INSTALL_LMOD=\${prefix}/share/data/lua/%{major_version}
INSTALL_CMOD=\${libdir}/lua/%{major_version}

Name: Lua %{major_version}
Description: An Extensible Extension Language
Version: %{version}
Libs: -llua%{major_version} -lm
Cflags: -I\${includedir}
EOF
ln -s lua%{major_version}.pc %{buildroot}%{_rpmint_libdir}/pkgconfig/lua.pc

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
%doc README
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Fri Mar 31 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
