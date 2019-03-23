Summary       : A utility to set/show the host name or domain name
Name          : hostname
Version       : 2.07
Release       : 1
Copyright     : GPL
Group         : Base System/Networking

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://packages.debian.org/stable/base/hostname.html

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: hostname-%{version}.tar.gz
Patch0: hostname-2.07-mint.patch


%description
The hostname command can be used to either set or display the current
host or domain name of the system. This name is used by many of the
networking programs to identify the machine.


%prep
%setup -q
%patch0 -p1 -b .orig


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/{bin,%{_prefix}/share/man/man1}

install -m755 hostname ${RPM_BUILD_ROOT}/bin/
install -m755 dnsdomainname ${RPM_BUILD_ROOT}/bin/

install -m444 man/en_US.88591/hostname.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/
install -m444 man/en_US.88591/dnsdomainname.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/

# domainname link
ln ${RPM_BUILD_ROOT}/bin/hostname ${RPM_BUILD_ROOT}/bin/domainname
install -m444 man/en_US.88591/dnsdomainname.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/domainname.1

strip ${RPM_BUILD_ROOT}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,0755)
%doc COPYRIGHT
/bin/*
%{_prefix}/share/man/*/*


%changelog
* Fri Sep 07 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
