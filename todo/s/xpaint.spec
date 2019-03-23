Summary       : An X Window System image editing or paint program.
Name          : xpaint
Version       : 2.4.9
Release       : 1
Copyright     : MIT
Group         : Applications/Graphics

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

BuildRequires : XFree86-devel
Requires      : XFree86

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://sunsite.unc.edu/pub/Linux/apps/graphics/draw/%{name}-%{version}.tar.gz
Patch0: xpaint-2.4.7-config.patch
Patch1: xpaint-2.4.7-glibc.patch


%description
XPaint is an X Window System color image editing program which
supports most standard paint program options.  XPaint also supports
advanced features like image processing algorithms.  XPaint allows you
to edit multiple images simultaneously and supports a variety of image
formats, including PPM, XBM, TIFF, JPEG, etc.

Install the xpaint package if you need a paint program for X.


%prep
%setup -q -n xpaint
%patch0 -p1 -b .config
%patch1 -p1 -b .glibc


%build
xmkmf
make Makefiles
make


%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=${RPM_BUILD_ROOT}
make install.man DESTDIR=${RPM_BUILD_ROOT} MANDIR=%{_prefix}/X11R6/man/man1

strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/*/*

( cd ${RPM_BUILD_ROOT}
  mkdir -p ./etc/X11/applnk/Graphics
  cat > ./etc/X11/applnk/Graphics/xpaint.desktop <<EOF
[Desktop Entry]
Name=Paint
Name[sv]=Paint
Type=Application
Comment=simple painting program
Comment[sv]=simpelt ritprogram
Exec=xpaint
EOF
)


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc ChangeLog README README.PNG TODO Doc
%config(missingok) /etc/X11/applnk/Graphics/xpaint.desktop
%config /etc/X11/app-defaults/XPaint
%{_prefix}/X11R6/bin/xpaint
%{_prefix}/X11R6/man/man1/xpaint.1x*


%changelog
* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
