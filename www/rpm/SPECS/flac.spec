%define pkgname flac

%rpmint_header

Summary:        Free Lossless Audio Codec
Name:           %{crossmint}%{pkgname}
Version:        1.3.2
Release:        1
License:        BSD-3-Clause and GPL-2.0-or-later and GFDL-1.2
Group:          Productivity/Multimedia/Sound/Utilities

Packager:       %{packager}
URL:            https://xiph.org/flac/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://downloads.xiph.org/releases/flac/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/flac/flac-CVE-2017-6888.patch
Patch1: patches/flac/flac-cflags.patch
Patch2: patches/flac/flac-lrintf.patch
Patch3: patches/flac/flac-staticlibs.patch
Patch4: patches/flac/flac-config.patch
Patch5: patches/flac/flac-amigaos.patch
Patch6: patches/flac/flac-wcwidth.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  %{crossmint}gcc-c++
BuildRequires:  %{crossmint}libogg-devel
Provides:       %{crossmint}libFLAC-devel
Provides:       %{crossmint}libFLAC++-devel

%rpmint_build_arch

%description
FLAC is an audio coding format for lossless compression of digital
audio, and is also the name of the reference software package that
includes a codec implementation. Digital audio compressed by FLAC&apos;s
algorithm can typically be reduced to between 50 and 70 percent of
its original size, and decompresses to an identical copy of the
original audio data.

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

rm -f aclocal.m4 ltmain.sh
libtoolize --force
aclocal -I m4
autoconf
autoheader
automake --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--with-ogg=yes
	--disable-shared
"

for CPU in ${ALL_CPUS}
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname} install

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

	make clean >/dev/null
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
%license COPYING*
%doc AUTHORS README
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}/*
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal/*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif


%changelog
* Fri Apr 07 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
