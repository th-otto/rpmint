Summary       : The ping command.
Name          : ping
Version       : 20010219
Release       : 2
Copyright     : BSD
Group         : Base System/Networking

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://cvsweb.netbsd.org/bsdweb.cgi/basesrc/sbin/ping/

Requires      : freemint-net

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ping-%{version}.tar.gz
Patch0: ping-20010219-mint.patch


%description
The ping command.


%prep
%setup -q
%patch0 -p1 -b .orig


%build
gcc -o ping -Wall ping.c -lm -lsocket


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

install -m4555 ping ${RPM_BUILD_ROOT}/sbin/
install -m444 ping.8 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/

strip ${RPM_BUILD_ROOT}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,0755)
/sbin/*
%{_prefix}/share/man/*/*


%changelog
* Tue Oct 02 2001 Frank Naumann <fnaumann@freemint.de>
- corrected wrong mode bits for the ping tool

* Tue Sep 25 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
