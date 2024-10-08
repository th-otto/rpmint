%define pkgname smpeg

%rpmint_header

Summary:        Software MPEG decoder
Name:           %{crossmint}%{pkgname}
Version:        0.4.5
Release:        1
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.lokigames.com/development/smpeg.php3

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make
Provides:       %{crossmint}libsmpeg-devel

%rpmint_build_arch

%description
SMPEG is based on UC Berkeley&apos;s mpeg_play software MPEG decoder
and SPLAY, an mpeg audio decoder created by Woo-jae Jung. We have
completed the initial work to wed these two projects in order to 
create a general purpose MPEG video/audio player.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

rm -f aclocal.m4 ltmain.sh
libtoolize --force
aclocal -I acinclude
autoconf
automake --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
"

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
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/smpeg
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/share
%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Mon Apr 03 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
