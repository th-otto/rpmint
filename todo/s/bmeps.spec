# This .spec file lets you build RPMs for RedHat and other RPM-based
# distributions simply by issuing this command as root:
#   rpm -ta bmeps.tgz

Name:      bmeps
Version:   1.0.7
Release:   1
Summary:   converts bitmaps to EPS
License:   LGPL
URL:       http://www.ctan.org/tex-archive/support/bmeps
Source:    %{name}.tar.gz
Group:     Applications/Multimedia
Prefix:    %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Packager:  Martin Tarenskeen <m.tarenskeen@zonnet.nl>
Vendor:    Sparemint

%description
The bmeps package contains a library and a command line tool to convert PNG
and other images to EPS. It is intended to be used together with LaTeX
and dvips.

%prep
%setup -q -n %{name}

%build
CFLAGS="$RPM_OPT_FLAGS -m68020-60 -Wall" \
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix}
strip $RPM_BUILD_ROOT%{_bindir}/bmeps
stack -S 128k $RPM_BUILD_ROOT%{_bindir}/bmeps

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%doc COPYING DOCU/ README
%{_bindir}/bmeps

%changelog
* Wed Jun 18 2003 Dirk Krause <krause.dirk@web.de>
- version number changed for 1.0.7
* Wed Jan 22 2003 Guido Gonzato <guido.gonzato@univr.it>
- built initial .spec file for version 1.0.6
