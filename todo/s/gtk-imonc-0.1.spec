Summary: GTK-Imonc - GTK+ based imond client for MiNT
Name: gtk-imonc
Version: 0.1
Release: 1


Copyright: distributable
Group: Applications/Internet
Packager: Marc-Anton Kehr <m.kehr@ndh.net>
Vendor: Sparemint
Source0: http://userpage.fu-berlin.de/~zeank/gtk-imonc/gtk-imonc-%{version}.tar.gz
Buildroot: /var/tmp/gtk-imonc-%{version}


%description
GTK Client for fli4l router


%prep
%setup


%build
./configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
#mkdir -p $RPM_BUILD_ROOT/usr/bin
#mkdir -p $RPM_BUILD_ROOT/usr/share/gtk-imonc
#mkdir -p $RPM_BUILD_ROOT/usr/share/gtk-imonc/pixmaps
#mkdir -p $RPM_BUILD_ROOT/usr/doc

make prefix=$RPM_BUILD_ROOT/usr localedir=$RPM_BUILD_ROOT/usr/share/locale install
strip $RPM_BUILD_ROOT/usr/bin/gtk-imonc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL LIESMICH NEWS README TODO
/usr/bin/gtk-imonc
/usr/share/locale/de/LC_MESSAGES/gtk-imonc.mo
/usr/share/gtk-imonc/pixmaps/fli4l.xpm
/usr/share/gtk-imonc/pixmaps/offline.xpm
/usr/share/gtk-imonc/pixmaps/online.xpm

%changelog
* Thu Sep 21 2001 Marc-Anton Kehr <m.kehr@ndh.net>
- build against MiNTLib 0.57.2

