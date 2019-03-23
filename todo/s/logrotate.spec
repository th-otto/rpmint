Summary       : Rotates, compresses, removes and mails system log files.
Summary(de)   : Rotiert, komprimiert, entfernt und mailt System-Logdateien.
Name          : logrotate
Version       : 3.5.9
Release       : 1
Copyright     : GPL
Group         : System Environment/Base

Packager      : Guido Flohr <guido@freemint.de>
Vendor        : Sparemint

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.redhat.com/pub/redhat/code/logrotate/logrotate-%{version}.tar.gz
Patch0: logrotate-mint.patch
Patch1: logrotate-3.5.9-install.patch


%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  Logrotate
allows for the automatic rotation, compression, removal and mailing of
log files.  Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.  Normally, logrotate
runs as a daily cron job.

Install the logrotate package if you need a utility to deal with the log
files on your system.

%description -l de
Das Logrotate-Werkzeug wurde entwickelt, um die Verwaltung von Logdateien
(Protokolldateien) auf Systemen, die davon eine Menge erzeugen, zu 
vereinfachen.  Logrotate ermöglicht die automatische Rotation, Kompression, 
Entfernung und Versendung per E-Mail von Logdateien.  Logrotate kann so
konfiguriert werden, dass es Logdateien täglich, wöchentlich, monatlich,
oder wenn die Logdatei eine bestimmte Größe überschreitet, verarbeitet.
Normalerweise wird Logrotate aus einem täglich ablaufenden Cron-Auftrag
gestartet.

Das Logrotate-Paket sollte installiert werden, wenn ein Werkzeug für
die Behandlung der Logdateien des Systems benötigt werden.


%prep
%setup -q
%patch0 -p1 -b .mint
%patch1 -p1 -b .install


%build
make RPM_OPT_FLAGS="${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	PREFIX=${RPM_BUILD_ROOT} \
	BINDIR=%{_prefix}/sbin \
	MANDIR=%{_prefix}/share/man

mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
mkdir -p ${RPM_BUILD_ROOT}/etc/cron.daily

install -m 644 examples/logrotate-default ${RPM_BUILD_ROOT}/etc/logrotate.conf
install -m 755 examples/logrotate.cron ${RPM_BUILD_ROOT}/etc/cron.daily/logrotate

strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%attr(0755, root, root) %{_prefix}/sbin/logrotate
%attr(0644, root, root) %{_prefix}/share/man/man*/*
%attr(0755, root, root) /etc/cron.daily/logrotate
%attr(0644, root, root) %config /etc/logrotate.conf
%attr(0755, root, root) %dir /etc/logrotate.d


%changelog
* Fri Sep 28 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 3.5.9
