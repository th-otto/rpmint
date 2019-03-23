Summary: Reads and writes data across network connections using TCP or UDP.
Summary(de): Liest und schreibt Daten ueber TCP oder UPD Netzwerkverbindungen.
Name: nc
Version: 1.10
Release: 2
Copyright: GPL
Group: Applications/Internet
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Source: ftp://ftp.avian.org/src/hacks/nc110.tgz
Patch0: nc-arm.patch
BuildRoot: /var/tmp/nc-root

%description
The nc package contains Netcat (the program is actually nc), a simple
utility for reading and writing data across network connections, using
the TCP or UDP protocols. Netcat is intended to be a reliable back-end
tool which can be used directly or easily driven by other programs and
scripts.  Netcat is also a feature-rich network debugging and exploration
tool, since it can create many different connections and has many
built-in capabilities.

You may want to install the netcat package if you are administering a
network and you'd like to use its debugging and network exploration
capabilities.

%description -l de
Das nc Paket enthält Netcat (das Programm selbst heißt nc). Netcat ist ein
einfaches Tool um Daten üeber TCP oder UDP Netzwerkverbindungen zu lesen und
schreiben. Es ist als stabiles und einfaches Backend gedacht, entweder zur
direkten Benutzung oder für andere Programme. Netcat ist weiterhin ein
komfortables Debugging Tool.

Installiere das Tool wenn du im Rahmen von Administrationsaufgaben
Netzwerke überwachen und kontrollieren mußt.

%prep
%setup -c -n nc -q
%patch0 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS" XLIBS=-lsocket generic

%install
mkdir $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT/usr
mkdir $RPM_BUILD_ROOT/usr/bin

cp nc $RPM_BUILD_ROOT/usr/bin
strip $RPM_BUILD_ROOT/usr/bin/nc
stack --fix=64k $RPM_BUILD_ROOT/usr/bin/nc || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README Changelog
%doc scripts
/usr/bin/nc

%changelog
* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- correct Packager and Vendor
