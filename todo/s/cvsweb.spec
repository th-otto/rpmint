Summary: CGI script that allows Web-browsing of a CVS repository
Summary(de): CGI Skript das Web-Browsing des CVS Repositorys ermöglicht
Name: cvsweb
Version: 1.58
Release: 4
Copyright: BSD
Group: Development/Version Control
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Patch: cvsweb-redhat-paths.patch
Patch2: cvsweb-lastmod.patch
Patch3: cvsweb-footer.patch
Source: http://lemming.stud.fh-heilbronn.de/~zeller/download/%{name}.tar.gz
URL: http://linux.fh-heilbronn.de/~zeller/cgi/cvsweb.cgi/
BuildRoot: /tmp/%{name}-%{version}-%{release}-root
BuildArchitectures: noarch
Requires: perl >= 5, apache

%description
The cgi-script cvsweb.cgi is written by Bill Fenner <fenner@freebsd.org> 
for the freebsd project. It allows browsing of CVS repositories
with an HTML browser. 

This package contains the version of cvsweb script modified by
Henner Zeller <zeller@think.de>, Henrik Nordström <hno@hem.passagen.se>
and Alexey Nogin <nogin@cs.cornell.edu>

%description -l de
Das cgi-script cvsweb.cgi wurde von Bill Fenner <fenner@freevsd.org>
für das FreeBSD Projekt geschrieben. Es erlaubt das Browsen des CVS
Repositorys mit einem HTML Browser.

Dieses Paket enthält eine von Henner Zeller <zeller@think.de>, Henrik
Nordström <hno@hem.passagen.se> und Alexey Nogin <nogin@cs.cornell.edu>
modifizierte Version des cvsweb Skriptes.

%prep
%setup -n %{name}
%patch
%patch2
%patch3

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{home/httpd/cgi-bin,etc/httpd/conf}
install cvsweb.cgi $RPM_BUILD_ROOT/home/httpd/cgi-bin
install cvsweb.conf $RPM_BUILD_ROOT/etc/httpd/conf
chmod 444 TODO INSTALL README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(555,root,root) /home/httpd/cgi-bin/cvsweb.cgi
%attr(644,root,root) %config /etc/httpd/conf/cvsweb.conf
%defattr(-,root,root)
%doc TODO INSTALL README

%changelog
* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- correct Packager and Vendor
