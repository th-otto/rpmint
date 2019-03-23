Summary: A utility for monitoring system logs files.
Name: swatch
Version: 2.2
Release: 1
Copyright: Distributable
Group: Applications/System
Source: ftp://ftp.stanford.edu/general/security-tools/swatch/swatch-2.2.tar.gz
Patch0: swatch-2.2-redhat.patch
BuildArchitectures: noarch
BuildRoot: /var/tmp/%{name}-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Requires: Perl
Summary(de): Ein Utility, um Log-Dateien zu betrachten.

%description
The Swatch utility monitors system log files, filters out unwanted data
and takes specified actions (i.e., sending email, executing a script,
etc.) based upon what it finds in the log files.

Install the swatch package if you need a program that will monitor log
files and alert you in certain situations.

%description -l de
Das Utility swatch zeigt Log-Dateien an, filtert unerwünschte Daten und
unternimmt bestimmte Aktionen (z.B. email senden, ein Skript ausführen usw.),
abhängig davon, was in den Log-Dateien steht.

Installieren Sie das Paket, wenn Sie ein Programm brauchen, das Log-Dateien
anzeigen und Sie in bestimmten Situationen warnen kann.

%prep
%setup -q
%patch0 -p1 -b .redhat

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,lib,man/man5,man/man8}

perl install.pl
gzip -9nf $RPM_BUILD_ROOT/usr/man/man5/%{name}.5
gzip -9nf $RPM_BUILD_ROOT/usr/man/man8/%{name}.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/swatch
/usr/lib/sw_actions.pl
/usr/lib/sw_history.pl
/usr/man/man5/swatch.5.gz
/usr/man/man8/swatch.8.gz
%doc *.ps config_files README Changes

%changelog
* Sat Sep 04 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT 
- added Vendor, Packager, Requires and german Summary/Description
- compressed manpage
