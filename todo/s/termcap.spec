Summary: Terminal database used by many applications
Name: termcap
Version: 9.12.6
Release: 5
Copyright: none
Group: Base
Source0: http://www.ccil.org/~esr/terminfo/termtypes.tc.gz
Patch0: termcap-linuxlat.patch
Patch1: termcap-mint.patch
Excludearch: sparc
BuildArchitectures: noarch
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): Von zahlreichen Applikationen benutzte Terminal-Datenbank
Summary(fr): Base de donn�es sur le terminal utilis� par de nombreuses applications.
Summary(tr): U�birim veri taban�
BuildRoot: /var/tmp/termcap-root

%description
The /etc/termcap file is a database defining the capabilities of
various terminals and terminal emulators.  Programs use /etc/termcap
to gain access to various features of terminals such as the bell,
color, and graphics.

%description -l de
Die Datei /etc/termcap ist eine Datenbank, die die Funktionen verschiedener
Terminals und Terminal-Emulatoren definiert. Programme verwenden
/etc/termcap f�r den Zugriff auf verschiedene Terminal-Funktionen wie
Signalton, Farben und Grafiken.

%description -l fr
Le fichier /etc/termcap est une base de donn�es d�finissant les
possibilit�s des diff�rents terminaux et �mulateurs de terminaux.
Les programmes utilisent /etc/termcap pour acc�der aux diff�rentes
caract�ristiques des terminaux, comme le bip, la couleur et les
graphismes. 

%description -l tr
/etc/termcap dosyas�, �e�itli terminallerin ve terminal �yk�n�mc�lerinin
yeteneklerini tan�mlayan bir veri taban�d�r. Programlar, bu dosyay�
terminallerin zil sesi, renk ve grafik gibi �zelliklerine ula�mak i�in
kullan�rlar.

%prep
mkdir -p $RPM_BUILD_ROOT/etc
zcat $RPM_SOURCE_DIR/termtypes.tc.gz > $RPM_BUILD_ROOT/etc/termcap
(cd $RPM_BUILD_ROOT/etc;
%patch0 -p0
%patch1 -p0
)
chmod 644 $RPM_BUILD_ROOT/etc/termcap

%clean
rm -rf $RPM_BUILD_ROOT

%files
%config /etc/termcap

%changelog
* Wed Aug 11 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Removed overstrike capability from terminal descriptions.

* Fri Jul 30 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Rewrote all atari specific terminal descriptions from scratch.

* Fri Jul 16 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Fixed autowrap problem for tw52.
- Mapped colors to ANSI.
- Removed capabilities that are no longer available in current Toswin 
  versions.

* Wed Jun 30 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Added st52, stv52 and tt52 to termcap database.
