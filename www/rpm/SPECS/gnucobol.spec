%define pkgname gnucobol

%rpmint_header

Summary:        COBOL compiler
Name:           %{crossmint}%{pkgname}
Version:        3.0rc1
Release:        1
License:        GPL-3.0-or-later AND LGPL-3.0-or-later
Group:          Development/Languages/Other

Packager:       %{packager}
URL:            https://www.libsdl.org/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root


Source0: %{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

Patch0:  patches/gnucobol/gnucobol-CFLAGS.patch
Patch1:  patches/gnucobol/gnucobol-ltdl.patch

%rpmint_essential
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make

%rpmint_build_arch

%description
GnuCOBOL (formerly OpenCOBOL) is a COBOL compiler.
cobc translates COBOL to executable using intermediate C sources,
providing full access to nearly all C libraries.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

rm -f aclocal.m4 build_aux/ltmain.sh m4/lt* m4/libtool.m4
libtoolize --force 
aclocal -I m4
autoconf
autoheader
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} build_aux/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--disable-nls
	--without-dl
	--disable-shared
"
STACKSIZE="-Wl,-stack,128k"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'

	make HELP2MAN=true %{?_smp_mflags}
	make HELP2MAN=true DESTDIR="%{buildroot}%{_rpmint_sysroot}" install
	rm -f "%{buildroot}%{_rpmint_bindir}/sdl-config"

	if test -n "$multilibdir"; then
		mkdir -p "%{buildroot}%{_rpmint_libdir}$multilibdir"
		mv "%{buildroot}%{_rpmint_libdir}/"*.a "%{buildroot}%{_rpmint_libdir}$multilibdir"
	fi

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
%doc ABOUT-NLS README* NEWS THANKS TODO
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share



%changelog
* Sat Apr 08 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
