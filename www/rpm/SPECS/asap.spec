%define pkgname asap

%rpmint_header

Summary:        Player of Atari 8-bit chiptunes
Name:           %{crossmint}%{pkgname}
Version:        5.0.1
Release:        1
License:        GPL-2.0
Group:          Productivity/Multimedia/Sound/Players

Packager:       %{packager}
URL:            http://asap.sourceforge.net/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.gz

%rpmint_essential
BuildRequires:  make
Provides:       %{crossmint}libasap-devel

%rpmint_build_arch

%description
ASAP is a player of Atari 8-bit chiptunes for modern computers and
mobile devices. It emulates the POKEY sound chip and the 6502
processor. The project was initially based on the routines from the
Atari800 emulator, but the current version has an original emulation
core.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	make V=1 \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	CC=%{_rpmint_target_gcc} \
	AR=%{_rpmint_target_ar} \
	RANLIB=%{_rpmint_target_ranlib}

	make DESTDIR=%{buildroot}%{_rpmint_sysroot} prefix=%{_rpmint_target_prefix} libdir='${prefix}/lib'$multilibdir install

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

	# we do not use "make clean" here because that removes files
	# which have to be rebuild using xasm
	rm -f *.o *.a asapconv
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
%license COPYING
%doc README
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a



%changelog
* Wed Apr 05 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
