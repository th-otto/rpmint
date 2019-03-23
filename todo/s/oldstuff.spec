Summary       : old MiNT Utilities
Name          : oldstuff
Version       : 1.0
Release       : 3
Copyright     : Freeware
Group         : System Environment/Base

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://sparemint.atari.org/

Requires      : /bin/bash
Conflicts     : mintinit

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: oldstuff-%{version}.tar.gz


%description
This package include some old tools that arn't available as modern
rpm replacements yet. This include init, reboot and such things.


%prep
%setup -q


%build


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/sbin
mkdir -p ${RPM_BUILD_ROOT}/%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}/%{_prefix}/sbin

install -m 755 init     ${RPM_BUILD_ROOT}/sbin
install -m 755 reboot   ${RPM_BUILD_ROOT}/sbin
install -m 755 shutdown ${RPM_BUILD_ROOT}/sbin

install -m 755 execgem  ${RPM_BUILD_ROOT}/sbin
install -m 755 execmtos ${RPM_BUILD_ROOT}/sbin

install -m 755 last     ${RPM_BUILD_ROOT}%{_prefix}/bin
install -m 755 getty    ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m 644 gettytab ${RPM_BUILD_ROOT}/etc
install -m 644 ttytab   ${RPM_BUILD_ROOT}/etc


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
/etc/*
/sbin/*
%{_prefix}/bin/*
%{_prefix}/sbin/*


%changelog
* Wed Nov 14 2001 Frank Naumann <fnaumann@freemint.de>
- first release
