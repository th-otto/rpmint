%define pkgname mp4v2

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        A C/C++ library to create, modify and read MP4 files
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        2.1.1
Release:        1
License:        MPL-1.1
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://mp4v2.org/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://github.com/enzo1982/mp4v2/archive/refs/tags/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/%{pkgname}/mp4v2-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make
%if "%{buildtype}" == "cross"
Provides:       cross-mint-mp4v2-devel
%else
Provides:       libmp4v2-devel
%endif

%rpmint_build_arch

%description
The MP4v2 library provides an API to create and modify MP4 files as
defined by ISO-IEC:14496-1:2001 MPEG-4 Systems. This file format is
derived from Apple's QuickTime file format that has been used as a
multimedia file format in a variety of platforms and applications. It
is a very powerful and extensible format that can accommodate
practically any type of media.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

autoreconf -fiv
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} autoaux/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-fvisibility
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	# help2man is bogus, it tries to execute the just-compiled binaries
	sed -i "s|S\[\"FOUND_HELP2MAN\"\]=.*|S[\"FOUND_HELP2MAN\"]=\"no\"|" config.status
	./config.status

	make V=1 %{?_smp_mflags}
	make prefix=%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix} install

	# remove the empty man pages
	rm -f %{buildroot}%{_rpmint_sysroot}/usr/share/man/man1/*
	
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

	make distclean
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
%{_isysroot}%{_rpmint_target_prefix}/include/%{pkgname}/*
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Sun Apr 02 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
