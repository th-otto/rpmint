Summary       : Security wrapper for tcp daemons
Summary(de)   : Sicherheitspackung für tcp-Dämonen 
Summary(fr)   : Enveloppe de sécurité pour les démons tcp
Summary(tr)   : TCP süreçleri için güvenlik sarmalayýcýsý
Name          : tcp_wrappers
Version       : 7.6
Release       : 3
Copyright     : Distributable
Group         : Base System/Networking

Packager      : John Blakeley <johnnie@ligotage.demon.co.uk>
Vendor        : Sparemint

Requires      : freemint-net

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: tcp_wrappers_7.6.tar.gz
Patch0: tcpw7.2-config.patch
Patch1: tcpw7.2-setenv.patch
Patch2: tcpw7.6-freemint.patch


%description
With this package you can monitor and filter incoming requests for the
SYSTAT, FINGER, FTP, TELNET, RLOGIN, RSH, EXEC, TFTP, TALK, and other
network services.

Please note: to rebuild this, you will need patches for the mintlib.
Please contact the packager.

%description -l fr
Avec ce paquetage, vous pouvez gérer et filtrer les requêtes entrantes pour
SYSTAT, FINGER, FTP, TELNET, RLOGIN, RSH, EXEC, TFTP, TALK et autres services
réseau.

%description -l tr
Bu paket, SYSTAT, FINGER, FTP, TELNET, RLOGIN, RSH, EXEC, TFTP, TALK ve diðer
að hizmetleri için gelen istekleri izlemenizi ve isteðinize göre süzmenizi
saðlar.


%prep
%setup -q -n tcp_wrappers_7.6
%patch0 -p1 -b .config
%patch1 -p1 -b .setenv
%patch2 -p1 -b .freemint


%build
make freemint


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/include
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man3
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

install -m 644 hosts_access.3 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man3
install -m 644 hosts_access.5 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5
install -m 644 hosts_options.5 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5
install -m 644 tcpd.8 tcpdchk.8 tcpdmatch.8 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

echo ".so man5/hosts_access.5.gz" >${RPM_BUILD_ROOT}%{_prefix}/share/man/man5/hosts.allow.5
echo ".so man5/hosts_access.5.gz" >${RPM_BUILD_ROOT}%{_prefix}/share/man/man5/hosts.deny.5
chmod 644 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5/hosts.allow.5
chmod 644 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5/hosts.deny.5

install -m 644 libwrap.a ${RPM_BUILD_ROOT}%{_prefix}/lib
install -m 644 tcpd.h ${RPM_BUILD_ROOT}%{_prefix}/include

install -m 755 safe_finger ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m 755 tcpd ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m 755 tcpdchk ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m 755 tcpdmatch ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m 755 try-from ${RPM_BUILD_ROOT}%{_prefix}/sbin

strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc BLURB CHANGES README* DISCLAIMER Banners.Makefile
%{_prefix}/include/*
%{_prefix}/lib/*
%{_prefix}/sbin/*
%{_prefix}/share/man/man*/*


%changelog
* Tue Sep 25 2001 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.57

* Sat Apr 01 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Mon Jan 31 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- First release for Sparemint.
