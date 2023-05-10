%define pkgname x3270

%rpmint_header

Summary:        A Family of IBM 3270 Terminal Emulators
Name:           %{crossmint}%{pkgname}
Version:        4.2ga9
Release:        1
License:        MIT
Group:          System/X11/Terminals

URL:            https://x3270.miraheze.org
VCS:            https://github.com/pmattes/x3270
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        https://download.sourceforge.net/x3270/x3270-%{version}.tar.xz
Source1:        patches/automake/mintelf-config.sub

Patch0:         patches/%{pkgname}/x3270-mknod.patch
Patch1:         patches/%{pkgname}/x3270-usr_local_bin.patch
Patch2:         patches/%{pkgname}/x3270-mint.patch


%rpmint_essential
BuildRequires:  make
BuildRequires:  %{crossmint}XFree86-devel
BuildRequires:  pkgconfig(%{crossmint}openssl)
BuildRequires:  %{crossmint}readline
Requires:       %{crossmint}XFree86

%rpmint_build_arch

%description
This package contains a family of IBM 3270 mainframe terminal
emulators:

* terminal emulators for interactive use x3270	X Window System
   c3270  curses based

* terminal emulators for scripted use s3270    see the x3270-script
   man page tcl3270  Tcl based

* printer emulator pr3287

x3270 is an IBM 3270 terminal emulator for the X Window System.  x3270
runs over a telnet connection (with or without TN3270E) and emulates
either an IBM 3279 (color) or 3278 (monochrome).  It supports APL2
characters, IND$FILE file transfer, NVT mode, a pop-up keypad for
3270-specific keys, alternative keymaps, 3287 printer sessions, and a
scrollbar and has extensive debugging and scripting facilities.

x3270a is a script that computes the correct font sizes for
higher-resolution displays, then runs x3270.
(x3270 handles scaling of visual elements automatically,
but it cannot adjust the font sizes by itself.)

b3270 is a generic back-end for 3270 emulators.
It implements the 3270 protocol and host input/output,
and communicates with a front end application using a simple XML-based protocol.

c3270 is the curses-based version of x3270.  It runs on any dumb
terminal (an xterm or a console, for example), and supports (almost)
all of the x3270 features.  c3270 scripts are compatible with x3270
scripts, and the subset of command line options and resource
definitions are also compatible.

s3270 is a scripting-only version of x3270.  This program is intended
primarily for writing "screen-scraping" applications, for example a CGI
back-end script that retrieves database information from a mainframe.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--enable-c3270
	--enable-x3270
	--enable-s3270
	--enable-b3270
"
STACKSIZE="-Wl,-stack,512k"
export LIBX3270DIR=/etc/x3270

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 000
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	LIBS="-lSM -lICE -lXpm -lXext -lX11" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags} LIBX3270DIR=${LIBX3270DIR}

	make DESTDIR=%{buildroot}%{_rpmint_sysroot} LIBX3270DIR=${LIBX3270DIR} install
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} LIBX3270DIR=${LIBX3270DIR} install.man

	# make install does a mkfontdir, that creates a fonts.dir we don't
	# want in the package.  remove that:
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/fonts/X11/misc/fonts.dir

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make clean
	rm -rf obj
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_isysroot}/etc/x3270/ibm_hosts
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share


%changelog
* Wed May 10 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
