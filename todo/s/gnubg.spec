Summary: GNU Backgammon
Name: gnubg
Version: 0.02
Release: 3
Copyright: GPL
Group: Games
Source0: ftp://alpha.gnu.org/gnu/gnubg/gnubg-0.02.tar.gz
Source1: ftp://alpha.gnu.org/gnu/gnubg/gnubg.bd.gz
Source2: ftp://alpha.gnu.org/gnu/gnubg/gnubg.weights.newer.gz
Patch0: gnubg-0.02-SetTurn.patch
Patch1: gnubg-0.02-pkgdatadir.patch
Patch2: gnubg-0.02-event.patch
Patch3: gnubg-0.02-x11libs.patch
URL: http://www.gnu.org/software/gnubg/
Packager: Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
Vendor: Sparemint
Buildroot: /var/tmp/gnubg-root
Buildrequires: mintbin

%description
This is a pre-release version of GNU Backgammon (gnubg), a backgammon
player and analysis tool.  Please send comments and suggestions to
<gnubg@sourceforge.net>.

Look for news and upcoming releases of GNU Backgammon at:
    http://gnubg.sourceforge.net/

%prep
%setup -q -T -b 0
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
gunzip -c "$RPM_SOURCE_DIR/gnubg.bd.gz" > gnubg.bd
gunzip -c "$RPM_SOURCE_DIR/gnubg.weights.newer.gz" > gnubg.weights

%build
#touch Makefile.in configure
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr/games
make
stack -S 128k gnubg

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/games/{bin,share}

make prefix=$RPM_BUILD_ROOT/usr/games install-strip

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README NEWS TODO
/usr/games/bin/gnubg
/usr/games/share/gnubg/gnubg.bd
/usr/games/share/gnubg/gnubg.weights

%changelog
* Thu Nov 14 2000 Frank Naumann <fnaumann@freemint.de>
- enabled X11 support

* Sat Apr  8 2000 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- initial revision for SpareMiNT, no X support
