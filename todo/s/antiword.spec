Name: 		antiword
Summary: 	MS Word to ASCII/Postscript converter
Version: 	0.35
Release: 	1
Packager:	Keith Scroggins <kws@radix.net>
Vendor:		Sparemint
License: 	GPL 
Source: 	http://www.winfield.demon.nl/linux/%{name}-%{version}.tar.gz
URL: 		http://www.winfield.demon.nl/
Group: 		Applications/Text
BuildRoot: 	%{_tmppath}/%{name}-buildroot

%description 
Antiword is a free MS-Word reader for Unix systems. It converts documents
from Word 6, 7, 97, 2000 and 2002 to ASCII and Postscript.  Antiword tries
to keep the layout of the document intact.

%prep
%setup -q

%build
OPT="$RPM_OPT_FLAGS" make all 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -m 755 antiword %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a Resources/* %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_mandir}/man1
cp Docs/*.1 %{buildroot}%{_mandir}/man1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Docs/COPYING Docs/FAQ Docs/ReadMe Docs/Netscape
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/%{name}

%changelog
* Mon Feb 2 2004 Keith Scroggins <kws@radix.net> 
- Initial build of Antiword for MiNT
