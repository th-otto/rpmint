%define pkgname XServer

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary       : The FreeMiNT X11 server for GEM
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 0.14
Release       : 1
License       : GPL-2.0-or-later
Group         : User Interface/X

Packager      : Ralph Lowinski <AltF4@freemint.de>
URL           : http://X11.freemint.de/

Requires      : /bin/sh

%rpmint_essential
BuildRequires : make

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{pkgname}-%{version}.tar.xz

%rpmint_build_arch


%description
This is the FreeMiNT X11 server for GEM. It runs as GEM application
and accepts X11 client requests from the local or a remote machines.

This is still a beta version. The XServer is under development and
not completly finished (especially the often requested Netscape
don't run properly yet).

Please read the README, especially the font handling possibly needs
some adjustment.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

cd src

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 020
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	make CROSS_TOOL=%{_rpmint_target} V=1 CPU="${CPU_CFLAGS}"
done


%install
mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin
mkdir -p %{buildroot}%{_isysroot}/etc/X11

install -m 755 src/X.app         %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/
install -m 644 src/Xapp.rsc      %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/
ln      -fs    X.app             %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/XServer

install -m 644 Xmodmap.EXMPL     %{buildroot}%{_isysroot}/etc/X11/Xmodmap
install -m 644 fonts.alias.EXMPL %{buildroot}%{_isysroot}/etc/X11/fonts.alias


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if "%{buildtype}" != "cross"
%pre
mkdir -p /var/lib/Xapp
%endif


%files
%defattr(-,root,root)
%doc ChangeLog* README *.EXMPL
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/*
%config(noreplace) %{_isysroot}/etc/X11/*


%changelog
* Sat Mar 25 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri Sep 21 2001  Ralph Lowinski <AltF4@freemint.de
- if the server can't load its RSC file the normal way, it also searches in
  /usr/X11/bin/ now.
- heaviely reworked handling of output stream buffer to avoid crashes due to
  buffer overflows, especially in GetImage and ListFonts request.
- speeded up Get/PutImage request for color depth >= 16bit.
- corrected drawing of window decor (border).
- some internal code tidy ups.
