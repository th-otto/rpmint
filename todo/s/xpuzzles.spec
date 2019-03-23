Summary       : Geometric puzzles and toys for the X Window System.
Name          : xpuzzles
Version       : 5.5.2
Release       : 1
Copyright     : MIT
Group         : X11/Games

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://sunsite.unc.edu/pub/Linux/games/strategy/

BuildRequires : XFree86-devel
Requires      : XFree86

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://sunsite.unc.edu/pub/Linux/games/strategy/%{name}-%{version}.tar.gz
Patch0: xpuzzles-5.4.1-install.patch
Patch1: xpuzzles-5.4.1-nobr.patch
Patch2: xpuzzles-5.5.2-usleep.patch


%description
A set of geometric puzzles and toys for the X Window System.  Xpuzzles
includes a version of Rubik's cube and various other geometric Rubik's
cube style puzzles.


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .nobr
%patch2 -p1 -b .usleep


%build
make -f xpuzzles.Makefile xmkmf
make -f xpuzzles.Makefile


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/X11R6/{bin,man/man1}

make -f xpuzzles.Makefile DESTDIR=${RPM_BUILD_ROOT} install

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/.directory <<EOF
[Desktop Entry]
Name=xpuzzles
Comment=Various Puzzles
Type=Directory
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xcubes.desktop <<EOF
[Desktop Entry]
Name=xcubes
Type=Application
Exec=xcubes
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xdino.desktop <<EOF
[Desktop Entry]
Name=xdino
Type=Application
Exec=xdino
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xhexagons.desktop <<EOF
[Desktop Entry]
Name=xhexagons
Type=Application
Exec=xhexagons
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xmball.desktop <<EOF
[Desktop Entry]
Name=xmball
Type=Application
Exec=xmball
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xmlink.desktop <<EOF
[Desktop Entry]
Name=xmlink
Type=Application
Exec=xmlink
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xoct.desktop <<EOF
[Desktop Entry]
Name=xoct
Type=Application
Exec=xoct
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xpanex.desktop <<EOF
[Desktop Entry]
Name=xpanex
Type=Application
Exec=xpanex
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xpyraminx.desktop <<EOF
[Desktop Entry]
Name=xpyraminx
Type=Application
Exec=xpyraminx
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xrubik.desktop <<EOF
[Desktop Entry]
Name=xrubik
Type=Application
Exec=xrubik
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xskewb.desktop <<EOF
[Desktop Entry]
Name=xskewb
Type=Application
Exec=xskewb
EOF

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Games/xpuzzles/xtriangles.desktop <<EOF
[Desktop Entry]
Name=xtriangles
Type=Application
Exec=xtriangles
EOF

strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%config /etc/X11/applnk/Games/xpuzzles/.directory
%config /etc/X11/applnk/Games/xpuzzles/xcubes.desktop
%config /etc/X11/applnk/Games/xpuzzles/xdino.desktop
%config /etc/X11/applnk/Games/xpuzzles/xhexagons.desktop
%config /etc/X11/applnk/Games/xpuzzles/xmball.desktop
%config /etc/X11/applnk/Games/xpuzzles/xmlink.desktop
%config /etc/X11/applnk/Games/xpuzzles/xoct.desktop
%config /etc/X11/applnk/Games/xpuzzles/xpanex.desktop
%config /etc/X11/applnk/Games/xpuzzles/xpyraminx.desktop
%config /etc/X11/applnk/Games/xpuzzles/xrubik.desktop
%config /etc/X11/applnk/Games/xpuzzles/xskewb.desktop
%config /etc/X11/applnk/Games/xpuzzles/xtriangles.desktop

%{_prefix}/X11R6/bin/xpanex
%{_prefix}/X11R6/man/man1/xpanex.1*
%{_prefix}/X11R6/bin/xrubik
%{_prefix}/X11R6/man/man1/xrubik.1*
%{_prefix}/X11R6/bin/xskewb
%{_prefix}/X11R6/man/man1/xskewb.1*
%{_prefix}/X11R6/bin/xdino
%{_prefix}/X11R6/man/man1/xdino.1*
%{_prefix}/X11R6/bin/xpyraminx
%{_prefix}/X11R6/man/man1/xpyraminx.1*
%{_prefix}/X11R6/bin/xoct
%{_prefix}/X11R6/man/man1/xoct.1*
%{_prefix}/X11R6/bin/xmball
%{_prefix}/X11R6/man/man1/xmball.1*
%{_prefix}/X11R6/bin/xcubes
%{_prefix}/X11R6/man/man1/xcubes.1*
%{_prefix}/X11R6/bin/xtriangles
%{_prefix}/X11R6/man/man1/xtriangles.1*
%{_prefix}/X11R6/bin/xhexagons
%{_prefix}/X11R6/man/man1/xhexagons.1*
%{_prefix}/X11R6/bin/xmlink
%{_prefix}/X11R6/man/man1/xmlink.1*


%changelog
* Fri Dec 29 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
