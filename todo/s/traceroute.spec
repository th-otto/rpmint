Summary       : Traces the route taken by packets over a TCP/IP network.
Name          : traceroute
Version       : 1.4a5
Release       : 1
Copyright     : BSD
Group         : Applications/Internet

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.ee.lbl.gov/

Requires      : freemint-net

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.ee.lbl.gov/traceroute-1.4a5.tar.Z
Patch0: traceroute-1.4a5-fix.patch
Patch1: traceroute-1.4a5-secfix.patch
Patch2: traceroute-1.4a5-alpha.patch
Patch3: traceroute-1.4a5-autoroute.patch
Patch4: traceroute-1.4a5-autoroute2.patch
Patch5: traceroute-1.4a5-unaligned.patch
Patch6: traceroute-1.4a5-llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch.patch
Patch7: traceroute-1.4a5-fhs.patch
Patch8: traceroute-1.4a5-sourceroute.patch
Patch9: traceroute-1.4a5-aliases.patch
Patch10: traceroute-1.4a5-droproot.patch
Patch11: traceroute-1.4a5-bigpacklen.patch
Patch12: traceroute-1.4a5-lsrr.patch
Patch13: traceroute-1.4a5-mint.patch


%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.  Traceroute displays
the IP number and host name (if possible) of the machines along the
route taken by the packets.  Traceroute is used as a network debugging
tool.  If you're having network connectivity problems, traceroute will
show you where the trouble is coming from along the route.

Install traceroute if you need a tool for diagnosing network connectivity
problems.


%prep
%setup -q
%patch0 -p1 -b .fix
%patch1 -p1 -b .secfix
%patch2 -p1 -b .alpha
%patch3 -p1 -b .autoroute
%patch4 -p1 -b .autoroute2
%patch5 -p1 -b .unaligned
%patch6 -p1 -b .hostname
%patch7 -p1 -b .fhs
%patch8 -p1 -b .sourceroute
%patch9 -p1 -b .aliases
%patch10 -p1 -b .droproot
%patch11 -p1 -b .bigpacklen
%patch12 -p1 -b .lsrr
%patch13 -p1 -b .mint

cp /usr/lib/rpm/config.guess .
cp /usr/lib/rpm/config.sub .


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

make install install-man \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

strip ${RPM_BUILD_ROOT}%{_sbindir}/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc CHANGES README
%attr(4755,root,root) %{_prefix}/sbin/*
%attr(644,root,root) %{_prefix}/share/man/man*/*


%changelog
* Tue Sep 25 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
