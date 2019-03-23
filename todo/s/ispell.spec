Summary: The GNU interactive spelling checker program.
Name: ispell
Version: 3.1.20
Release: 1
Group: Applications/Text
Source0: ftp://prep.ai.mit.edu/pub/gnu/ispell-3.1.20.tar.gz
Source1: ispell.info
Source2: spell
Source3: hk2-deutsch.tar.gz
Patch0: ispell-3.1.20-config.patch
Patch1: ispell-3.1.20-german.patch 
Patch2: ispell-3.1-info.patch
Patch3: ispell-3.1.20-termio.patch
Patch4: ispell-3.1.20-mask.patch
Patch5: ispell-3.1.20-strcmp.patch
Patch6: ispell-mint.patch
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): Die interaktive GNU-Rächzschreipprüvunk
Copyright: GPL
BuildRoot: /var/tmp/ispell-root

%description
Ispell is the GNU interactive spelling checker.  Ispell will check a text
file for spelling and typographical errors.  When it finds a word that is
not in the dictionary, it will suggest correctly spelled words for the
misspelled word.

You should install ispell if you need a program for spell checking (and who
doesn't...).

%description -l de
Ispell ist die interaktive GNU-Rechtschreibprüfung.  Ispell prüft einen
Text auf Rechtschreibfehler und typographische Fehler.  Wenn es ein 
Wort nicht im Wörterbuch findet, schlägt es richtig geschriebene Wörter
statt des falsch geschriebenen vor.

Ispell sollte installiert werden, wenn eine Rechtschreibprüfung
benötigt wird (und wer braucht das nicht ...).

%prep
%setup -q -n ispell-3.1
tar xzf $RPM_SOURCE_DIR/hk2-deutsch.tar.gz -C ./languages/deutsch/ '*.txt' '*.aff' '*README'
%patch0 -p1
%patch1 
# patch 1 deleted
%patch2 -p1 -b .makeinfo
%patch3 -p1 -b .termio

%ifarch alpha
%patch4 -p1 -b .mask
%endif

%patch5 -p1 -b .strcmp
%patch6 -p1 -b .mint

echo "Getting prebuilt ispell.info file :-(."
cp $RPM_SOURCE_DIR/ispell.info .

%build

# Make config.sh first
TMPDIR=/var/tmp PATH=.:$PATH make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" config.sh

# Get our RPM_OPT_FLAGS really in it.
mv Makefile Makefile.tmp
sed s,CFLAGS,RPM_OPT_FLAGS,g <Makefile.tmp >Makefile

# Now save build-rooted version (with time-stamp) for install ...
cp config.sh config.sh.BUILD
sed -e "s,/usr/,$RPM_BUILD_ROOT/usr/,g" < config.sh.BUILD > config.sh.INSTALL

# and then make everything
TMPDIR=/var/tmp PATH=.:$PATH make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/man
mkdir -p $RPM_BUILD_ROOT/usr/lib/emacs/site-lisp
mkdir -p $RPM_BUILD_ROOT/usr/info

# Roll in the build-root'ed version (with time-stamp!)
mv config.sh.INSTALL config.sh
TMPDIR=/var/tmp PATH=.:$PATH make install

mv $RPM_BUILD_ROOT/usr/info/ispell $RPM_BUILD_ROOT/usr/info/ispell.info
gzip -9nf $RPM_BUILD_ROOT/usr/info/ispell.info

install -m 755 ${RPM_SOURCE_DIR}/spell $RPM_BUILD_ROOT/usr/bin/

for manpage in buildhash munchlist findaffix tryaffix icombine ijoin; do
  ln -sf ispell.1.gz $RPM_BUILD_ROOT/usr/man/man1/$manpage.1.gz
done
ln -sf sq.1.gz $RPM_BUILD_ROOT/usr/man/man1/unsq.1.gz

gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/ispell.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man4/ispell.4
gzip -9nf $RPM_BUILD_ROOT/usr/man/man4/english.4
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/sq.1

strip $RPM_BUILD_ROOT/usr/bin/* || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
/usr/bin/ispell
/usr/bin/spell
/usr/man/man1/ispell.1.gz
/usr/man/man4/ispell.4.gz
/usr/info/ispell.info.gz
#/usr/lib/emacs/site-lisp/ispell.el
/usr/bin/buildhash
/usr/bin/icombine
/usr/bin/ijoin
/usr/bin/munchlist
/usr/bin/findaffix
/usr/bin/tryaffix
/usr/bin/sq
/usr/bin/unsq
/usr/man/man1/sq.1.gz
/usr/man/man1/buildhash.1.gz
/usr/man/man1/munchlist.1.gz
/usr/man/man1/findaffix.1.gz
/usr/man/man1/tryaffix.1.gz
/usr/man/man1/icombine.1.gz
/usr/man/man1/ijoin.1.gz
/usr/man/man1/unsq.1.gz
/usr/lib/ispell
/usr/man/man4/english.4.gz

%changelog
* Tue Sep 09 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Initial revision.
- Gzipped manpages.
- Added manpages icombine(1) and ijoin(1).
