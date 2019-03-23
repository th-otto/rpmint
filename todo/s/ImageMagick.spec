Summary       : An X application for displaying and manipulating images.
Name          : ImageMagick
Version       : 5.3.6
Release       : 1
Copyright     : Freeware
Group         : Applications/Multimedia

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.imagemagick.org/

BuildRequires : bzip2-devel >= 1.0.1, freetype-devel >= 2.0.2-2, libjpeg-devel,
BuildRequires : libpng, libtiff-devel, libungif-devel, zlib-devel, XFree86-devel
BuildRequires : libwmf, perl >= 5.6.0, libxml2-devel >= 2.0
Requires      : bzip2, freetype, libjpeg, libtiff, zlib
#Requires     : libungif, libpng

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.simplesystems.org/pub/ImageMagick/ImageMagick-%{version}.tar.gz
Patch0: ImageMagick-libpath.patch
Patch1: ImageMagick-perlpaths.patch
Patch2: ImageMagick-libwmf.patch
Patch3: ImageMagick-perl-link.patch
Patch4: ImageMagick-DESTDIR.patch


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
Requires      : ImageMagick = %{version}

%description devel
Image-Magick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications.  ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code
or APIs, you'll need to install ImageMagick-devel as well as ImageMagick.
You don't need to install it if you just want to use ImageMagick, 
however.


%prep
%setup  -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1

# fix typo
perl -pi -e 's@htmlc\.@html.c@' coders/Makefile.am
# fix lcms.h include path
perl -pi -e 's@lcms/lcms\.h@lcms.h@' magick/transform.c

autoconf


%build
lt_cv_sys_max_cmd_len=50000 \
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
CXXFLAGS="${RPM_OPT_FLAGS} -O -D_GNU_SOURCE" \
LIBS="-liconv -lsocket" \
./configure \
	--prefix=%{_prefix}/X11R6 \
	--includedir=%{_prefix}/X11R6/include/magick \
	--with-perl \
	--with-ttf \
	--with-x \
	--with-magick_plus_plus \
	--without-perl \
	--without-threads
make
make -C Magick++


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	PREFIX=${RPM_BUILD_ROOT}%{_prefix}/X11R6 \
	prefix=${RPM_BUILD_ROOT}%{_prefix}/X11R6 \
	includedir=${RPM_BUILD_ROOT}%{_prefix}/X11R6/include/magick	

strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files
%defattr(-,root,root)
%doc www images
%doc ImageMagick.html Copyright.txt README.txt TODO.txt
%{_prefix}/X11R6/bin/*
#%{_prefix}/lib/perl*/site_perl/*/*/auto/Image
#%{_prefix}/lib/perl*/site_perl/*/*/Image
%{_prefix}/X11R6/man/*/*
%{_prefix}/X11R6/share/*


%files devel
%defattr(-,root,root)
%{_prefix}/X11R6/include/magick
%{_prefix}/X11R6/lib/ImageMagick
%{_prefix}/X11R6/lib/lib*a


%changelog
* Thu Jul 19 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 5.3.6

* Wed Dec 27 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
