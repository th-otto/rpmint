Summary       : The client program for the telnet remote login protocol.
Name          : telnet
Version       : 0.1
Release       : 1
Copyright     : BSD
Group         : Applications/Internet

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Requires      : freemint-net netbase

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: telnet-0.1.tar.gz


%description
Telnet is a popular protocol for logging into remote systems over the
Internet.  The telnet package provides a command line telnet client.

Install the telnet package if you want to telnet to remote machines.

%package server
Summary       : The server program for the telnet remote login protocol.
Group         : System Environment/Daemons
Requires      : inetd

%description server
Telnet is a popular protocol for logging into remote systems over the
Internet.  The telnet-server package  a telnet daemon, which will
support remote logins into the host machine.  The telnet daemon is
disabled by default.  You may enable the telnet daemon by editing
/etc/inetd.conf, uncomment the telnet configuration line and restart
the inetd.

Install the telnet-server package if you want to support remote logins
to your own machine.


%prep
%setup -q


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

install -m 755 telnet/telnet ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m 444 telnet/telnet.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/

install -m 755 telnetd/telnetd ${RPM_BUILD_ROOT}%{_prefix}/sbin/in.telnetd
install -m 444 telnetd/telnetd.8 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/in.telnetd.8

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_prefix}/bin/telnet
%{_prefix}/share/man/man1/telnet.1*

%files server
%defattr(-,root,root)
%{_prefix}/sbin/in.telnetd
%{_prefix}/share/man/man8/in.telnetd.8*


%changelog
* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
