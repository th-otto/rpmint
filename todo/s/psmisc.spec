Summary       : Utilities for managing processes on your system.
Name          : psmisc
Version       : 19
Release       : 3
Copyright     : distributable
Group         : Applications/System

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://lrcftp.epfl.ch/pub/linux/local/psmisc/psmisc-%{version}.tar.gz
Patch0: psmisc-mint.patch


%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.


%prep
%setup -q -n psmisc
%patch0 -p1 -b .mint


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1

install -m 0755 killall ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m 0755 pstree ${RPM_BUILD_ROOT}%{_prefix}/bin/

install -m 644 killall.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/
install -m 644 pstree.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/

ln ${RPM_BUILD_ROOT}%{_prefix}/bin/killall ${RPM_BUILD_ROOT}%{_prefix}/bin/pidof
install -m 644 pidof.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc CHANGES COPYING README
%{_prefix}/bin/*
%{_prefix}/share/*/*


%changelog
* Wed Nov 14 2001 Frank Naumann <fnaumann@freemint.de>
- added workarounds for buggy kernel versions

* Fri Sep 07 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
