Summary       : old ps/top tool
Name          : pstop
Version       : 1.0
Release       : 1
Copyright     : Freeware
Group         : System Environment/Base

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://sparemint.atari.org/

Requires      : /bin/bash

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: pstop-%{version}.tar.gz


%description
This package include the KGMD ps and top tools. This package
will be hopefully replaced in the enar future by more modern
replacements.


%prep
%setup -q


%build


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/bin

install -m 755 ps  ${RPM_BUILD_ROOT}/bin
install -m 755 top ${RPM_BUILD_ROOT}/bin


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
/bin/*


%changelog
* Wed Nov 14 2001 Frank Naumann <fnaumann@freemint.de>
- first release
