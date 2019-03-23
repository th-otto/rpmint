Summary: 	Interface for MPEG-1 Streams.
Name: 		mpeg_lib
Version: 	1.3.1
Release: 	1
License: 	BSD
Group: 		System/Libraries
Packager: 	Keith Scroggins <kws@radix.net>
Vendor:		Sparemint
Source: 	%{name}-%{version}.tar.gz
Patch0:		mpeg_lib-1.3.1-mint.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
URL: 		http://starship.python.net/~gward/mpeglib/

%description
The MPEG Library is a C library for decoding MPEG-1 video streams and dithering 
them to a variety of colour schemes. Most of the code in the library comes 
directly from an old version of the Berkeley MPEG player (mpeg_play), an 
X11-specific implementation that worked fine, but suffered from minimal 
documentation and a lack of modularity. 

%prep
%setup -q
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=$RPM_BUILD_ROOT/usr
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/lib/lib*.a
/usr/include

%changelog
* Thu Dec 11 2003 Keith Scroggins <kws@radix.net>
- Initial build of mpeg_lib 1.3.1 for MiNT
