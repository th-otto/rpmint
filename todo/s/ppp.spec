Summary: The PPP daemon and documentation.
Name: ppp
Version: 2.3.11
Release: 2
Copyright: distributable
Group: System Environment/Daemons
URL: ftp://ftp.linuxcare.com.au/pub/ppp/
Source: ftp://ftp.linuxcare.com.au/pub/ppp/ppp-%{version}.tar.gz
Patch0: ppp-2.3.11-mint.patch
Packager: Frank Naumann <fnaumann@freemint.de>
Vendor: Sparemint
Prefix: %{_prefix}
Docdir: %{_prefix}/doc
BuildRoot: %{_tmppath}/%{name}-root

%description
The ppp package contains the PPP (Point-to-Point Protocol) daemon
and documentation for PPP support.  The PPP protocol provides a
method for transmitting datagrams over serial point-to-point links.

The ppp package should be installed if your machine need to support
the PPP protocol.

%prep
%setup  -q
%patch0 -p1

%build
./configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install TOPDIR=$RPM_BUILD_ROOT

## it shouldn't be SUID root be default
#chmod 755 $RPM_BUILD_ROOT%{_prefix}/sbin/pppd

strip $RPM_BUILD_ROOT%{_prefix}/sbin/* ||:
chmod 644 scripts/*

mkdir -p $RPM_BUILD_ROOT%{_prefix}/share
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_prefix}/share/
gzip -9nf $RPM_BUILD_ROOT%{_prefix}/share/man/*/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README README.mint scripts sample
%attr(0755,root,root)	%{_prefix}/sbin/chat
%attr(0755,root,root)	%{_prefix}/sbin/pppd
%attr(0755,root,daemon)	%{_prefix}/sbin/pppdump
%attr(0644,root,root)	%{_prefix}/share/man/man8/chat.8.gz
%attr(0644,root,root)	%{_prefix}/share/man/man8/pppd.8.gz
%attr(0644,root,daemon)	%{_prefix}/share/man/man8/pppdump.8.gz
%attr(0755,root,root)	%dir /etc/ppp
%attr(0600,root,daemon)	%config /etc/ppp/chap-secrets
%attr(0644,root,daemon)	%config /etc/ppp/options
%attr(0600,root,daemon)	%config /etc/ppp/pap-secrets

%changelog
* Fri Nov 24 2000 Frank Naumann <fnaumann@freemint.de>
- reduce stack size to 64k
- compressed manpages

* Fri May 19 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
