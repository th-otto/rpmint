Summary       : Utilities for TCP programming in shell-scripts.
Name          : tcputils
Version       : 0.6.2
Release       : 1
Copyright     : BSD
Group         : Base System/Networking

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Requires      : freemint-net

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: tcputils-%{version}.tar.gz
Patch0: tcputils-0.6.2-mint.patch


%description
This is a collection of programs to facilitate TCP programming
in shell-scripts.  There is also a small library which makes it
somewhat easier to create TCP/IP sockets.

The programs included in this release are:

  fionread    - do FIONREAD ioctl on stdin
  fstat       - do fstat ytem call on stdin
  mini-inetd  - small TCP/IP connection dispatcher
  tcpbug      - TCP/IP connection bugging device
  tcpconnect  - general TCP/IP client
  tcplisten   - general TCP/IP server
  getpeername - get name of connected TCP/IP peer


%prep
%setup -q
%patch0 -p1 -b .orig


%build
make
make fionread
make fstat


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1

install -m755 fionread    ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m755 fstat       ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m755 getpeername ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m755 mini-inetd  ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m755 tcpbug      ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m755 tcpconnect  ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m755 tcplisten   ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m444 *.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/

# strip anything
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,0755)
%doc README
%{_prefix}/bin/*
%{_prefix}/share/man/man*/*


%changelog
* Fri Sep 29 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
