%define pkgname xpaint

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary       : An X Window System image editing or paint program.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 2.4.9
Release       : 2
License       : MIT
Group         : Applications/Graphics

%rpmint_essential
%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
BuildRequires : cross-mint-libpng-devel
BuildRequires : cross-mint-libtiff-devel
BuildRequires : cross-mint-libjpeg-devel
Requires      : cross-mint-XFree86
%else
BuildRequires : XFree86-devel
BuildRequires : libpng-devel
BuildRequires : libtiff-devel
BuildRequires : libjpeg-devel
Requires      : XFree86
%endif

Prefix        : %{_prefix}
Docdir        : %{_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://sunsite.unc.edu/pub/Linux/apps/graphics/draw/%{pkgname}-%{version}.tar.gz
Patch0: patches/%{pkgname}/xpaint-2.4.7-config.patch
Patch1: patches/%{pkgname}/xpaint-2.4.7-glibc.patch
Patch2: patches/%{pkgname}/xpaint-png.patch

%rpmint_build_arch

%description
XPaint is an X Window System color image editing program which
supports most standard paint program options.  XPaint also supports
advanced features like image processing algorithms.  XPaint allows you
to edit multiple images simultaneously and supports a variety of image
formats, including PPM, XBM, TIFF, JPEG, etc.

Install the xpaint package if you need a paint program for X.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n xpaint
%patch0 -p1
%patch1 -p1
%patch2 -p1


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
	make Makefiles
	make
done


%install

make install DESTDIR=%{buildroot}
make install.man DESTDIR=%{buildroot}

# fix symlink
rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/app-defaults
# ln -s ../../../../etc/X11/app-defaults %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/app-defaults

%if "%{buildtype}" != "cross"
cp -pr %{buildroot}%{_rpmint_sysroot}/. %{buildroot}
rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%{_rpmint_target}-strip %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:
%{_rpmint_target}-stack --fix=256k %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/*/*

( cd %{buildroot}%{_isysroot}
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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ChangeLog README README.PNG TODO Doc
%config %{_isysroot}/etc/X11/applnk/Graphics/xpaint.desktop
%config %{_isysroot}/etc/X11/app-defaults/XPaint
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xpaint
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xpaint.1x*


%changelog
* Tue Mar 21 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
