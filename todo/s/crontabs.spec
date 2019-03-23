Summary: Root crontab files used to schedule the execution of programs.
Name: crontabs
Version: 1.7
Release: 2
Copyright: public domain
Group: System Environment/Base
Source0: crontab
Source1: run-parts
Requires: tmpwatch
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
BuildArchitectures: noarch
BuildRoot: /var/tmp/crontabs-root
Summary(de): Root-Crontab-Dateien, um Ausführungszeit von Programmen festzulegen.

%description
The crontabs package contains root crontab files.  Crontab is the
program used to install, uninstall or list the tables used to drive the
cron daemon.  The cron daemon checks the crontab files to see when
particular commands are scheduled to be executed.  If commands are
scheduled, it executes them.

Crontabs handles a basic system function, so it should be installed on
your system.

%description -l de
Das Paket crontabs enthält die Crontab-Dateien für den Superuser root.
Crontab ist das Programm, mit dem die Tabellen, die den Cron-Dämon steuern,
installiert, deinstalliert oder aufgelistet werden.  Der Cron-Dämon prüft
die Crontab-Dateien, um festzustellen, wann ein bestimmtes Kommando
ausgeführt werden soll.  Wenn ein Kommando an der Reihe ist, startet der
Dämon es.

Crontabs erfüllt eine fundamentale Systemfunktion, so dass es auf jedem
System installiert werden sollte.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/cron.{hourly,daily,weekly,monthly}
mkdir -p $RPM_BUILD_ROOT/usr/bin

install -m644 $RPM_SOURCE_DIR/crontab $RPM_BUILD_ROOT/etc/crontab
install -m755 $RPM_SOURCE_DIR/run-parts $RPM_BUILD_ROOT/usr/bin/run-parts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config /etc/crontab
/usr/bin/run-parts
%dir /etc/cron.hourly
%dir /etc/cron.daily
%dir /etc/cron.weekly
%dir /etc/cron.monthly

%changelog
* Wed Aug 25 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Added German translations.
- Modified to meet Sparemint standards.
