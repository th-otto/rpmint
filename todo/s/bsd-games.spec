Summary: miscellaneous BSD games package
Name: bsd-games
Version: 2.1
Release: 3
Copyright: distributable
Group: Games
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Source0: ftp://sunsite.unc.edu/pub/Linux/games/bsd-games-2.1.tar.gz
Patch0: bsd-games-2.1-config.patch
Patch1: bsd-games-2.1-nonlist.patch
Patch2: bsd-games-2.1-hole.patch
Patch3: bsd-games-2.1-sailbug.patch
Patch4: bsd-games-2.1-mint.patch
Buildroot: /var/tmp/bsd-games
Summary(de): Diverse BSD-Games  
Summary(fr): paquetage de jeux BSD divers
Summary(tr): Metin ekranda oyunlar paketi

%description
This is a bunch of games.  Highlights include backgammon, cribbage,
hangman, monop, primes, trek, and battlestar.

%description -l de
Dies ist eine Sammlung von Games. Zu den bekanntesten gehören Backgammon,
Cribbage, Monop, Primes, Trek und Battlestar.

%description -l fr
Lot de jeux. Contient backgammon, cribbage, le pendu, monop, primes, trek
et battlestar.

%description -l tr
Tavla, cribbage, adam asmaca, monop, primes, trek ve battlestar gibi oyunlar
içeren bir paket.

%prep
%setup -q
%patch -p1 -b .config
%patch1 -p1 -b .nonlist
%patch2 -p1 -b .nocheat
%patch3 -p1 -b .reallynocheat
%patch4 -p1 -b .mint
chmod +x install-man
chmod +x install-score

%build
rm -rf $RPM_BUILD_ROOT
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
make RPM_BUILD_ROOT="$RPM_BUILD_ROOT" install
# There are some shell scripts, so don't fail.
strip $RPM_BUILD_ROOT/usr/games/* 2>/dev/null || :
strip $RPM_BUILD_ROOT/usr/sbin/*
rm -f $RPM_BUILD_ROOT/usr/man/man6/{cfscores,morse,ppt,primes,rot13,snscore,teachgammon}.6
gzip -9nf $RPM_BUILD_ROOT/usr/man/man5/*.5
gzip -9nf $RPM_BUILD_ROOT/usr/man/man6/*.6
gzip -9nf $RPM_BUILD_ROOT/usr/man/man8/*.8
ln -s canfield.6.gz $RPM_BUILD_ROOT/usr/man/man6/cfscores.6.gz
ln -s bcd.6.gz $RPM_BUILD_ROOT/usr/man/man6/morse.6.gz
ln -s bcd.6.gz $RPM_BUILD_ROOT/usr/man/man6/ppt.6.gz
ln -s factor.6.gz $RPM_BUILD_ROOT/usr/man/man6/primes.6.gz
ln -s caesar.6.gz $RPM_BUILD_ROOT/usr/man/man6/rot13.6.gz
ln -s snake.6.gz $RPM_BUILD_ROOT/usr/man/man6/snscore.6.gz
ln -s backgammon.6.gz $RPM_BUILD_ROOT/usr/man/man6/teachgammon.6.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README 
%doc README.MiNT 
%doc BUGS 
%doc TODO 
%doc ChangeLog
%doc backgammon/README.linux
%doc dm/README.linux
%doc hunt/README
%doc hunt/README.linux
%doc phantasia/README
%doc trek/README.linux
%doc trek/DOC/read_me.nr
%doc trek/DOC/things
%doc trek/DOC/trekmanual.nr
%doc trek/USD.doc/spell.ok
%doc trek/USD.doc/trek.me
/var/lib/games
/usr/share/games
/usr/man/man5/*
/usr/man/man6/*
/usr/man/man8/*
/usr/games/*
/usr/sbin/*

%changelog
* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- correct Packager and Vendor
