Name: urlview
%define version 0.7
Version: %{version}
Release: 1
Copyright: GPL
Group: Applications/Internet
Source: ftp://ftp.cs.hmc.edu/pub/me/urlview-0.7.tar.gz
Patch0: urlview-sparemint.patch
Requires: webclient
Buildroot: /var/tmp/urlview-root
Summary: A URL extractor/viewer for use with Mutt.
Summary(de): Ein URL-Finder/-Betrachter fÅr Mutt.
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint

%description
urlview extracts URLs from a given text file, and presents a menu
of URLs to view using a user specified command.

%description -l de
Urlview extrahiert URLs aus einer Text-Datei und prÑsentiert ein MenÅ
der gefundenen URLs, um diese mit einem benutzerdefinierten Kommando
zu betrachten.

%prep
%setup -q
%patch -p1 -b .sparemint

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man1}
make prefix=$RPM_BUILD_ROOT/usr install
install -m755 url_handler.sh $RPM_BUILD_ROOT/usr/bin/url_handler.sh
strip $RPM_BUILD_ROOT/usr/bin/urlview
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING
%doc INSTALL README sample.urlview 
%doc urlview.sgml
/usr/bin/urlview
/usr/bin/url_handler.sh
/usr/man/man1/urlview.1.gz
