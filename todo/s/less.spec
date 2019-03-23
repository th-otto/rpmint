Summary: A text file browser similar to more, but better.
Name: less
Version: 458
Release: 1
License: GPL
Group: Applications/Text
Packager: P Slegg <mint@lists.fishpool.fi>
Vendor: Sparemint
Source: http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
Source1: lesspipe.sh
Source2: less.sh
Source3: less.csh
URL: http://www.greenwoodsoftware.com/less/
Buildroot: /var/tmp/less-root
Summary(de): Ein Betrachter für Textdateien, ähnlich more, aber besser.

%description
The less utility is a text file browser that resembles more, but has
more capabilities.  Less allows you to move backwards in the file as
well as forwards.  Since less doesn't have to read the entire input file
before it starts, less starts up more quickly than text editors (for
example, vi). 

You should install less because it is a basic utility for viewing text
files, and you'll use it frequently.

%description -l de
Das Utility less ist ein Betrachter für Textdateien, der more ähnelt, aber
mehr Möglichkeiten bietet. Less erlaubt Ihnen, sich in der Datei genauso 
rückwärts wie vorwärts zu bewegen.  Weil less nicht die ganze Datei lesen 
muß, bevor es startet, ist sein Programmstart schneller als der von 
Texteditoren (zum Beispiel vi). 

Sie sollten Less installieren, weil es ein grundlegendes Utility zum 
Betrachten von Textdateien ist, und Sie werden es häufig benützen.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s ./configure --prefix=/usr
make datadir=/usr/doc

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/usr \
             exec_prefix=$RPM_BUILD_ROOT/usr \
             mandir=$RPM_BUILD_ROOT/usr/share/man
strip -R .comments $RPM_BUILD_ROOT/usr/bin/less
stack --fix=32k $RPM_BUILD_ROOT/usr/bin/* || :
gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man1/*

mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -c -m 755 %{SOURCE1} $RPM_BUILD_ROOT/usr/bin/
install -c -m 755 %{SOURCE2} $RPM_BUILD_ROOT/etc/profile.d
install -c -m 755 %{SOURCE3} $RPM_BUILD_ROOT/etc/profile.d

%files
/etc/profile.d/*
/usr/bin/*
/usr/share/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Dec 18 2013 P Slegg <mint@lists.fishpool.fi>
- new version 458

* Tue Jul 30 2002 Edgar Aichinger <eaiching@t0.or.at>
- new version 376

* Sat Mar 09 2002 Edgar Aichinger <eaiching@t0.or.at>
- new version 374

* Tue Dec 12 2000 Edgar Aichinger <eaiching@t0.or.at>
- new version 358

* Fri May 05 2000 Edgar Aichinger <eaiching@t0.or.at>
- forgot to mark german description in specfile

* Fri Apr 21 2000 Edgar Aichinger <eaiching@t0.or.at>
- build against mintlibs 0.55.2

* Thu Apr 06 2000 Edgar Aichinger <eaiching@t0.or.at>
- updated to version 354
- man pages to /usr/share/man

* Mon Oct 18 1999 Edgar Aichinger <eaiching@t0.or.at>
- updated to version 340
- added german summary and description

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
