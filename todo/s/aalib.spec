Summary: 	An ASCII art library.
Name: 		aalib
Version: 	1.4.0
Release: 	1
Group: 		System Environment/Libraries
License: 	LGPL
Vendor: 	Sparemint
Packager:	Keith Scroggins <kws@radix.net>
URL: 		http://aa-project.sourceforge.net/aalib/
Source:		%{name}-%{version}.tar.gz
Buildroot: 	%{_tmppath}/%{name}-root
Requires: 	XFree86, ncurses, slang
BuildRequires: 	XFree86-devel, ncurses-devel, slang

%description
AA-lib is a low level graphics library that doesn't require a graphics
device and has no graphics output.  Instead AA-lib replaces those
old-fashioned output methods with a powerful ASCII-art renderer.  The
AA-Project is working on porting important software like DOOM and Quake
to work with AA-lib. If you'd like to help them with their efforts,
you'll also need to install the aalib-devel package.


%package devel
Summary: The static libraries and header files for AA-lib.
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
The aalib-devel package contains the static libraries and header files
for the AA-lib ASCII art library.  If you'd like to develop programs
using AA-lib, you'll need to install aalib-devel.


%prep
%setup -q 

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --with-x11 --with-slang --with-curses-driver=yes --with-ncurses --host=m68k-atari-mint --target=m68k-atari-mint --build=m68k-atari-mint
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc ANNOUNCE AUTHORS COPYING ChangeLog NEWS
/usr/bin/aafire
/usr/bin/aainfo
/usr/bin/aasavefont
/usr/bin/aatest
/usr/lib/*.a
/usr/info/*.info*
/usr/man/man1/*

%files devel
%defattr(-, root, root)
/usr/bin/aalib-config
/usr/lib/*.a
/usr/lib/*.la
/usr/include/*.h
/usr/share/aclocal/*.m4
/usr/man/man3/*

%changelog
* Wed Dec 10 2003 Keith Scroggins <kws@radix.net>
- Initial build of aalib for FreeMiNT
