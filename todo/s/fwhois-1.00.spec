Summary: finger-style whois 
Name: fwhois
Version: 1.00
Release: 2
Packager: John Blakeley <johnnie@ligotage.demon.co.uk>
Vendor: Sparemint
Copyright: BSD
Group: Networking/Utilities
Source: fwhois-1.00.tar.gz
Buildroot: /var/tmp/fwhois-root
Summary(de): Finger-artiges whois
Summary(fr): Un whois dans le style finger.
Summary(tr): finger tarzý whois

%changelog
* Tue Apr 25 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- Rebuilt against mintlib-0.55.2

* Tue Jan 11 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- First release for Sparemint

%description
This is the ``whois'' program.  It will allow you to find out
information on people stored in the whois databases around 
the world.

%description -l de
Dies ist das 'WHOIS'-Programm. Es gestattet Ihnen, in den 
Whois-Datenbanken rund um die Welt nach Personen zu suchen. 

%description -l fr
Programme « whois ». Il vous permet d'obtenir des informations sur les
personnes répertoriées dans les bases de données whois de part le monde.

%description -l tr
whois ile dünyadaki whois veri tabanlarýnda kaydý bulunan kiþiler hakkýnda
bilgi edinebilirsiniz.

%prep
%setup

%build
gcc $RPM_OPT_FLAGS -s fwhois.c -o fwhois -lsocket

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -s -m755 fwhois $RPM_BUILD_ROOT/usr/bin/fwhois
ln -sf fwhois $RPM_BUILD_ROOT/usr/bin/whois

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README
/usr/bin/fwhois
/usr/bin/whois
