Summary: info to html converter
Name: info2html
Version: 1.1
Release: 1
Copyright: Unknown
Group: Utilities/System
URL: http://iamwww.unibe.ch/work/docs/info2html/info2html.html
Source: http://iamwww.unibe.ch/work/docs/info2html/info2html%{version}/info2html%{version}.tar.gz
Patch0: info2html.patch
Patch1: info2html-1.1-mint.patch
Packager: Frank Naumann <fnaumann@freemint.de>
Vendor: Sparemint
Requires: perl
Prefix: %{_prefix}
Docdir: %{_prefix}/doc
BuildRoot: %{_tmppath}/%{name}-root

%description
Convert info documentation files to html.

%prep
%setup -q -c
%patch0
%patch1 -p1

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT/etc
install -m 755 info2html $RPM_BUILD_ROOT%{_prefix}/bin
install -m 644 info2html.conf $RPM_BUILD_ROOT/etc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (755, root, root)
%{_prefix}/bin/info2html
%defattr (644, root, root)
%config /etc/info2html.conf

%changelog
* Fri Nov 24 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
