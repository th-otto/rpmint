Summary: Vixie cron daemon
Name: vixie-cron
Version: 3.0.1
Release: 1
Copyright: distributable
Group: Daemons
Source0: ftp://ftp.vix.com/pub/vixie/vixie-cron-3.0.1.tar.gz
Source1: vixie-cron.init
Source2: cron.log
Source3: vixie-cron-mintdoc.tar.gz
Patch0: vixie-cron-3.0.1-sparemint.patch
Patch1: vixie-cron-3.0.1-security.patch
Patch3: vixie-cron-3.0.1-badsig.patch
Patch4: vixie-cron-3.0.1-crontab.patch
Patch5: vixie-cron-3.0.1-sigchld.patch
Patch6: vixie-cron-3.0.1-sprintf.patch
Patch7: vixie-cron-3.0.1-sigchld2.patch
Patch8: vixie-cron-mint.patch
Buildroot: /var/tmp/cron-root
#Prereq: /sbin/chkconfig
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): Vixie Cron-Dämon 
Summary(fr): Démon Vixie cron
Summary(tr): Vixie cron süreci, periyodik program çalýþtýrma yeteneði

%description
cron is a standard UNIX program that runs user-specified programs at
periodic scheduled times. vixie cron adds a number of features to the
basic UNIX cron, including better security and more powerful configuration
options.

%description -l de
Cron ist ein Standard-UNIX-Programm, das zu vorgegebenen Zeiten vom
Benutzer angegebene Programme ausführt. Vixie-Cron weist mehr Funktionen
auf als cron aus UNIX, u. a. bessere Sicherheit und leistungsfähigere
Konfigurationsoptionen.

%description -l fr
cron est un des programmes UNIX standard qui permet à un utilisateur donné
de lancer des périodiquement des programmes selon un ordre planifié.
vixie cron ajoute de nombreuses fonctionnalités au cron UNIX de base, dont
une plus grande sécurité et des options de configuration plus puissantes.

%description -l tr
cron UNIX'de standart olarak belirli zamanlarda bir programý çalýþtýrmak
için kullanýlan daemon'dur. Vixie cron, standart cron'dan daha güvenlidir
ve daha geliþmiþ yapýlandýrma seçenekleri içerir.

%prep
%setup
%patch0 -p1 -b .norh
%patch1 -p1 -b .nomisc
%patch3 -p1 -b .badsig
%patch4 -p1 -b .crontabhole
%patch5 -p1 -b .sigchld
%patch6 -p1 -b .sprintf
%patch7 -p1 -b .sigchld
%patch8 -p1 -b .mint

%build
make LIBS="-lport" RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man{1,5,8},sbin}
#mkdir -p $RPM_BUILD_ROOT/etc/rc.d/{init.d,rc{0,1,2,3,4,5,6}.d}
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/spool/cron
chmod 700 $RPM_BUILD_ROOT/var/spool/cron
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/crontab.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man5/crontab.5
gzip -9nf $RPM_BUILD_ROOT/usr/man/man8/cron.8
ln -sf cron.8.gz $RPM_BUILD_ROOT/usr/man/man8/crond.8.gz

#install -m755 $RPM_SOURCE_DIR/vixie-cron.init $RPM_BUILD_ROOT/etc/rc.d/init.d/crond
#cd $RPM_BUILD_ROOT/etc/rc.d
#ln -sf ../init.d/crond rc0.d/K60crond
#ln -sf ../init.d/crond rc1.d/K60crond
#ln -sf ../init.d/crond rc2.d/S40crond
#ln -sf ../init.d/crond rc3.d/S40crond
#ln -sf ../init.d/crond rc5.d/S40crond
#ln -sf ../init.d/crond rc6.d/K60crond

mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m644 $RPM_SOURCE_DIR/cron.log $RPM_BUILD_ROOT/etc/logrotate.d/cron

cd $RPM_BUILD_DIR/%{name}-%{version}
tar xzvf $RPM_SOURCE_DIR/vixie-cron-mintdoc.tar.gz

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#/sbin/chkconfig --add crond

#%postun
#if [ $1 = 0 ]; then 
#    /sbin/chkconfig --del crond
#fi

%files
%defattr(-,root,root)
%doc CHANGES CONVERSION FEATURES MAIL THANKS README README.MiNT
/usr/sbin/crond
/usr/bin/crontab
/usr/man/man8/crond.8.gz
/usr/man/man8/cron.8.gz
/usr/man/man5/crontab.5.gz
/usr/man/man1/crontab.1.gz
%dir /var/spool/cron

#%config(missingok) /etc/rc.d/rc0.d/K60crond
#%config(missingok) /etc/rc.d/rc1.d/K60crond
#%config(missingok) /etc/rc.d/rc2.d/S40crond
#%config(missingok) /etc/rc.d/rc3.d/S40crond
#%config(missingok) /etc/rc.d/rc5.d/S40crond
#%config(missingok) /etc/rc.d/rc6.d/K60crond
#%config /etc/rc.d/init.d/crond
#%config /etc/logrotate.d/cron
