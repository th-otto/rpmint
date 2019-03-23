Summary: copy web site files to server by ftp
Vendor: Sparemint
Distribution: Sparemint
Packager: Edgar Aichinger <eaiching@t0.or.at>
Name: sitecopy
Version: 0.5.1
Release: 1
Group: Networking/Utilities
Copyright: GPL
Source: http://www.lyra.org/sitecopy/sitecopy-0.5.1.tar.gz
BuildRoot: /var/tmp/%{name}-root
Summary(de): Dateien einer Website per ftp zum Server kopieren

%description
sitecopy is for copying LOCALLY stored websites to REMOTE ftp servers.
The program will upload files to the server which have changed
locally, and delete files from the server which have been removed
locally, to keep the remote site synchronized with the local site,
with a single command.  The aim is to remove the hassle of uploading
and deleting individual files using an FTP client.

sitecopy is NOT for copying websites onto your hard disk - if you want
to do that, get a mirroring program.

%description -l de
Sitecopy dient dazu, LOKAL gespeicherte Websites an ENTFERNTE ftp-Server zu
senden.  Das Programm wird - mit einem einzigen Befehl - alle Dateien, die
lokal verändert wurden, zum Server schicken, und am Server all jene Dateien
löschen, die lokal entfernt wurden, um so die entfernte Site zur lokalen zu
synchronisieren.  Das Ziel ist es, Ihnen den Ärger zu ersparen, einzelne
Dateien mittels FTP-Client manuell hochladen bzw. löschen zu müssen.

Sitecopy dient NICHT dazu, Websites auf Ihre Festplatte zu kopieren - falls
Sie das tun wollen, besorgen Sie sich ein "mirroring"-Programm.


%prep
%setup 

%build
./configure --prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT/usr/bin
install -s -o root -g bin -m 0755 sitecopy $RPM_BUILD_ROOT/usr/bin

install -d -m 0755 $RPM_BUILD_ROOT/usr/share/man/man1
install -o root -g root -m 0644 sitecopy.1 $RPM_BUILD_ROOT/usr/share/man/man1
gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man1/sitecopy.1
mkdir -p $RPM_BUILD_ROOT/usr/doc/sitecopy-0.5.1

%files
/usr/bin/*
/usr/share/man/man1/*
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc README
%doc RELEASE
%doc TODO

%changelog
* Thu Aug 24 2000 <eaiching@t0.or.at>
- first release for SpareMiNT 
- changed Vendor, Packager, Distribution
- added german Summary/Description
- moved (compressed) manpages to /usr/share/man

