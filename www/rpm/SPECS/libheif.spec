%define pkgname libheif

%rpmint_header

Summary:        HEIF and AVIF (AV1 Image File Format) file format decoder and encoder
Name:           %{crossmint}%{pkgname}
Version:        1.14.2
Release:        1
License:        LGPL-3.0-or-later
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/strukturag/libheif/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: packages/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/libheif/libheif-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  %{crossmint}gcc-c++
BuildRequires:  %{crossmint}libde265-devel
BuildRequires:  %{crossmint}x265
Requires:       %{crossmint}libde265
Provides:       %{crossmint}libheif-devel
%endif

%rpmint_build_arch

%description
libheif is an ISO/IEC 23008-12:2017 HEIF and AVIF (AV1 Image File
Format) file format decoder and encoder.

HEIF and AVIF are new image file formats employing HEVC (h.265) or AV1
image coding, respectively, for the best compression ratios currently
possible.

libheif makes use of libde265 for HEIF image decoding and x265 for
encoding. For AVIF, libaom, dav1d, svt-av1, or rav1e are used as
codecs.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub

%build

export LANG=POSIX
export LC_ALL=POSIX

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-threads
	--disable-shared
	--disable-visibility
	--without-pic
	--disable-multithreading
"

STACKSIZE="-Wl,-stack,128k"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

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
* Wed Mar 8 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
