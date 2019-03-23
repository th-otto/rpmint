Summary: Install Debian and Slackware Packages with rpm.
Name: alien
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Version: 6.56
Release: 1
Source: ftp://kitenet.net/pub/code/debian/alien_6.56.tar.gz
Copyright: GPL
Group: Utilities/File
Buildroot: /var/tmp/alien-6.56.build
Requires: perl

%description
Alien allows you to convert Debian, Slackware, and Stampede Packages into Red
Hat packages, which can be installed with rpm.

It can also convert into Slackware, Debian and Stampede packages.

This is a tool only suitable for binary packages.

%prep
%setup -n alien
rm -rf /var/tmp/alien-6.56.build || true

%install
make DESTDIR=$RPM_BUILD_ROOT install
chown -R 0.0 $RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -not -type d -printf "/%%P\n" > manifest

%files -f manifest
%doc CHANGES COPYING README alien.lsm
