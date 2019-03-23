Summary:	A utility for converting amounts from one unit to another.
Name:		units
Version:	1.74
Release:	1
Source:		ftp://ftp.gnu.org/gnu/units/%{name}-%{version}.tar.gz
Copyright:	GPL
Group:		Applications/Engineering
BuildRoot:	/var/tmp/units-root
Distribution:	Sparemint
Vendor:		Sparemint
Packager:	Edgar Aichinger <eaiching@t0.or.at>
Summary(de):	Ein Utility zum Konvertieren zwischen Maßeinheiten.

%description
Units converts an amount from one unit to another, or tells you what
mathematical operation you need to perform to convert from one unit to
another.  Units can handle multiplicative scale changes as well as 
nonlinear conversions such as Fahrenheit to Celsius.

Units is a handy little program which contains a large number of
conversions, from au's to parsecs and tablespoons to cups.  You probably
don't need to install it, but it comes in handy sometimes.

%description -l de
Units konvertiert einen Betrag von einer Einheit in eine andere, oder 
gibt aus, welche mathematische Operationen für diesen Vorgang nötig sind.
Units kann sowohl multiplikative als auch nichtlineare Umwandlungen 
durchführen (so wie von Fahrenheit nach Celsius).

Units ist a nützliches kleines Programm, das eine Vielzahl von Umwandlungen
beinhaltet, von AE nach parsec bis zu Teelöffel nach Tassen.  Sie müssen
es nicht installieren, aber es kann manchmal recht praktisch sein.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=${RPM_BUILD_ROOT}%{_prefix} exec_prefix=${RPM_BUILD_ROOT}%{_prefix} install
strip $RPM_BUILD_ROOT/usr/bin/* || :

gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/units.1
gzip -9nf $RPM_BUILD_ROOT/usr/info/units.info

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /usr/info/units.info.gz /usr/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete /usr/info/units.info.gz /usr/info/dir
fi

%files
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/share/*
%{_prefix}/info/*
%{_prefix}/man/man1/*
%doc units.doc README NEWS ChangeLog 

%changelog
* Thu Sep 13 2001 Edgar Aichinger <eaiching@t0.or.at>
- updated to version 1.74

* Sat Nov 13 1999 Edgar Aichinger <eaiching@t0.or.at>
- small corrections in specfile (release 2)

* Tue Nov 09 1999 Edgar Aichinger <eaiching@t0.or.at>
- updated to version 1.55
- compressed manpage and info file

* Wed Sep 15 1999 Edgar Aichinger <eaiching@t0.or.at>
- cleanup in spec file

* Fri Aug 27 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT 
