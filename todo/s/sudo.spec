Summary: Allows restricted root access for specified users.
Name: sudo
Version: 1.5.9p1
Release: 1
Copyright: GPL
Group: Applications/System
Source: ftp://ftp.cs.colorado.edu/pub/sudo/cu-sudo.v%{version}.tar.gz
URL: http://www.courtesan.com/sudo/
Patch0: sudo-1.5.9-fixvi.patch
Patch1: sudo-mintcnf.patch
Patch2: sudo-mint.patch
BuildRoot: /var/tmp/%{name}-root
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): Erlaube begrenzten Superuser-Zugriff für bestimmte Benutzerinnen.
Prefix: %{_prefix}

%description
Sudo (superuser do) allows a system administrator to give certain
users (or groups of users) the ability to run some (or all) commands
as root while logging all commands and arguments. Sudo operates on a
per-command basis.  It is not a replacement for the shell.  Features
include:  the ability to restrict what commands a user may run on a
per-host basis, copious logging of each command (providing a clear audit
trail of who did what), a configurable timeout of the sudo command, and
the ability to use the same configuration file (`sudoers') on many
different machines.

%description -l de
Sudo (superuser do) erlaubt dem SysAdmin, bestimmten Benutzerinnen (oder
Gruppen von Benutzern), die Rechte zu erteilen, einige (oder alle) Kommandos
als Root auszuführe, und protokolliert alle Kommandos und Argumente mit.
Sudo arbeitet auf einer Per-Kommando-Basis.  Es ist kein Ersatz für die 
Shell. Weitere Fähigkeiten sind unter anderem: Die Möglichkeit, die
erlaubten für eine Benutzerin erlaubten Kommandos auf einer Per-Host-Basis
zu begrenzen, ausschweifende Protokollierung aller Kommandos (inklusive
einer klaren Auflistung, wer was getan hat), ein konfigurierbares Timeout
des Sudo-Kommandos und die Möglichkeit, ein und dieselbe Konfigurationsdatei
(»sudoers«) auf vielen verschiedenen Maschinen zu benutzen.

%prep
%setup -q -n sudo.v%{version}
%patch0 -p1 -b .fixvi
%patch1 -p1 -b .mintcnf
%patch2 -p1 -b .mint

%build
# FIXME: Add "--with-pam" here.
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-static" \
./configure \
	--prefix=%{_prefix} \
	--sbindir=%{_prefix}/sbin \
	--with-libraries=-lport \
	--with-logging=syslog \
	--with-logfac=LOG_AUTH \
	--with-env-editor \
	--with-ignore-dot \
	--with-tty-tickets \
	--with-insults \
	--with-all-insults
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

make \
	prefix="$RPM_BUILD_ROOT%{_prefix}" \
	sbindir="$RPM_BUILD_ROOT%{_prefix}/sbin" \
	sysconfdir="$RPM_BUILD_ROOT/etc" \
	install
install -d -m 700 -o 0 -g 0 $RPM_BUILD_ROOT/var/run/sudo

#mkdir -p $RPM_BUILD_ROOT/etc/pam.d
#cat > $RPM_BUILD_ROOT/etc/pam.d/sudo << EOF
##%PAM-1.0
#auth       required	/lib/security/pam_pwdb.so shadow nullok
#account    required	/lib/security/pam_pwdb.so
#password   required	/lib/security/pam_cracklib.so
#password   required	/lib/security/pam_pwdb.so shadow use_authtok nullok
#session    required	/lib/security/pam_pwdb.so
#EOF

gzip -9nf $RPM_BUILD_ROOT%{_prefix}/man/man*/*

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BUGS CHANGES COPYING FAQ HISTORY README RUNSON TODO TROUBLESHOOTING *.pod
%config /etc/sudoers
%dir /var/run/sudo
%{_prefix}/bin/sudo
%{_prefix}/sbin/visudo
%{_prefix}/man/man5/sudoers.5.gz
%{_prefix}/man/man8/sudo.8.gz
%{_prefix}/man/man8/visudo.8.gz

%changelog
* Wed Sep 15 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Initial version for Sparemint.
