%define pkgname lame

%rpmint_header

Summary:        The LAME MP3 encoder
Name:           %{crossmint}%{pkgname}
Version:        3.100
Release:        1
License:        LGPL-2.0-or-later
Group:          Productivity/Multimedia/Sound/Editors and Convertors

Packager:       %{packager}
URL:            https://lame.sourceforge.net/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://prdownloads.sourceforge.net/lame/lame-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/lame/lame-field-width-fix.patch
Patch1: patches/lame/lame-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  make
Provides:       %{crossmint}libmp3lame-devel = %{version}

%rpmint_build_arch

%description
LAME is an educational tool to be used for learning about MP3 encoding.
The goal of the LAME project is to use the open source model to improve the
psycho acoustics, noise shaping and speed of MP3.
Another goal of the LAME project is to use these improvements for the basis of
a patent free audio compression codec for the GNU project.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%patch0 -p1
%patch1 -p1

autoreconf -fiv
cp %{S:1} config.sub

%build

%rpmint_cflags
COMMON_CFLAGS+=" -fno-strict-aliasing"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-static
	--disable-shared
	--without-pic
	--without-libiconv-prefix
	--enable-decoder
	--disable-debug
	--enable-mp3rtp
"

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
%license COPYING LICENSE
%doc API HACKING STYLEGUIDE
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/bin
%{_isysroot}%{_rpmint_target_prefix}/share/man
%{_isysroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}



%changelog
* Mon Nov 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
