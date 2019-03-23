Summary: English dictionary for /usr/dict
Name: words
Version: 2
Release: 1
Copyright: freeware
Group: Utilities/Text
Source: ftp://sunsite.unc.edu/pub/Linux/libs/linux.words.2.tar.gz
Patch0: linux.words.2-jbj.patch
BuildArchitectures: noarch
BuildRoot: /var/tmp/words-root
Summary(de): Englisches W�rterbuch f�r /usr/dict
Summary(fr): Dictionnaire anglais pour /etc/dict
Summary(tr): �ngilizce s�zl�k
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint

%description
This package contains the english dictionary in /usr/dict.  It
is used by programs like ispell as a database of words to check
for spelling and so forth.

%description -l de
Dieses Paket enth�lt das englische W�rterbuch in /usr/dict. Es
wird von Programmen wie ispell als Wortdatenbank, z.B. zum Pr�fen
der Rechtschreibung, verwendet.

%description -l fr
Ce paquetage contient le dictionnaire anglais dans /usr/dict. Il
est utilis� par des programmes comme ispell comme base de donn�es
de mots pour v�rifier l'orthographe.

%description -l tr
Bu paket ingilizce s�zl�k i�ermektedir. Ispell gibi yaz�l�mlar bu s�zc�k
veri taban�n� kullanarak yaz�m hatalar�n� bulmaya �al���rlar.

%prep
%setup -q -c
%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/dict

cp usr/dict/linux.words $RPM_BUILD_ROOT/usr/dict
ln -sf linux.words $RPM_BUILD_ROOT/usr/dict/words

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc usr/dict/README.linux.words
%doc usr/dict/README2.linux.words
/usr/dict/linux.words
/usr/dict/words

%changelog
* Wed Sep 09 1999 Guido Flohr <gufl0000@stud.uni-sb.de
- Initial revision.

