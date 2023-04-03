%define pkgname xpuzzles

%rpmint_header

Summary       : Geometric puzzles and toys for the X Window System.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 5.5.2
Release       : 1
License       : MIT
Group         : X11/Games

URL           : ftp://sunsite.unc.edu/pub/Linux/games/strategy/

%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
Requires      : cross-mint-XFree86
%else
BuildRequires : XFree86-devel
Requires      : XFree86
%endif

Packager:       Thorsten Otto <admin@tho-otto.de>

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://sunsite.unc.edu/pub/Linux/games/strategy/%{pkgname}-%{version}.tar.gz
Patch0: patches/%{pkgname}/xpuzzles-5.4.1-install.patch
Patch2: patches/%{pkgname}/xpuzzles-5.5.2-usleep.patch

%rpmint_build_arch

%description
A set of geometric puzzles and toys for the X Window System.  Xpuzzles
includes a version of Rubik's cube and various other geometric Rubik's
cube style puzzles.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch2 -p1


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# That package does not have an Imakefile in the top directory :(
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

	make -f xpuzzles.Makefile XMKMF="%{_rpmint_target}-xmkmf -DCpuOption=${CPU_CFLAGS}" xmkmf
	make -f xpuzzles.Makefile
done


%install

make -f xpuzzles.Makefile DESTDIR=%{buildroot}%{_isysroot} install

mkdir -p %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/.directory <<EOF
[Desktop Entry]
Name=xpuzzles
Comment=Various Puzzles
Type=Directory
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xcubes.desktop <<EOF
[Desktop Entry]
Name=xcubes
Type=Application
Exec=xcubes
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xdino.desktop <<EOF
[Desktop Entry]
Name=xdino
Type=Application
Exec=xdino
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xhexagons.desktop <<EOF
[Desktop Entry]
Name=xhexagons
Type=Application
Exec=xhexagons
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xmball.desktop <<EOF
[Desktop Entry]
Name=xmball
Type=Application
Exec=xmball
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xmlink.desktop <<EOF
[Desktop Entry]
Name=xmlink
Type=Application
Exec=xmlink
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xoct.desktop <<EOF
[Desktop Entry]
Name=xoct
Type=Application
Exec=xoct
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xpanex.desktop <<EOF
[Desktop Entry]
Name=xpanex
Type=Application
Exec=xpanex
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xpyraminx.desktop <<EOF
[Desktop Entry]
Name=xpyraminx
Type=Application
Exec=xpyraminx
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xrubik.desktop <<EOF
[Desktop Entry]
Name=xrubik
Type=Application
Exec=xrubik
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xskewb.desktop <<EOF
[Desktop Entry]
Name=xskewb
Type=Application
Exec=xskewb
EOF

cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Games/xpuzzles/xtriangles.desktop <<EOF
[Desktop Entry]
Name=xtriangles
Type=Application
Exec=xtriangles
EOF

%{_rpmint_target}-strip %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:
%{_rpmint_target}-stack --fix=256k %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/*/*


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/.directory
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xcubes.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xdino.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xhexagons.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xmball.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xmlink.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xoct.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xpanex.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xpyraminx.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xrubik.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xskewb.desktop
%config %{_isysroot}/etc/X11/applnk/Games/xpuzzles/xtriangles.desktop

%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xpanex
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xpanex.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xrubik
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xrubik.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xskewb
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xskewb.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xdino
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xdino.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xpyraminx
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xpyraminx.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xoct
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xoct.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xmball
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xmball.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xcubes
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xcubes.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xtriangles
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xtriangles.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xhexagons
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xhexagons.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xmlink
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xmlink.1*


%changelog
* Tue Mar 21 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri Dec 29 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
