Summary       : An X based image file viewer and manipulator.
Name          : xv
Version       : 3.10a
Release       : 2
Copyright     : Shareware
Group         : Applications/Graphics

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.trilon.com/xv/xv.html

BuildRequires : XFree86-devel, libjpeg-devel, libpng, zlib-devel
Requires      : XFree86

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.cis.upenn.edu/pub/xv/%{name}-%{version}.tar.gz
Source1: ftp://swrinde.nde.swri.edu/pub/png/applications/%{name}-%{version}-png-1.2d.tar.gz
Source2: xv.wmconfig
Patch0:  xv-3.10a-linux.patch
Patch1:  xv-3.10a-jpeg.patch
Patch2:  xv-3.10a-glibc.patch
Patch3:  xv-3.10a-grabpatch
Patch4:  xv-3.10a-deepcolor.patch
Patch5:  xv-3.10a-gifpatch
Patch6:  xv-3.10a-longname.patch
Patch7:  xv-3.10a-pdf.patch
Patch9:  xv-3.10a-tiff.patch
Patch10: xv-3.10a-syslibs.patch


%description
Xv is an image display and manipulation utility for the X Window
System.  Xv can display GIF, JPEG, TIFF, PBM, PPM, X11 bitmap, Utah
Raster Toolkit RLE, PDS/VICAR, Sun Rasterfile, BMP, PCX, IRIS RGB, XPM,
Targa, XWD, PostScript(TM) and PM format image files.  Xv is also
capable of image manipulation like cropping, expanding, taking
screenshots, etc.


%prep
%setup -q
cd ${RPM_BUILD_DIR}/%{name}-%{version}
tar xvfz ${RPM_SOURCE_DIR}/%{name}-%{version}-png-1.2d.tar.gz
patch -p1 --quiet < xvpng.diff
%patch0  -p1 -b .linux
%patch1  -p1 -b .jpegpatc
%patch2  -p1 -b .glibc
%patch3  -p1 -b .grab
%patch4  -p1 -b .deepcolor
%patch5  -p1 -b .gifpatch
%patch6  -p1 -b .longname
%patch7  -p1 -b .pdfpatch
%patch9  -p1 -b .tiffpatch
%patch10 -p1 -b .syslibs


%build
xmkmf
cd tiff; xmkmf; cd ..
make EXTRA_DEFINES="-D__GNU_LIBRARY__"


%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=${RPM_BUILD_ROOT}
make install.man DESTDIR=${RPM_BUILD_ROOT}

strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/*/*

mkdir -p ${RPM_BUILD_ROOT}/etc/X11/applnk/Graphics
cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Graphics/xv.desktop <<EOF
[Desktop Entry]
Name=xv
Comment=An X based image file viewer and manipulator.
Exec=xv
Terminal=0
Type=Application
EOF

( cd ${RPM_BUILD_ROOT}
  mkdir -p ./etc/X11/wmconfig
  install -m644 ${RPM_SOURCE_DIR}/xv.wmconfig ./etc/X11/wmconfig/xv
)


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README BUGS CHANGELOG IDEAS 
%doc docs/{bmp.doc,epsf.ps,gif.ack,gif.aspect,gif87.doc,gif89.doc}
%doc docs/{help,xpm.ps,vdcomp.man,penn.policy,xv.ann,xv.blurb}
%doc docs/xvdocs.ps
%config /etc/X11/applnk/Graphics/xv.desktop
%config /etc/X11/wmconfig/xv
%{_prefix}/X11R6/bin/bggen
%{_prefix}/X11R6/bin/vdcomp
%{_prefix}/X11R6/bin/xcmap
%{_prefix}/X11R6/bin/xv
%{_prefix}/X11R6/bin/xvpictoppm
%{_prefix}/X11R6/man/man1/bggen.1x*
%{_prefix}/X11R6/man/man1/vdcomp.1x*
%{_prefix}/X11R6/man/man1/xcmap.1x*
%{_prefix}/X11R6/man/man1/xv.1x*
%{_prefix}/X11R6/man/man1/xvpictoppm.1x*


%changelog
* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
