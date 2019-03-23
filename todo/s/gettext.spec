Summary: Libraries and utilties for program national language support
Name: gettext
Version: 0.12.1
Release: 1
Copyright: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/pub/gnu/gettext-%{version}.tar.gz
Packager: Mark Duckworth <mduckworth@atari-source.com>
Vendor: Sparemint
Buildroot: /var/tmp/gettext-root
Summary(de): Libraries und Utilities zum Programmieren von nationaler Sprachunterstützung
Summary(fr): Librairies et  utilitaires pour le support de la langue nationnalepar les programmes.
Summary(tr): Yerel dil desteði için kitaplýk ve araçlar

%description
The gettext library provides an easy to use library and tools for creating,
using, and modifying natural language catalogs. It is a powerfull and simple
method for internationalizing programs.

%description -l de
Die gettext-Library enthält eine einfach anzuwendende Library und Tools
zum Erstellen, Verwenden und Ändern von natürlichsprachigen-Kataloge. Es ist
ein einfaches und leistungsfähiges Verfahren zum Lokalisieren von Programmen.

%description -l fr
La librarie gettext fournit des outils et une librairie simple à utiliser
pour manipuler, créer, et modifier des catalogues de langage naturel. C'est
une méthode simple et puissante pour internationnaliser les programmes.

%description -l tr
gettext, yerel dil desteðinde kullanýlan kataloglarý deðiþtirebilmek için,
kolayca kullanýlabilen kitaplýk ve araçlarý saðlar. Bu, programlarý
uluslararasýlaþtýrmak için sýkça baþvurulan, kuvvetli bir yöntemdir.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_BASENAME=1 -Dgnu_basename=basename" \
./configure \
	--prefix=/usr \
	--with-included-gettext

# The gettext package was written by the maintainer of the GNU libc and
# he thinks that only the GNU libc has a clean implementation of the
# basename function. ;-)
make

# This is still alpha software.  If a test fails, that doesn't necessarily
# mean that our port is broken.  It may just as well be the code itself.
# Better || :.
stack --fix=64k gettext-tools/src/msgfmt
make check || :

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/usr lispdir=$RPM_BUILD_ROOT/usr/share/emacs/site-lisp

( cd $RPM_BUILD_ROOT
  rm -f ./usr/info/dir
  gzip -9nf ./usr/info/*
  strip ./usr/bin/* || :
)
stack --size=64k $RPM_BUILD_ROOT/usr/bin/* ||:
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /usr/info/gettext.info.gz /usr/info/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete /usr/info/gettext.info.gz /usr/info/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README 
%doc README.gemtext README-alpha THANKS TODO
/usr/bin/autopoint
/usr/bin/gettext
/usr/bin/gettextize
/usr/bin/msgattrib
/usr/bin/msgcat
/usr/bin/msgcmp
/usr/bin/msgcomm
/usr/bin/msgconv
/usr/bin/msgen
/usr/bin/msgexec
/usr/bin/msgfilter
/usr/bin/msgfmt
/usr/bin/msggrep
/usr/bin/msginit
/usr/bin/msgmerge
/usr/bin/msgunfmt
/usr/bin/msguniq
/usr/bin/ngettext
/usr/bin/xgettext
/usr/include/*
/usr/info/*
/usr/lib/*.a
/usr/lib/*.la
/usr/share/gettext/*
/usr/share/locale/*
/usr/share/aclocal/*
/usr/share/emacs/site-lisp/*
/usr/share/man/*
/usr/share/doc/*

%changelog
* Tue Feb 24 2004 Mark Duckworth <mduckworth@atari-source.com>
- Original packager, guido flohr but because of the changes and upgrades
- bug reports should surely go to me.
- Upgraded to version 0.12.1 compiled against mintlib cvs
- Removed stuff about xgemtext, it doesn't seem to be part of this pkg?

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 11 1999 Guido Flohr <guido@freemint.de>
- Changed vendor to Sparemint.
