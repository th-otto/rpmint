%define pkgname fltk

%rpmint_header

Summary       : C++ GUI Toolkit for the X Window System, OpenGL, and WIN32
Name          : %{crossmint}%{pkgname}
Version       : 1.3.9
Release       : 1
License       : Development/Libraries/X11
Group         : Development/Libraries/X11

%rpmint_essential
BuildRequires : autoconf
BuildRequires : automake
BuildRequires : make
BuildRequires : %{crossmint}XFree86-devel
Requires      : %{crossmint}XFree86
Provides      : %{pkgname}-devel = %{version}

Packager      : %{packager}
URL           : https://www.fltk.org/
VCS           : https://github.com/fltk/fltk

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot     : %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/%{pkgname}/fltk-mint.patch

%rpmint_build_arch


%description
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a cross-platform C++ GUI toolkit for
for the X Window System), Microsoft&#x00AE; Windows&#x00AE;, and macOS&#x00AE;.
FLTK provides modern GUI functionality without the bloat and
supports 3D graphics via OpenGL&#x00AE; and its built-in GLUT
emulation. It was originally developed by Mr. Bill Spitzak
and is currently maintained by a small group of developers
across the world with a central repository on GitHub.

Note: You'll need theX11-Libaries to
compile FLTK applications for Atari, and a X-Server to run them.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

autoconf --force || exit 1
automake --force --copy --add-missing || :
rm -rf autom4te.cache

cp "%{S:1}" config.sub

%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--disable-threads
	--disable-localpng
	--disable-localzlib
	--disable-largefile
	--disable-test
	--disable-xdbe
"

export prefix=%{_rpmint_target_prefix}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	make V=1 %{?_smp_mflags} || exit 1

	make DESTDIR="%{buildroot}%{_rpmint_sysroot}" install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs

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
%license COPYING
%doc README* CHANGES* CREDITS KNOWN_BUGS.html
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*


%changelog
* Sat Dec 23 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file for 1.3.9
