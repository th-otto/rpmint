%define pkgname openh264

%rpmint_header

Summary:        Library which supports H.264 encoding and decoding
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        2.3.0
Release:        1
License:        BSD-2-Clause
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://libexif.sourceforge.net

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

# https://github.com/cisco/openh264/archive/refs/tags/v2.3.0.tar.gz
Source0: %{pkgname}-%{version}.tar.gz
Patch0:  patches/%{pkgname}/%{pkgname}-%{version}-mint.patch

%rpmint_essential
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-gcc-c++
BuildRequires:  cross-mint-pthread-devel
Provides:       cross-mint-openh264-devel
%else
BuildRequires:  gcc-c++
BuildRequires:  pthread-devel
Provides:       openh264-devel
%endif

%rpmint_build_arch

%description
OpenH264 is a codec library which supports H.264 encoding and decoding.
It is suitable for use in real time applications such as WebRTC. See
<a href="http://www.openh264.org/">http://www.openh264.org/</a> for more details.

Needs the pth library from above.
You need to use g++ to link against this library.
Original MiNT-Patch by medmed.

A simple GEM example can be found in <a href="https://www.atari-forum.com/viewtopic.php?p=436559#p436559">this thread</a>

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	OS=freemint \
	ARCH=m68k \
	CC="${TARGET}-gcc" \
	CXX="${TARGET}-g++" \
	AR="${ar}" \
	ARFLAGS=rcs \
	RANLIB=${ranlib} \
	NM=${TARGET}-nm \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	make %{?_smp_mflags} V=Yes || exit 1

	OS=freemint \
	ARCH=m68k \
	make PREFIX="%{buildroot}%{_rpmint_sysroot}/%{_rpmint_target_prefix}" LIBDIR_NAME='lib'$multilibdir install

	mkdir -p "%{buildroot}%{_rpmint_bindir}"
	cp h264dec h264enc "%{buildroot}%{_rpmint_bindir}"
	%{_rpmint_target}-strip "%{buildroot}%{_rpmint_bindir}"/*

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	OS=freemint \
	ARCH=m68k \
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
%if "%{buildtype}" == "cross"
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%else
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%endif



%changelog
* Tue Mar 7 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
