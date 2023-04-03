%define pkgname mpeg_lib

%rpmint_header

Summary: 	Interface for MPEG-1 Streams.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version: 	1.3.1
Release: 	1
License: 	BSD-3-Clause
Group: 		System/Libraries

Packager: 	Thorsten Otto <admin@tho-otto.de>
URL: 		http://starship.python.net/~gward/mpeglib/

Source0: 	%{pkgname}-%{version}.tar.gz
Source1:        patches/automake/mintelf-config.sub
Patch0:		mpeg_lib-1.3.1-mint.patch

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root

%rpmint_essential
Provides      : %{name}-devel = %{version}

%rpmint_build_arch



%description
The MPEG Library is a C library for decoding MPEG-1 video streams and dithering 
them to a variety of colour schemes. Most of the code in the library comes 
directly from an old version of the Berkeley MPEG player (mpeg_play), an 
X11-specific implementation that worked fine, but suffered from minimal 
documentation and a lack of modularity. 

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

rm -f aclocal.m4 acinclude.m4 ltmain.sh ltconfig
rm -rf autom4te.cache
autoconf || exit 1
autoheader || :
rm -rf autom4te.cache
rm -f config.sub
cp %{S:1} config.sub


%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	EXTRA_CFLAGS="$CPU_CFLAGS" \
	OPTIMIZE="$COMMON_CFLAGS" \
	EXTRA_LDFLAGS="${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	make # %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files for multilib
	%rpmint_remove_pkg_configs
	# remove obsolete glibconfig.h for multilib

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
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
%defattr(-, root, root)
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/include/*

%changelog
* Sun Mar 26 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Thu Dec 11 2003 Keith Scroggins <kws@radix.net>
- Initial build of mpeg_lib 1.3.1 for MiNT
