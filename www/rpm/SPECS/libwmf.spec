%define pkgname libwmf

%rpmint_header

Summary       : library and utilities for displaying and converting metafile images
Name          : %{crossmint}%{pkgname}
Version       : 0.2.8.4
Release       : 1
License       : LGPL-2.0-or-later
Group         : Development/Libraries

Packager      : %{packager}
URL           : https://wvware.sourceforge.net/libwmf.html

%rpmint_essential
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: make
BuildRequires: libpng
BuildRequires: %{crossmint}zlib-devel
BuildRequires: %{crossmint}freetype-devel >= 2.0.4
BuildRequires: %{crossmint}libxml2-devel
BuildRequires: %{crossmint}libpng-devel
Provides     : %{crossmint}libwmf-devel

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: https://nav.dl.sourceforge.net/project/wvware/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/libwmf/libwmf-config.patch

%rpmint_build_arch


%description
This is a library for interpreting metafile images and either displaying them
using X or converting them to standard formats such as PNG, JPEG, PS, EPS,...


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

# configure.ac & configure.in are both present.....
rm -f configure.in
autoreconf -fiv
rm -rf autom4te.cache

cp %{S:1} config.sub


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--without-expat
	--with-plot
	--with-layers
"
STACKSIZE="-Wl,-stack,128k"

for CPU in ${ALL_CPUS}
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	./configure ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}

	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/libwmf-config
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
%license COPYING
%doc README ChangeLog
%doc %{_isysroot}%{_rpmint_target_prefix}/share/doc/libwmf/

%{_isysroot}%{_rpmint_target_prefix}/bin/libwmf-fontmap
%{_isysroot}%{_rpmint_target_prefix}/bin/wmf2*
%{_isysroot}%{_rpmint_target_prefix}/share/libwmf

%{_isysroot}%{_rpmint_target_prefix}/include/libwmf
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a


%changelog
* Sun Apr 02 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- updated to 0.2.8.4

* Tue Nov 06 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.2.2

* Tue Jul 10 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.2.0

* Sat Dec 23 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
