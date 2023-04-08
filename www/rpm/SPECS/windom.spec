%define pkgname windom

%rpmint_header

Summary:        A high level GEM library for TOS system
Name:           %{crossmint}%{pkgname}
Version:        2.0.1
Release:        1
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++

Packager:       %{packager}
URL:            http://windom.sourceforge.net/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz

Patch0: patches/windom/windom-cross.patch
Patch1: patches/windom/windom-menuexec.patch
Patch2: patches/windom/windom-formthumb.patch
Patch3: patches/windom/windom-gemlib.patch

%rpmint_essential
BuildRequires:  make
BuildRequires:  %{crossmint}libldg-devel
Provides:       %{crossmint}libwindom-devel

%rpmint_build_arch

%description
Windom is a C library to make GEM programming very easy. With the help
of windom, you can focus on programming the real job of your
application, and let windom handle complex and "automatic" GEM stuff
(toolbar, forms, menu in windows...).
Warning: do not run make in the top level directory
after unpacking the source archive; the build system is utterly broken and will
remove your source directory.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS="-Os -fomit-frame-pointer $LTO_CFLAGS"

SUBDIRS="src demo"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	rm -f lib/gcc/*.a
	for dir in $SUBDIRS; do
		cd $dir || exit 1
		make clean
		make -f gcc.mak \
			CROSS_PREFIX=${TARGET}- \
			M68K_ATARI_MINT_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
			M68K_ATARI_MINT_LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
		mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib
		mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/include
		make -f gcc.mak \
			PREFIX=%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix} \
			CROSS_PREFIX=${TARGET}- \
			M68K_ATARI_MINT_CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
			M68K_ATARI_MINT_LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" install
		cd ..
	done

	if test "$multilibdir" != ""; then
		mkdir -p "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib$multilibdir"
		mv %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/*.a "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib$multilibdir"
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
%license COPYRIGHT
%doc AUTHORS CHANGES ChangeLog COMPONENTS INSTALL README VERSION doc/*
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a



%changelog
* Tue Apr 04 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- updated to windom 2.0.1

* Mon Feb 20 2006 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated for windom 2.0.0-1

* Tue Feb 14 2006 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated for windom 2.0.0-RC2

* Tue Dec 20 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- Initial version of the windom package for windom 2.0.0-RC1
