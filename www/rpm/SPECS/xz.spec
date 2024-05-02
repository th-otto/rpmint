%define pkgname xz

%rpmint_header

Summary:        A Program for Compressing Files with the Lempel–Ziv–Markov algorithm
Name:           %{crossmint}%{pkgname}
Version:        5.4.4
Release:        2
License:        LGPL-2.1+ AND GPL-2.0+
Group:          Productivity/Archiving/Compression

Packager:       %{packager}
URL:            http://tukaani.org/xz/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://tukaani.org/xz/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  make
Provides:       %{crossmint}liblzma5 = %{version}
Provides:       %{crossmint}lzma-devel = %{version}

%rpmint_build_arch

%description
The xz command is a program for compressing files.
* Average compression ratio of LZMA is about 30%% better than that of
  gzip, and 15%% better than that of bzip2.
* Decompression speed is only little slower than that of gzip, being
  two to five times faster than bzip2.
* In fast mode, compresses faster than bzip2 with a comparable
  compression ratio.
* Achieving the best compression ratios takes four to even twelve
  times longer than with bzip2. However, this does not affect
  decompressing speed.
* Very similar command line interface to what gzip and bzip2 have.

%prep
%setup -q -n %{pkgname}-%{version}
cp %{S:1} build-aux/config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname}
    --disable-threads
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

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
%if "%{buildtype}" == "cross"
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}
%{_rpmint_datadir}
%else
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%endif



%changelog
* Sun Aug 06 2023 Thorsten Otto <admin@tho-otto.de>
- Update to 5.4.4

* Thu Mar 02 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
