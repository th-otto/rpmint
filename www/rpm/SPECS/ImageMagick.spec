%define pkgname ImageMagick

%rpmint_header

Summary       : An X application for displaying and manipulating images
Name          : %{crossmint}%{pkgname}
Version       : 5.3.6
Release       : 1
License       : ImageMagick
Group         : Applications/Multimedia

Packager      : %{packager}
URL           : http://www.imagemagick.org/

%rpmint_essential
BuildRequires : %{crossmint}bzip2-devel >= 1.0.1
BuildRequires : %{crossmint}freetype-devel >= 2.0.2
BuildRequires : %{crossmint}libjpeg-devel
BuildRequires : %{crossmint}libpng-devel
BuildRequires : %{crossmint}libtiff-devel
BuildRequires : %{crossmint}libgif-devel
BuildRequires : %{crossmint}zlib-devel
BuildRequires : %{crossmint}XFree86-devel
BuildRequires : %{crossmint}libwmf-devel
BuildRequires : %{crossmint}libxml2-devel >= 2.0
Requires      : bzip2
Requires      : freetype
Requires      : libjpeg
Requires      : libtiff
Requires      : zlib

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: https://github.com/ImageMagick/ImageMagick/archive/refs/tags/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0: ImageMagick-libpath.patch
Patch1: ImageMagick-perlpaths.patch
Patch2: ImageMagick-libwmf.patch
Patch3: ImageMagick-perl-link.patch
Patch4: ImageMagick-DESTDIR.patch
Patch5: ImageMagick-config.patch
Patch6: ImageMagick-png.patch

%rpmint_build_arch


%description
ImageMagick(TM) is an image display and manipulation tool for the X 
Window System.  ImageMagick can read and write JPEG, TIFF, PNM, GIF
and Photo CD image formats.  It can resize, rotate, sharpen, color 
reduce or add special effects to an image, and when finished you can 
either save the completed work in the original format or a different 
one.  ImageMagick also includes command line programs for creating 
animated or transparent .gifs, creating composite images, creating 
thumbnail images, and more.  

ImageMagick is one of your choices if you need a program to manipulate 
and display images. If you'd also like to develop your own applications 
which use ImageMagick code or APIs, you'll need to install 
ImageMagick-devel as well.

%package devel
Summary       : Static libraries and header files for ImageMagick app development.
Group         : Development/Libraries
Requires      : %{name} = %{version}

%description devel
Image-Magick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications.  ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code
or APIs, you'll need to install ImageMagick-devel as well as ImageMagick.
You don't need to install it if you just want to use ImageMagick, 
however.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup  -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

rm -f aclocal.m4 ltmain.sh ltconfig
libtoolize --force --automake
aclocal
autoconf
autoheader
automake --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub



%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix}/X11R6 ${CONFIGURE_FLAGS_AMIGAOS}
	--includedir=%{_rpmint_target_prefix}/X11R6/include/magick
	--enable-lzw
	--with-ttf
	--with-x
	--with-magick_plus_plus
	--without-perl
	--without-threads
"
STACKSIZE=-Wl,-stack,256k

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	lt_cv_sys_max_cmd_len=50000 \
	LIBS="-liconv" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make %{?_smp_mflags} -C Magick++
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	if test "$multilibdir" != ""; then
		rm %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib$multilibdir/ImageMagick/delegates.mgk
		rm %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib$multilibdir/ImageMagick/fonts.mgk
		rm %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib$multilibdir/ImageMagick/modules/coders/modules.mgk
		rmdir %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib$multilibdir/ImageMagick/modules/coders/
		rmdir %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib$multilibdir/ImageMagick/modules/
		rmdir %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib$multilibdir/ImageMagick/
	fi

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
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
%license Copyright.txt
%doc ImageMagick.html README.txt TODO.txt QuickStart.txt
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/*
#%%{_isysroot}%%{_rpmint_target_prefix}/lib/perl*/site_perl/*/*/auto/Image
#%%{_isysroot}%%{_rpmint_target_prefix}/lib/perl*/site_perl/*/*/Image
%{_isysroot}%{_rpmint_target_prefix}/X11R6/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/share/%{pkgname}/*


%files devel
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/magick
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/Magick++.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/Magick++/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/ImageMagick
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/*/*.a


%changelog
* Mon Apr 03 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Thu Jul 19 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 5.3.6

* Wed Dec 27 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
