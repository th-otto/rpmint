Summary       : Tool for getting the date/time from another machine on your network.
Name          : rdate
Version       : 1.0
Release       : 1
Copyright     : GPL
Group         : Applications/System

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://people.redhat.com/sopwith/

Requires      : freemint-net

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://people.redhat.com/sopwith/rdate-%{version}.tar.gz
Patch1: rdate-1.0.returnvalue.patch
Patch2: rdate-1.0.service.patch


%description
The rdate utility retrieves the date and time from another machine on
your network, using the protocol described in RFC 868.  If you run
rdate as root, it will set your machine's local time to the time of
the machine that you queried.  Note that rdate isn't scrupulously
accurate.  If you are worried about milliseconds, install the xntp3
package, which includes the xntpd daemon, instead.


%prep
%setup -q
%patch1 -p1 -b .returnvalue
%patch2 -p1 -b .service


%build
make CFLAGS="${RPM_OPT_FLAGS} -lsocket -liio"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
install -c rdate ${RPM_BUILD_ROOT}%{_prefix}/bin/

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
install -c rdate.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_prefix}/bin/rdate
%{_prefix}/share/man/man1/rdate.1*


%changelog
* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
