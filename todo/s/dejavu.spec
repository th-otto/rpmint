%define name	dejavu-fonts-ttf
%define version	2.31
%define release	1

Summary:		DejaVu Truetype Fonts
Group:		System/Fonts
Name:			%name
Version:		%version
Release:		%release
Source:		http://prdownloads.sourceforge.net/dejavu/dejavu-fonts-ttf-%{version}.tar.bz2
URL:			http://dejavu.sourceforge.net/
License:		Copyright Bitstream Inc, freely distributable
BuildRoot:	%{_tmppath}/build-%{name}-%{version}
Prefix:		%{_prefix}
Docdir:		%{_prefix}/share/doc
Provides:	dejavu-fonts-ttf = %{version}-%{release}
Provides:	dejavu-ttf = %{version}-%{release}
BuildArch:	noarch
Vendor:		Sparemint
Packager:	Ole Loots <ole@monochrom.net>

%description
The DejaVu fonts are a font family based on the Bitstream Vera Fonts.
Its purpose is to provide a wider range of characters while maintaining the
original look and feel through the process of collaborative development.

%prep
%setup -q 

%build

%install
mkdir -p "%{buildroot}%{_prefix}/share/fonts/truetype/ttf-dejavu/"
%__install -m 0644 ttf/* "%{buildroot}%{_prefix}/share/fonts/truetype/ttf-dejavu/"
ls "%{buildroot}%{_prefix}/share/fonts/truetype/ttf-dejavu/"


%clean
%__rm -rf "%{buildroot}"


%files
%defattr(-,root,root)
%doc AUTHORS BUGS LICENSE NEWS README *.txt
%{_prefix}/share/fonts/truetype/ttf-dejavu/*.ttf

%changelog
* Sat Jul 12 2010 Ole Loots <ole@monochrom.net> 2.26-0.pm.1
- Initial Sparemint release of DejaVu Truetype Fonts Version 2.31

