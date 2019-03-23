Summary: Utility to control digital cameras based on Sierra Imaging firmware 
Name: photopc
Version: 3.05dev4
Release: 2
Patch0: photopc-3.05-shell.patch
#Patch1: photopc-3.05dev4-mint.patch

Copyright: distributable
Group: Applications/File
Packager: Marc-Anton Kehr <m.kehr@ndh.net>
Vendor: Sparemint
Source0: ftp://ftp.average.com/pub/photopc/photopc-%{version}.tar.gz
Buildroot: /var/tmp/photopc-%{version}


%description
This is a command line tool to manipulate digital still cameras that use certain control protocol,
namely Agfa ePhoto line, Epson PhotoPC line, Olympus D-xxxL line, Sanyo and Nikon (at least CoolPix
900) cameras. It can set camera parameters, download and erase pictures, etc. It was originaly
developed for Epson PhotoPC 500, now the authos uses it with Olympus D-600L, results with other mod-
els may vary.

%prep
%setup
%patch0 -p1
#%patch1 -p1

%build
./configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install

mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1



install -m 755 photopc   $RPM_BUILD_ROOT/usr/bin/photopc
install -m 755 epinfo    $RPM_BUILD_ROOT/usr/bin/epinfo
install -m 644 photopc.1 $RPM_BUILD_ROOT/usr/share/man/man1/photopc.1
install -m 644 epinfo.1  $RPM_BUILD_ROOT/usr/share/man/man1/epinfo.1
install -m 755 photoshell $RPM_BUILD_ROOT/usr/bin/

gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man1/*.1
 
strip $RPM_BUILD_ROOT/usr/bin/photopc $RPM_BUILD_ROOT/usr/bin/epinfo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(0755,root,root)	/usr/bin/photopc
%attr(0755,root,root)	/usr/bin/epinfo
%attr(0755,root,root)	/usr/bin/photoshell
%attr(0644,root,root)	/usr/share/man/man1/photopc.1*
%attr(0644,root,root)	/usr/share/man/man1/epinfo.1*

%doc README usage.htm protocol.htm

%changelog
* Sun Feb 18 2001 Marc-Anton Kehr <m.kehr@ndh.net>
- build against MiNTLib 0.56
- added photoshell, a shellscript to control photopc

