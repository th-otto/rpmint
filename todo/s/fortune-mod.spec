Summary: fortune cookie program with bug fixes 
Name: fortune-mod
Version: 1.0
Release: 2
Copyright: BSD
Group: Games
Source: ftp://sunsite.unc.edu/pub/Linux/games/amusements/fortune-mod-9708.tar.gz
Patch0: fortune-mod-offense.patch
Patch1: fortune-mod-mint.patch
BuildRoot: /var/tmp/fortune-mod-root
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): Glückskeks-Programm mit Bugfixes
Summary(fr): Programme fortune cookie avec bugs fixés.
Summary(tr): Rasgele, minik, sevimli mesajlar görüntüler

%description
This is the ever popular fortune program.  It will gladly print
a random fortune when run.  Is usually fun to put in the .login
for your users on a system so they see something new every time
they log in.

%description -l de
Dies ist das beliebte Glückskeks-Programm. Es druckt eine zufällige
Weisheit. Wenn Sie es in die .login-Datei Ihrer Benutzer schreiben,
erhalten diese bei jedem Anmelden einen neuen Spruch.

%description -l fr
Le célèbre programme fortune. Il affiche joyeusement un dicton
aléatoire lorsqu'il est lancé. Il est généralement amusant de le
placer dans le .login des utilisateurs d'un système pour qu'ils
voient quelque chose de nouveau à chaque fois qu'ils se loggent.

%description -l tr
Fortune, her çaðrýldýðýnda büyük bir kitaplýktan rasgele seçeceði, eðlenceli
bir metni görüntüleyecektir. Aþýrý bilimsel ve yararlý bir uygulama olmamasýna
karþýn kullanýcýlarýn her sisteme baðlanýþýnda deðiþik bir mesajla
karþýlaþmalarýný saðlar.

%prep
%setup -q -n fortune-mod-9708
%patch0 -p1
%patch1 -p1

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{games,sbin,man/man1,man/man6,share/games/fortune}

make	COOKIEDIR=/usr/share/games/fortunes fortune/fortune.man	
make	FORTDIR=$RPM_BUILD_ROOT/usr/games \
	COOKIEDIR=$RPM_BUILD_ROOT/usr/share/games/fortunes \
	BINDIR=$RPM_BUILD_ROOT/usr/sbin \
	BINMANDIR=$RPM_BUILD_ROOT/usr/man/man1 \
	FORTMANDIR=$RPM_BUILD_ROOT/usr/man/man6 \
	install
gzip -9nf $RPM_BUILD_ROOT/usr/man/man6/fortune.6
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/strfile.1
rm -f $RPM_BUILD_ROOT/usr/man/man1/unstr.1
ln -s strfile.1.gz $RPM_BUILD_ROOT/usr/man/man1/unstr.1.gz
stack --size=32k $RPM_BUILD_ROOT/usr/games/fortune

%clean
rm -rf $RPM_BUILD_ROOT

%preun
rm -f /usr/man/man1/unstr1.gz

%files
%defattr(-,root,root)
%doc README ChangeLog TODO
/usr/games/fortune
/usr/sbin/strfile
/usr/sbin/unstr
/usr/share/games/fortunes
/usr/man/man6/fortune.6.gz
/usr/man/man1/strfile.1.gz

%changelog
* Wed Aug 11 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Changed vendor to Sparemint.
