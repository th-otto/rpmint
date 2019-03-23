Summary: RCS - version control system
Name: rcs
Version: 5.7
Release: 3
Copyright: GPL
Group: Development/Version Control
Source: ftp://prep.ai.mit.edu:/pub/gnu/rcs-5.7.tar.gz
Patch0: rcs-5.7-stksize.patch
Patch1: rcs-5.7-stupidrcs.patch
Buildroot: /var/tmp/rcs-root
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): RCS - Versionssteuersystem
Summary(fr): RCS - Syst�me de contr�le de version
Summary(fr.atarist): RCS - Syst�me de contr�le de version
Summary(tr): S�r�m denetleme sistemi

%description
The Revision Control System (RCS) manages multiple revisions of files.
RCS automates the storing, retrieval, logging, identification, and
merging of revisions.  RCS is useful for text that is revised
frequently, for example programs, documentation, graphics, papers, and
form letters.

%description -l de
Das Revision Control System (RCS) verwaltet mehrere Dateirevisionen. 
Es automatisiert das Abspeichern, das Einlesen, das Aufzeichnen, 
die Erkennung und das Zusammenf�hren von Revisionen. RCS ist praktisch
f�r Texte, die h�ufig revidiert werden, etwa Programme, 
Dokumentation, Graphiken, Artikel und Formulare. 

%description -l fr
Le syst�me de contr�le de r�vision (RCS) g�re les nombreuses r�visions
des fichiers. RCS automatise le stockage, la r�cup�ration, l'identification
et le m�lange des r�visions. RCS sert aux textes r�vis�s fr�quemment, par
exemple les "programmes, la documentation, les graphiques, les articles et
les lettres.  

%description -l tr
S�r�m denetim sistemi (Revision Control System - RCS) bir dosyan�n birden
fazla s�r�m�n� denetlemek i�in kullan�l�r. RCS dosya �zerindeki
de�i�ikliklerin tutulmas�n�, saklanmas�n�, kay�tlar�n�n tutulmas� i�lerini
kolayla�t�r�r. �zerinde s�k�a de�i�iklik yap�lan program kodlar�, belgeler ve
makaleler i�in son derece yararl� bir ara�t�r.

%prep
rm -rf $RPM_BUILD_ROOT

%setup

%patch0 -p1
%patch1 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --with-diffutils
touch src/conf.h
make 

%install
./configure --prefix=$RPM_BUILD_ROOT/usr --with-diffutils
touch src/conf.h
make install

strip $RPM_BUILD_ROOT/usr/bin/*
chmod a+x $RPM_BUILD_ROOT/usr/bin/*

gzip --best $RPM_BUILD_ROOT/usr/man/*/*

%files
%doc NEWS REFS
/usr/bin/*
/usr/man/man1/*
/usr/man/man5/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Aug 12 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Renamed vendor to Sparemint

* Thu Jul 8 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Renamed spec file to rcs.spec
- Built against MiNTLib 0.53.3a

