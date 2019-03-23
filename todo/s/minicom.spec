Summary: A text-based modem control and terminal emulation program.
Name: minicom
Version: 1.83.1
Release: 1
Vendor: Sparemint
Distribution: Sparemint
Packager: Jan Krupka <jkrupka@volny.cz>
Copyright: GPL
Group: Applications/Communications
Source: ftp://metalab.unc.edu/pub/Linux/apps/serialcomm/dialout/minicom-%{PACKAGE_VERSION}.src.tar.gz
Patch0: minicom-1.83.1-mint.patch
Patch1: minicom-1.83.1-make.patch
Buildroot: /var/tmp/%{name}-root

%description
Minicom is a simple text-based modem control and terminal emulation
program somewhat similar to MSDOS Telix.  Minicom includes a dialing
directory, full ANSI and VT100 emulation, an (external) scripting
language, and other features.

Minicom should be installed if you need a simple modem control program
or terminal emulator.

%prep
%setup -q

%patch0 -p1
%patch1 -p1

%build
make -C src

%install
rm -rf $RPM_BUILD_ROOT
make -C src install R=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc demos doc tables
%config /etc/minicom.users
%attr(2755,root,uucp) /usr/bin/minicom
/usr/bin/runscript
/usr/bin/ascii-xfr
%{_mandir}/*/*
/usr/share/locale/*/*/*

%changelog
* Sat Mar 2 2002 Jan Krupka <jkrupka@volny.cz>
- first release for Sparemint
