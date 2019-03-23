%define __prefix	/usr

Name:		texi2html
Summary: 	TeXinfo to HTML converter
Version: 	1.64
Release:	1
Group: 		Applications/Text
Copyright: 	GPL
Source0: 	%{name}-%{version}.tar.gz
URL: 		http://texinfo.org/texi2html/
Packager:	Keith Scroggins <kws@radix.net>
Vendor:		Sparemint
BuildRoot: 	/var/tmp/%{name}-root
BuildRequires: 	perl
Prereq: 	/sbin/install-info

%description
'texi2html' converts texinfo documents to HTML.

Texinfo is the official documentation format of the GNU project. It
uses a single source file to produce both on-line information and
printed output. For more details about texinfo, see
http://www.texinfo.org. 

In contrast to the HTML produced by 'makeinfo --html' (the 'makeinfo'
program is part of the Texinfo distribution), the HTML output of
'texi2html' is highly configurable. Among others, with 'texi2html' you 
can customize your entire page layout (like headers, footers, style
sheets, etc), split documents at various levels and use 'latex2html' to
convert @tex sections.

'texi2html' should reasonably convert all Texinfo 4.0 constructs. If
not, please send a bug report to 'texi2html@mathematik.uni-kl.de'.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q

%build
./configure --prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/texi2html.info* %{_infodir}/dir.gz

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/texi2html.info* %{_infodir}/dir.gz
fi

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INTRODUCTION NEWS README TODO texi2html.html
/usr/bin/*
%{_infodir}/*.info*
%{_mandir}/man1/*

%changelog
* Fri Feb 5 2004 Keith Scroggins <kws@radix.net>
- Initial build for MiNT
