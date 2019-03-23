Summary: library for accessing the termcap database
Name: libtermcap
Version: 2.0.8
Release: 4
Source: ftp://sunsite.unc.edu/pub/Linux/GCC/termcap-2.0.8.tar.gz
Url: ftp://sunsite.unc.edu/pub/Linux/GCC/
Copyright: LGPL
Group: Libraries
# Patch: termcap-2.0.8-shared.patch
Patch1: termcap-2.0.8-setuid.patch
Patch2: termcap-2.0.8-instnoroot.patch
Patch3: libtermcap-mint.patch
Requires: /etc/termcap
BuildRoot: /var/tmp/libtermcap-root
Packager: Guido Flohr <guido@freemint.de>
Vendor: Sparemint
Summary(de): Library zum Zugriff auf die termcap-Datenbank
Summary(fr): Librairie pour accéder à la base de données termcap.
Summary(tr): termcap veri tabanýna eriþim kitaplýðý

%description
This is the library for accessing the termcap database.  It is necessary
to be installed for a system to be able to do much of anything.  

%package devel
Summary: development libraries and header files for termcap library
Group: Libraries
Requires: libtermcap
Summary(de): Entwicklungs-Libraries und Header-Dateien für die termcap-Library
Summary(fr): Librairies de développement et fichiers d'en-tête pour la librairie termcap.
Summary(tr): termcap kitaplýðýný kullanan programlar geliþtirmek için gerekli dosyalar

%description devel
This is the package containing the development libaries and header
files for writing programs that access the termcap database.  It may
be necessary to build some other packages as well.

%description -l de devel
Dies ist ein Paket mit Entwicklungs-Libraries und Header-Dateien
zum Schreiben von Programmen, die auf die termcap-Datenbank
zugreifen. Eventuell müssen noch ein paar andere Pakete gebaut
werden.

%description -l de
Dies ist die Library zum Zugriff auf die termcap-Datenbank. Sie muß
installiert werden, damit das System funktionsfähig ist.

%description -l fr devel
Ceci est le package contenant les bibliothéques de développement et
les fichiers d'en-tête pour écrire des programmes accédant à la base 
de données termcap. Cela peut être nécessaire pour construire certains
autres packages.

%description -l fr
Bibliothèque pour accéder à la base de données termcap. Nécessaire pour
qu'un système puisse faire quelque chose.

%description -l tr devel
Bu paket, termcap veri tabanýný kullanan programlar geliþtirmek için gereken
baþlýk dosyalarý ve kitaplýklarý içerir.

%description -l tr
Bu paket termcap veri tabanýna ulaþým kitaplýðýný içerir. Sistem üzerinde
pek çok þeyi yapabilmek için kurulu olmasý gerekmektedir.

%prep
%setup -q -n termcap-2.0.8
# %patch -p1
%patch1 -p1
%patch2 -p1 -b .nochown
%patch3 -p1 -b .mint

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" CFLAGS="-g -I. $RPM_OPT_FLAGS" TARGETS="libtermcap.a"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{usr/lib,usr/info,usr/include,etc}

export PATH=/sbin:$PATH
make prefix=$RPM_BUILD_ROOT/usr TARGETS="libtermcap.a" install

install -m644 termcap.src $RPM_BUILD_ROOT/etc/termcap
cp termcap.info* $RPM_BUILD_ROOT/usr/info

( cd $RPM_BUILD_ROOT
  gzip -9nf ./usr/info/termcap.info*
  chmod 644 ./usr/info/termcap.info*
)

%clean
rm -rf $RPM_BUILD_ROOT

%trigger -- info >= 3.12
/sbin/install-info \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=/usr/info /usr/info/termcap.info.gz

%postun
if [ $1 = 0 ]; then
    /sbin/install-info --delete \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=/usr/info /usr/info/termcap.info.gz
fi

%files
%defattr(-,root,root)
/usr/info/termcap.info*

%files devel
%defattr(-,root,root)
%doc ChangeLog README
/usr/lib/libtermcap.a
/usr/include/termcap.h

%changelog
* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Fri Aug 13 1999 Guido Flohr <guido@freemint.de>
- Changed vendor to Sparemint

* Fri Jul 16 1999 Guido Flohr <guido@freemint.de>
- Fixed unresolvable references from setfsuid and setfsgid in libtermcap.c.
- Build against MiNTLib 0.52.3a
