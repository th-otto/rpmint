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
Summary(fr): RCS - Système de contrôle de version
Summary(fr.atarist): RCS - SystŠme de contr“le de version
Summary(tr): Sürüm denetleme sistemi

%description
The Revision Control System (RCS) manages multiple revisions of files.
RCS automates the storing, retrieval, logging, identification, and
merging of revisions.  RCS is useful for text that is revised
frequently, for example programs, documentation, graphics, papers, and
form letters.

%description -l de
Das Revision Control System (RCS) verwaltet mehrere Dateirevisionen. 
Es automatisiert das Abspeichern, das Einlesen, das Aufzeichnen, 
die Erkennung und das Zusammenführen von Revisionen. RCS ist praktisch
für Texte, die häufig revidiert werden, etwa Programme, 
Dokumentation, Graphiken, Artikel und Formulare. 

%description -l fr
Le système de contrôle de révision (RCS) gère les nombreuses révisions
des fichiers. RCS automatise le stockage, la récupération, l'identification
et le mélange des révisions. RCS sert aux textes révisés fréquemment, par
exemple les "programmes, la documentation, les graphiques, les articles et
les lettres.  

%description -l tr
Sürüm denetim sistemi (Revision Control System - RCS) bir dosyanýn birden
fazla sürümünü denetlemek için kullanýlýr. RCS dosya üzerindeki
deðiþikliklerin tutulmasýný, saklanmasýný, kayýtlarýnýn tutulmasý iþlerini
kolaylaþtýrýr. Üzerinde sýkça deðiþiklik yapýlan program kodlarý, belgeler ve
makaleler için son derece yararlý bir araçtýr.

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

