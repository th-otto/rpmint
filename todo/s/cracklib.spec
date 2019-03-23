Summary: A password-checking library.
Name: cracklib
Version: 2.7
Release: 3
Group: System Environment/Libraries
Source: ftp://coast.cs.purdue.edu/pub/tools/unix/cracklib/cracklib_2.7.tgz
Url: ftp://coast.cs.purdue.edu/pub/tools/unix/cracklib/
Copyright: artistic
Patch: cracklib-2.7-sparemint.patch
Buildroot: /var/tmp/cracklib-root/
Packager: Guido Flohr <guido@freemint.de>
Vendor: Sparemint
Summary(de): Eine Bibliothek zur Passwort-Prüfung.

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics.  You can use CrackLib to stop
users from choosing passwords which would be easy to guess.  CrackLib
performs certain tests: 

* It tries to generate words from a username and gecos entry and 
  checks those words against the password;
* It checks for simplistic patterns in passwords;
* It checks for the password in a dictionary.

CrackLib is actually a library containing a particular
C function which is used to check the password, as well as
other C functions. CrackLib is not a replacement for a passwd
program; it must be used in conjunction with an existing passwd
program.

Install the cracklib package if you need a program to check users'
passwords to see if they are at least minimally secure. If you
install CrackLib, you'll also want to install the cracklib-dicts
package.

%description -l de
CrackLib testet Passwörter, um festzustellen, ob sie gewisse 
sicherheitsrelevante Charakteristiken aufweisen.  CrackLib kann dazu
benutzt werden, um zu verhindern, dass Benuterinnen Passwörter
wählen, die einfach zu erraten sind.  CrackLib führt dazu bestimmte
Tests durch:

* Aus dem Benutzernamen und dem Gecos-Feld werden Wörter generiert,
  und auf Übereinstimmung mit dem Passwort geprüft
* Einfache Muster in Passwörtern werden geprüft
* Es wird geprüft, ob das Passwort im Wörterbuch enthalten ist

CrackLib ist eigentlich eine Bibliothek, die eine bestimmte C-Funktion
enthält, die verwendet wird, um das Passwort zu prüfen, sowie auch
andere C-Funktion.  CrackLib ist kein Ersatz für das Programm passwd;
die Bibliothek kann nur in Verbindung mit einem vorhandenen 
passwd-Programm benutzt werden.

Das CrackLib-Paket sollte installiert werden, wenn Software benötigt
wird, die prüft, ob die Benutzerpasswörter minimalen 
Sicherheitsanforderungen genügt.  Wer CrackLib installiert, sollte auch
das Paket cracklib-dicts installieren.

%package dicts
Summary: The standard CrackLib dictionaries.
Group: System Environment/Libraries
Summary(de): Die Standard-CrackLib-Wörterbücher.

%description dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/dict/words.  Cracklib-dicts also contains
the utilities necessary for the creation of new dictionaries.

If you are installing CrackLib, you should also install cracklib-dicts.

%description -l de dicts
Das Paket cracklib-dicts beinhaltet die CrackLib-Wörterbücher.
CrackLib benötigt die geeigneten System-Wörterbücher, die 
normalerweise in /usr/dict/words installiert sind.  Cracklib-dicts
beinhaltet auch die Werkzeuge, die zur Erzeugung neuer Wörterbücher
notwendig sind.

%prep
%setup -q -n cracklib,2.7
%patch -p1 -b .sparemint

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" all

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{sbin,lib,include}
make install ROOT=$RPM_BUILD_ROOT
strip $RPM_BUILD_ROOT/usr/sbin/packer

%files
%doc README MANIFEST LICENCE HISTORY POSTER
/usr/include/*
/usr/lib/lib*

%files dicts
/usr/sbin/*
/usr/lib/cracklib_dict*

%changelog
* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNT-Lib

* Sat Sep 11 1999 Guido Flohr <guido@freemint.de>
- Initial revision
