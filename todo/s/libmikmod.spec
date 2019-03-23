# libmikmod rpm specification file
%define version	3.1.11
%define release	1
# Can't make a relocatable package since this would require patching
# libmikmod-config and I'm too lazy to create a sed command for that.
%define prefix /usr

Summary:	libmikmod sound library
Summary(de):	libmikmod Sound Library
Summary(fr):	Bibliothèque sonore libmikmod
Name:		libmikmod
Version:	%version
Release:	%release
Copyright:	LGPL
Group:		Libraries
URL:		http://mikmod.raphnet.net/
PreReq:		/sbin/install-info
Buildroot:	/tmp/build/libmikmod-%{PACKAGE_VERSION}
Packager:	Marc-Anton Kehr <makehr@ndh.net>
Vendor:		Sparemint

Source0:	http://mikmod.raphnet.net/files/libmikmod-%{PACKAGE_VERSION}.tar.gz

%description
A portable sound library for Unix, capable of playing samples as well as module
files, on a wide range of sound devices.

%description -l de
Eine portable Sound Library für Unix. Sie kann sowohl Samples als auch Module
auf verschiedensten Audio Devices abspielen.

%description -l fr
Une bibliothèque sonore portable pour Unix, capable de jouer aussi bien des
effets sonores que des modules, sur un grand choix de périphériques sonores.

%package devel
Summary:	Libraries and include files to develop libmikmod applications
Summary(fr):	Bibliothèques et includes pour programmer pour libmikmod
Group:		Libraries
Requires:	libmikmod

%description devel

%description devel -l fr

################################################################################

%prep
%setup

%build
./configure --prefix=%prefix
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{prefix} install
gzip -9nf $RPM_BUILD_ROOT%{prefix}/info/mikmod*

%post
#/sbin/ldconfig

%post devel
/sbin/install-info %{prefix}/info/mikmod.info %{prefix}/info/dir

#%postun -p /sbin/ldconfig

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING.LIB INSTALL NEWS PROBLEMS README TODO
#%{prefix}/lib/lib*.so.*

%files devel
%defattr(-, root, root)
%doc %{prefix}/info/mikmod*
%{prefix}/bin/libmikmod-config
#%{prefix}/lib/lib*.so
%{prefix}/lib/lib*a
%{prefix}/include/mikmod.h
%{prefix}/share/aclocal/*

%changelog
* Mon Apr 07 2008 Marc-Anton Kehr <makehr@ndh.net>
- new version

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
- added %description de and Summary(de)
