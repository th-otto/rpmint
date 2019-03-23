Summary: Utility to control digital cameras based on Sanyo firmware 
Name: camediaplay
Version: 20010211
Release: 1
Patch0: camediaplay-mint.patch


Copyright: distributable
Group: Applications/File
Packager: Marc-Anton Kehr <m.kehr@ndh.net>
Vendor: Sparemint
Source0: ftp://ftp.itojun.org/pub/digi-cam/800L/camediaplay-%{version}.tar.gz
Buildroot: /tmp/camediaplay-%{version}


%description
camediaplay is an downloading/controlling tool for digital cameras with
Sanyo firmware.  Camera with Sanyo firmware includes all Olympus prod-
ucts, Epson products, Agfa products, and of course, Sanyo digital cam-
eras.



%prep
%setup
%patch0 -p1


%build
./build/configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install

mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1



install -m 755 camediaplay   $RPM_BUILD_ROOT/usr/bin/camediaplay
install -m 644 src/camediaplay.man $RPM_BUILD_ROOT/usr/share/man/man1/camediaplay.1

gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man1/camediaplay.1
 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(0755,root,root)	/usr/bin/camediaplay
%attr(0644,root,root)	/usr/share/man/man1/camediaplay.1*

%doc README.english README.japanese 

%changelog
* Wed Mar 21 2001 Marc-Anton Kehr <m.kehr@ndh.net>
- build against MiNTLib 0.56.1

