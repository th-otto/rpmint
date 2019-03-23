Summary: A time server for synchronizing networked machines' clocks.
Name: intimed
Version: 1.10
Release: 2
Copyright: freeware
Group: System Environment/Daemons
Source: ftp://sunsite.unc.edu/pub/Linux/system/network/sunacm/Other/intimed/intimed-1.10.tar.gz
Patch: intimed.mint.patch
Prefix: /usr
Buildroot: /var/tmp/%{name}-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Summary(de): Ein Time-Server zum Synchronisieren der Uhren von vernetzten Maschinen

%description
The intimed package contains a server (in.timed), which keeps networked
machines' clocks correctly synchronized to the server's time.  

Install intimed if you need a network time server.

%description -l de
Das Paket intimed beinhaltet einen Server (in.timed), der die Uhren von vernetzten 
Maschinen zu der Uhrzeit des Servers synchronisiert.  

Installieren Sie intimed, wenn Sie einen Time-Server fÅr Ihr Netzwerk brauchen.

%prep
%setup -q -c
%patch -p1 -b .mint

%build
make
strip in.timed

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin

install -s -m 755 in.timed $RPM_BUILD_ROOT/usr/sbin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/sbin/in.timed

%changelog
* Sat Sep 04 1999 Edgar Aichinger <eaiching@t0.or.at>
- strip binary

* Sat Sep 04 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT 
- added Vendor, Packager, german Summary/Description
