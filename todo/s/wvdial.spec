Summary       : A heuristic autodialer for PPP connections.
Name          : wvdial
Version       : 1.41
Release       : 2
Copyright     : LGPL
Group         : System Environment/Daemons

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.worldvisions.ca/wvdial/

Requires      : ppp >= 2.3.7

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.worldvisions.ca/wvdial/wvdial-%{version}.tar.gz
Patch0: wvdial-1.41-libs.patch
Patch1: wvdial-1.41-mint.patch


%description
WvDial automatically locates and configures modems and can log into
almost any ISP's server without special configuration. You need to
input the username, password, and phone number, and then WvDial will
negotiate the PPP connection using any mechanism needed.

Install wvdial if you need a utility to configure your modem and set
up a PPP connection.


%prep
%setup -q
%patch0 -p1 -b .rhconf
%patch1 -p1 -b .mint


%build
make PREFIX=%{_prefix} \
	RPM_OPT_FLAGS="-O" \
	LIBS=-lsocket


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install PREFIX=${RPM_BUILD_ROOT}%{_prefix} PPPDIR=${RPM_BUILD_ROOT}/etc/ppp/peers

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc ANNOUNCE CHANGES* COPYING* README* TODO
%attr(0600,root,daemon)	%config /etc/ppp/peers/wvdial
%attr(0755,root,root)	%{_prefix}/bin/*
%attr(0644,root,root)	%{_prefix}/share/man/man1/*


%changelog
* Mon Jan 08 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
