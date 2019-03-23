Version: 	2.03
Release: 	1
Summary: 	Data compression library with very fast (de)compression
Name: 		lzo
Source0: 	http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz
License: 	GPLv2+
Group: 		System Environment/Libraries
URL: 		http://www.oberhumer.com/opensource/lzo/
Packager: 	Keith Scroggins <kws@radix.net>
Vendor: 	Sparemint
BuildRoot:  	/var/tmp/%{name}-%{version}-root

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.
This package contains development files needed for lzo.

%prep
%setup -q
%build 
CFLAGS="-O2 -fomit-frame-pointer" ./configure --prefix=/usr
make
#make check - all tests pass!
#make test - all tests pass!

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING THANKS NEWS doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%attr(0644,root,root) /usr/lib/lib*.a
%attr(0644,root,root) /usr/include/lzo/*

%changelog
* Thu May 14 2009 Keith Scroggins <kws@radix.net>
- Initial build of lzo RPM
