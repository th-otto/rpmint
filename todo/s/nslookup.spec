Summary       : The nslookup command.
Name          : nslookup
Version       : 5.42
Release       : 2
Copyright     : BSD
Group         : Base System/Networking

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Requires      : freemint-net
Conflicts     : bind, bind-utils

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: nslookup-%{version}.tar.gz


%description
The nslookup command.


%prep
%setup -q


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

install -m755 nslookup ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m444 nslookup.8 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,0755)
%{_prefix}/bin/*
%{_prefix}/share/man/*/*


%changelog
* Tue Sep 25 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
