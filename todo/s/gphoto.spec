%define ver	0.4.3
%define rel	1
%define prefix	/usr

Summary: gPhoto - the GNU Digital Still Camera Program
Name: gphoto        
Version: %ver
Release: %rel
Patch0: gphoto.mint.patch

Copyright: GPL
Group: Applications/Graphics
Packager: Marc-Anton Kehr <m.kehr@ndh.net>
Vendor: Sparemint
Source: ftp://ftp.gphoto.org/projects/gphoto/pub/tar/gphoto/stable/gphoto-%{ver}.tar.gz
BuildRoot: /var/tmp/gphoto-root
URL: http://www.gphoto.org/
Docdir: %{prefix}/doc
Requires: gtk+ >= 1.2.3
Requires: imlib-devel >= 1.9.4

%description
gPhoto is part of the GNU project - and is an universal, free
GTK+ application and library framework that lets you download
images from several different digital camera models, and from
the local harddrive, and generate HTML albums.

%prep
%setup -q
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix
make

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{prefix} install

#%post
#/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING FAQ MANUAL NEWS README THANKS THEMES ChangeLog
%{prefix}/man/man1/gphoto.1
%{prefix}/bin/*
%{prefix}/lib/*
%{prefix}/share/gphoto/doc/*
%{prefix}/share/gphoto/gallery/Default/*
%{prefix}/share/gphoto/gallery/RedNGray/*
%{prefix}/share/gphoto/gallery/CSStheme/*
%{prefix}/share/gnome/apps/Graphics/*

%changelog
* Sat Apr 14 2001 Marc-Anton Kehr <m.kehr@ndh.net>
- ported by Frank Naumann
- build against MiNTLib 0.56.1
