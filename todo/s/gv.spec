Summary       : A X front-end for the Ghostscript PostScript(TM) interpreter.
Name          : gv
Version       : 3.5.8
Release       : 2
Copyright     : GPL
Group         : Applications/Publishing

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://wwwthep.physik.uni-mainz.de/~plass/gv/

BuildRequires : XFree86-devel Xaw3d
Requires      : XFree86 ghostscript

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://thep.physik.uni-mainz.de/pub/gv/unix/gv-3.5.8.tar.gz
Patch0: gv-3.5.8-config.patch
Patch1: gv-3.5.8-alias.patch
Patch2: gv-3.5.8-mint.patch


%description
Gv is a user interface for the Ghostscript PostScript(TM) interpreter.
Gv can display PostScript and PDF documents on an X Window System.

Install the gv package if you'd like to view PostScript and PDF
documents on your system.  You'll also need to have the ghostscript
package and X installed.


%prep
%setup -q
%patch0 -p1 -b .config
%patch1 -p1 -b .alias
%patch2 -p1 -b .mint


%build
xmkmf
make Makefiles
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc/X11/applnk/Graphics

make DESTDIR=${RPM_BUILD_ROOT} install install.man
gunzip doc/*gz

cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Graphics/gv.desktop <<EOF
[Desktop Entry]
Name=Ghostview
Type=Application
Icon=kghostview.xpm
Exec=gv
EOF

ln -sf gv ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/ghostview

strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README CHANGES COPYING doc/*.html doc/*doc doc/*txt
%config /etc/X11/applnk/Graphics/gv.desktop
%config /etc/X11/app-defaults/GV
%{_prefix}/X11R6/bin/gv
%{_prefix}/X11R6/bin/ghostview
%{_prefix}/X11R6/lib/X11/gv
%{_prefix}/X11R6/man/man1/gv.*


%changelog
* Sat Dec 30 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
