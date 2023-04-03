%define pkgname aalib

%rpmint_header

Summary: 	An ASCII art library.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version: 	1.4.0
Release: 	2
Group: 		System Environment/Libraries
License: 	LGPL-2.0-or-later

Packager:	Keith Scroggins <kws@radix.net>
URL: 		http://aa-project.sourceforge.net/aalib/

Source0:	%{pkgname}-%{version}.tar.gz
Source1:        patches/automake/mintelf-config.sub
Patch0:         patches/aalib/aalib-config.patch

Buildroot: 	%{_tmppath}/%{name}-root

%rpmint_essential
%if "%{buildtype}" == "cross"
BuildRequires: 	cross-mint-XFree86-devel
BuildRequires: 	cross-mint-ncurses-devel
BuildRequires: 	cross-mint-slang
Requires: 	cross-mint-XFree86
Requires: 	cross-mint-ncurses
Requires: 	cross-mint-slang
%else
BuildRequires: 	XFree86-devel
BuildRequires: 	ncurses-devel
BuildRequires: 	slang
Requires: 	XFree86
Requires: 	ncurses
Requires: 	slang
%endif

%rpmint_build_arch


%description
AA-lib is a low level graphics library that doesn't require a graphics
device and has no graphics output.  Instead AA-lib replaces those
old-fashioned output methods with a powerful ASCII-art renderer.  The
AA-Project is working on porting important software like DOOM and Quake
to work with AA-lib. If you'd like to help them with their efforts,
you'll also need to install the aalib-devel package.


%package devel
Summary: The static libraries and header files for AA-lib.
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
The aalib-devel package contains the static libraries and header files
for the AA-lib ASCII art library.  If you'd like to develop programs
using AA-lib, you'll need to install aalib-devel.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

rm -f aclocal.m4 acinclude.m4 ltmain.sh ltconfig
rm -rf autom4te.cache
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache
rm -f config.sub
cp %{S:1} config.sub

%build

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--with-x11-driver
	--with-slang-driver
	--with-curses-driver=yes
	--with-ncurses
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	sed -i 's@-I/usr/include/ncurses@@' config.status
	./config.status

	make # %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files for multilib
	%rpmint_remove_pkg_configs

	rm -f %{buildroot}%{_rpmint_bindir}/aalib-config

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
%doc ANNOUNCE AUTHORS COPYING ChangeLog NEWS
%{_isysroot}%{_rpmint_target_prefix}/bin/aafire
%{_isysroot}%{_rpmint_target_prefix}/bin/aainfo
%{_isysroot}%{_rpmint_target_prefix}/bin/aasavefont
%{_isysroot}%{_rpmint_target_prefix}/bin/aatest
%{_isysroot}%{_rpmint_target_prefix}/share/info/*.info*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/*

%files devel
%defattr(-, root, root)
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%{_isysroot}%{_rpmint_target_prefix}/include/*.h
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal/*.m4
%{_isysroot}%{_rpmint_target_prefix}/share/man/man3/*

%changelog
* Sun Mar 26 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Wed Dec 10 2003 Keith Scroggins <kws@radix.net>
- Initial build of aalib for FreeMiNT
