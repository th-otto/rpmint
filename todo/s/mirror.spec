Summary: Perl program to mirror FTP sites
Name: mirror
Version: 2.9
Release: 1
Copyright: distributable
Group: Applications/System
Source:  ftp://sunsite.org.uk/packages/mirror/mirror.tar.gz  
Url: http://sunsite.doc.ic.ac.uk/packages/mirror/
Patch: mirror-2.9-redhat.patch
BuildRoot: /var/tmp/mirror-root
BuildArchitectures: noarch
Vendor: Sparemint
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Requires: /bin/sh /usr/bin/perl
Summary(de): Perl-Programm zur Spiegelung von FTP-Servern

%description
Perl program to mirror FTP sites.

%description -l de
Perl-Programm zur Spiegelung von FTP-Servern.

%prep
%setup -q -c
%patch -p1 -b .redhat

%build 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/lib/mirror
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
%ifos freemint
make "PLDIR=$RPM_BUILD_ROOT/usr/lib/mirror" "BINDIR=$RPM_BUILD_ROOT/usr/bin" "MANDIR=$RPM_BUILD_ROOT/usr/man/man1" "GRP=wheel" install
%else
make "PLDIR=$RPM_BUILD_ROOT/usr/lib/mirror" "BINDIR=$RPM_BUILD_ROOT/usr/bin" "MANDIR=$RPM_BUILD_ROOT/usr/man/man1" install
%endif

install -m 644 mirror.defaults $RPM_BUILD_ROOT/etc

ln -sf mirror.pl $RPM_BUILD_ROOT/usr/bin/mirror

gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.txt *.html CHANGES*
%doc mirror.nightly support/cyber-patches support/lstest.pl
%config /etc/mirror.defaults
/usr/bin/do_unlinks.pl
/usr/bin/mirror
/usr/bin/mirror.pl
/usr/bin/mm.pl
/usr/bin/pkgs_to_mmin.pl
/usr/lib/mirror/dateconv.pl
/usr/lib/mirror/ftp.pl
/usr/lib/mirror/lchat.pl
/usr/lib/mirror/lsparse.pl
/usr/man/man1/*

%changelog
* Tue Sep 7 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Initial release.

