Summary       : An image loading and rendering library for X11R6.
Name          : imlib
Version       : 1.9.8.1
Release       : 1
Copyright     : LGPL
Group         : System Environment/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.labs.redhat.com/imlib/

BuildRequires : libtiff-devel libjpeg-devel zlib-devel libungif-devel libpng
BuildRequires : netpbm-devel XFree86-devel gtk+ >= 1.2
Requires      : libtiff libjpeg zlib
#libungif libpng
Requires      : netpbm-progs XFree86 gtk+ >= 1.2

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.labs.redhat.com/pub/imlib/imlib-%{version}.tar.gz
Patch0: imlib-palfallback.patch


%description
Imlib is a display depth independent image loading and rendering library.
Imlib is designed to simplify and speed up the process of loading images
and obtaining X Window System drawables.  Imlib provides many simple
manipulation routines which can be used for common operations.  

Install imlib if you need an image loading and rendering library for
X11R6, or if you are installing GNOME.  You may also want to install
the imlib-cfgeditor package, which will help you configure Imlib.

%package devel
Summary       : Development tools for Imlib applications.
Group         : Development/Libraries
#Requires      : imlib = %{PACKAGE_VERSION}
Requires      : libtiff-devel libjpeg-devel zlib-devel libungif-devel libpng
Requires      : netpbm-devel XFree86-devel gtk+ >= 1.2

%description devel
The header files, static libraries and documentation needed for
developing Imlib applications.  Imlib is an image loading and
rendering library for X11R6.

Install the imlib-devel package if you want to develop Imlib
applications.  You will also need to install the imlib and
imlib_cfgeditor packages.

%package cfgeditor
Summary       : A configuration editor for the Imlib library.
Group         : System Environment/Libraries
#Requires      : imlib = %{PACKAGE_VERSION}

%description cfgeditor
The imlib-cfgeditor package contains the imlib_config program, which
you can use to configure the Imlib image loading and rendering
library.  Imlib_config can be used to control how Imlib uses color and
handles gamma corrections, etc.

If you're installing the imlib package, you should also install
imlib_cfgeditor.


%prep
%setup -q
%patch0 -p1


%build
automake
if [ ! -f configure ]; then
  CFLAGS="${RPM_OPT_FLAGS}" ./autogen.sh --prefix=%{_prefix} --sysconfdir=/etc
else
  CFLAGS="${RPM_OPT_FLAGS}" ./configure --prefix=%{_prefix} --sysconfdir=/etc
fi

make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make prefix=${RPM_BUILD_ROOT}%{_prefix} sysconfdir=${RPM_BUILD_ROOT}/etc install

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/imlib_config ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/imlib_config ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,root)
%doc README AUTHORS ChangeLog NEWS
%doc doc/*.gif doc/*.html
%config /etc/*
%{_prefix}/bin/imlib-config
%{_prefix}/lib/lib*.a
%{_prefix}/include/*
%{_prefix}/share/aclocal/*

%files cfgeditor
%defattr(-,root,root)
%{_prefix}/bin/imlib_config


%changelog
* Mon Dec 18 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
