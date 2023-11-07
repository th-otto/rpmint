%define pkgname x264

%rpmint_header

Summary       : H.264/MPEG-4 AVC format encoder
Name          : %{crossmint}%{pkgname}
Version       : 20230215
Release       : 1
License       : GPL-2.0-or-later
Group         : Productivity/Multimedia/Other

%rpmint_essential
BuildRequires:  cmake >= 3.10.0
BuildRequires:  %{crossmint}cmake
BuildRequires:  %{crossmint}gcc-c++
BuildRequires:  pkgconfig
Provides:       %{crossmint}libx264-devel

Packager      : %{packager}
URL           : https://code.videolan.org/videolan/x264

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot     : %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
patch0: patches/x264/x264-mint.patch

%rpmint_build_arch


%description
x264 package provides a library for encoding video streams into the H.264/MPEG-4 AVC format. 

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

cp %{S:1} config.sub

%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags
COMMON_CFLAGS+=" -fno-strict-aliasing"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-static
	--disable-avs
	--disable-opencl
	--disable-cli
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	LD="${TARGET}-gcc" \
	CC="${TARGET}-gcc" \
	CXX="${TARGET}-g++" \
	AR="${ar}" \
	RANLIB=${ranlib} \
	NM=${TARGET}-nm \
	STRIP=${TARGET}-strip \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR="%{buildroot}%{_rpmint_sysroot}" install
	
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
%doc AUTHORS
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}/*.pc
%endif


%changelog
* Mon Nov 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
