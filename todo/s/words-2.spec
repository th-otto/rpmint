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
Summary(de): Englisches Wörterbuch für /usr/dict
Summary(fr): Dictionnaire anglais pour /etc/dict
Summary(tr): Ýngilizce sözlük
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint

%description
This package contains the english dictionary in /usr/dict.  It
is used by programs like ispell as a database of words to check
for spelling and so forth.

%description -l de
Dieses Paket enthält das englische Wörterbuch in /usr/dict. Es
wird von Programmen wie ispell als Wortdatenbank, z.B. zum Prüfen
der Rechtschreibung, verwendet.

%description -l fr
Ce paquetage contient le dictionnaire anglais dans /usr/dict. Il
est utilisé par des programmes comme ispell comme base de données
de mots pour vérifier l'orthographe.

%description -l tr
Bu paket ingilizce sözlük içermektedir. Ispell gibi yazýlýmlar bu sözcük
veri tabanýný kullanarak yazým hatalarýný bulmaya çalýþýrlar.

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

