Summary: Browser program for the File Transfer Protocol
Name: ncftp
Version: 3.1.5
Release: 1
Group: Applications/Networking
Copyright: Artistic
Url: http://www.ncftp.com/
Source0: ftp://ftp.ncftp.com/ncftp/ncftp-%{version}-src.tar.gz
Source1: ncftp.wmconfig
BuildRoot: /var/tmp/%{name}-root
Vendor: Sparemint
Prefix: /usr
BuildRoot: /var/tmp/ncftp-root
Packager: Martin Tarenskeen <m.tarenskeen@zonnet.nl>

%description
NcFTP is a ftp client with many advantages over the standard one. It
includes command line editing, command histories, support for recursive
gets, automatic logins, background downloading and much more.


%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr
make


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
make install prefix=$RPM_BUILD_ROOT/usr mandir=$RPM_BUILD_ROOT/usr/man
stack -S 128k $RPM_BUILD_ROOT/usr/bin/*

gzip $RPM_BUILD_ROOT/usr/man/man1/*.1

mkdir -p $RPM_BUILD_ROOT/etc/X11/wmconfig
install -m644 $RPM_SOURCE_DIR/ncftp.wmconfig $RPM_BUILD_ROOT/etc/X11/wmconfig/ncftp

%files
%defattr(-,root,root)
%doc README.txt doc/[A-Z]*.txt
/usr/bin/*
/usr/man/man1/*


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jun 25 2003 Martin Tarenskeen <m.tarenskeen@zonnet.nl> 
- updated to 3.1.5

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
