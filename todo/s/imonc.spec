Summary: Client imonc for MiNT
Name: imonc
Version: 20010125
Release: 1
Group: Applications/Internet
License: distributable

Source: imonc-20010125.tar.gz
Patch0: imonc-20010125.mint.patch
Buildroot: /var/tmp/%{name}-root
Vendor: Sparemint
Packager: Marc-Anton Kehr <m.kehr@ndh.net>
Summary(de): ISDN Monitor fÅr fli4l Router


%description
isdn monitor for fli4l router

%prep
%setup 
%patch0 -p1

%build
make "RPM_OPT_FLAGS=$RPM_OPT_FLAGS"


%install

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m770 imonc $RPM_BUILD_ROOT/usr/bin
install -m770 mkfli4l $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(755,root,root)

/usr/bin/imonc
/usr/bin/mkfli4l

%doc readme 

%changelog
* Thu Sep 20 2001 Marc-Anton Kehr <m.kehr@ndh.net>
- first release for MiNT