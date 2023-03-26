%define pkgname xv

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

%rpmint_header

Summary       : An X based image file viewer and manipulator.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 3.10a
Release       : 3
License       : Shareware
Group         : Applications/Graphics

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : http://www.trilon.com/xv/xv.html
# http://www.gregroelofs.com/greg_xv.html

%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
BuildRequires : cross-mint-libjpeg-devel
BuildRequires : cross-mint-libtiff-devel
BuildRequires : cross-mint-libpng-devel
BuildRequires : cross-mint-zlib-devel
Requires      : cross-mint-XFree86
%else
BuildRequires : XFree86-devel
BuildRequires : libjpeg-devel
BuildRequires : libtiff-devel
BuildRequires : libpng-devel
BuildRequires : zlib-devel
Requires      : XFree86
%endif

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.cis.upenn.edu/pub/xv/%{pkgname}-%{version}.tar.gz
Source1: ftp://swrinde.nde.swri.edu/pub/png/applications/%{pkgname}-%{version}-png-1.2d.tar.gz
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
Patch11: xv-png.patch

%rpmint_build_arch


%description
Xv is an image display and manipulation utility for the X Window
System.  Xv can display GIF, JPEG, TIFF, PBM, PPM, X11 bitmap, Utah
Raster Toolkit RLE, PDS/VICAR, Sun Rasterfile, BMP, PCX, IRIS RGB, XPM,
Targa, XWD, PostScript(TM) and PM format image files.  Xv is also
capable of image manipulation like cropping, expanding, taking
screenshots, etc.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

tar xvfz %{S:1}

patch -p1 --quiet < xvpng.diff
%patch0  -p1
%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch4  -p1
%patch5  -p1
%patch6  -p1
%patch7  -p1
%patch9  -p1
%patch10 -p1
%patch11 -p1


%build
%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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

	%{_rpmint_target}-xmkmf -DCpuOption="${CPU_CFLAGS}"
	cd tiff
	%{_rpmint_target}-xmkmf -DCpuOption="${CPU_CFLAGS}"
	cd ..
	make EXTRA_DEFINES="-D__GNU_LIBRARY__"

	# make clean
	# make -C tiff clean
	# rm -rf .xvpics
done


%install

make install DESTDIR=%{buildroot}
make install.man DESTDIR=%{buildroot}

%if "%{buildtype}" != "cross"
cp -pr %{buildroot}%{_rpmint_sysroot}/. %{buildroot}
rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%{_rpmint_target}-stack --fix=256k %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/*/*

mkdir -p %{buildroot}%{_isysroot}/etc/X11/applnk/Graphics
cat > %{buildroot}%{_isysroot}/etc/X11/applnk/Graphics/xv.desktop <<EOF
[Desktop Entry]
Name=xv
Comment=An X based image file viewer and manipulator.
Exec=xv
Terminal=0
Type=Application
EOF

( cd %{buildroot}%{_isysroot}
  mkdir -p ./etc/X11/wmconfig
  install -m644 %{S:2} ./etc/X11/wmconfig/xv
)


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README BUGS CHANGELOG IDEAS 
%doc docs/{bmp.doc,epsf.ps,gif.ack,gif.aspect,gif87.doc,gif89.doc}
%doc docs/{help,xpm.ps,vdcomp.man,penn.policy,xv.ann,xv.blurb}
%doc docs/xvdocs.ps
%config %{_isysroot}/etc/X11/applnk/Graphics/xv.desktop
%config %{_isysroot}/etc/X11/wmconfig/xv
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/bggen
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/vdcomp
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xcmap
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xv
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xvpictoppm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/*


%changelog
* Fri Mar 24 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
