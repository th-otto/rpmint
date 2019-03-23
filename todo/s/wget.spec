Summary       : Retrieve files from the World Wide Web using HTTP and FTP
Summary(de)   : Dateien aus dem World Wide Web ueber HTTP oder FTP herunterladen
Name          : wget
Version       : 1.9.1
Release       : 0
Copyright     : GPL
Group         : Applications/Networking

Packager      : Guido Flohr <guido@freemint.de>
Vendor        : Sparemint
URL           : http://wget.sunsite.dk/

Prereq        : /sbin/install-info
Conflicts     : wget-ssl

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.gnu.org/pub/gnu/wget/wget-%{version}.tar.gz 


%description
GNU Wget is a freely available network utility to retrieve files from the
World Wide Web using HTTP and FTP, the two most widely used Internet
protocols.  It works non-interactively, thus enabling work in the background,
after having logged off. 

The recursive retrieval of HTML pages, as well as FTP sites is supported --
you can use Wget to make mirrors of archives and home pages, or traverse the
web like a WWW robot (Wget understands /robots.txt). 

Wget works exceedingly well on slow or unstable connections, keeping getting
the document until it is fully retrieved. Re-getting files from where it left
off works on servers (both HTTP and FTP) that support it. Matching of
wildcards and recursive mirroring of directories are available when retrieving
via FTP. Both HTTP and FTP retrievals can be time-stamped, thus Wget can see
if the remote file has changed since last retrieval and automatically retrieve
the new version if it has. 

By default, Wget supports proxy servers, which can lighten the network load,
speed up retrieval and provide access behind firewalls. However, if you are
behind a firewall that requires that you use a socks style gateway, you can
get the socks library and compile wget with support for socks. 

Most of the features are configurable, either through command-line options, or
via initialization file .wgetrc.  Wget allows you to install a global startup
file (/etc/wgetrc on Sparemint or RedHat) for site settings. 

%description -l de
GNU Wget ist ein frei erhältliches Netzwerk-Tool, mit Hilfe dessen man
Dateien aus dem Word Wide Web über HTTP oder FTP - den beiden 
meistbenutzten Internet-Protokollen - herunterladen kann.  Wget arbeitet
nicht interaktiv und kann somit im Hintergrund nach einem Logout benutzt
werden.

Auch das rekursive Herunterladen von HTML-Seiten, ebenso wie FTP-Sites
wird unterstützt -- Wget kann damit auch zum Spiegeln von Archiven oder
Homepages benutzt werden. Genauso kann es wie ein Roboter (Wget wertet
/robots.txt aus) das Web durchwandern.

Wget arbeitet außerordentlich gut über langsame oder instabile 
Netzwerkverbindungen; es versucht ein Dokument so lange zu laden, bis
es vollständig angekommen ist.  Die Wiederaufnahme abgebrochener
Transaktionen funktioniert auf Servern (sowohl HTTP als auch FTP), die
dies unterstützen.  Die Auswertung von Meta-Zeichen (Wildcards) und
das rekursive Spiegeln von Verzeichnissen sind über FTP möglich.
Sowohl HTTP- als auch FTP-Transaktionen können Zeitstempel benutzen,
damit Wget erkennen kann, ob eine entfernte Datei sich seit dem letzten
Download geändert hat, und gegebenenfalls eine neue Version lädt.

Standardmäßig unterstützt Wget Proxy-Server, die die Netzwerkbelastung
mildern, die Ladezeiten verkürzen und Zugriff hinter Firewalls ermöglichen.
Jedoch, um Wget hinter einem Firewall zu benutzen, muss ein Socks-Gateway
benutzt werden, und Wget deshalb mit der Socks-Bibliothek neukompiliert
werden.

Die meisten Fähigkeiten sind konfigurierbar, entweder über Kommandozeilen-
Optionen oder über die Initialisierungsdatei .wgetrc.  Wget erlaubt auch
die Installation einer globalen Startdatei (/etc/wgetrc auf Sparemint oder
RedHat), um systemweite Voreinstellungen vorzunehmen.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=/etc \
	--without-ssl
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	sysconfdir=${RPM_BUILD_ROOT}/etc

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* || :
stack --fix=96k ${RPM_BUILD_ROOT}%{_prefix}/bin/* || :

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/man*/*

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/


%post
/sbin/install-info %{_prefix}/info/wget.info.gz %{_prefix}/info/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/wget.info.gz %{_prefix}/info/dir
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog MACHINES MAILING-LIST NEWS PATCHES
%doc README TODO
%config /etc/wgetrc
%{_prefix}/bin/wget
%{_prefix}/info/*
%{_prefix}/share/man/man1/wget.1.gz
%{_prefix}/share/locale/*/LC_MESSAGES/*


%changelog
* Mon Dec 08 2003 Adam Klobukowski <atari@gabo.pl>
- updated to version 1.9.1

* Tue Oct 23 2003 Adam Klobukowski <atari@gabo.pl>
- updated to version 1.9

* Wed Dec 26 2001 Frank Naumann <fnaumann@freemint.de>
- updated to version 1.8.1

* Mon Jul 09 2001 Frank Naumann <fnaumann@freemint.de>
- updated to version 1.7

* Sat Mar 17 2001 Frank Naumann <fnaumann@freemint.de>
- updated to version 1.6
