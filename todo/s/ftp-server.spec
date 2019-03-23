Summary       : The server program for the ftp protocol.
Name          : ftp-server
Version       : 0.4
Release       : 1
Copyright     : BSD
Group         : System Environment/Daemons

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Requires      : freemint-net netbase inetd

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp-server-0.4.tar.gz


%description
FTP is a popular protocol for uploading and downloading files to
the host system over the Internet.  The ftp-server package is a ftp
daemon, which will support remote ftp into the host machine.  The
ftp daemon is disabled by default.  You may enable the ftp daemon by
editing /etc/inetd.conf, uncomment the ftpd configuration line and
restart the inetd.

Install the ftp-server package if you want to support ftp logins
to your own machine.


%prep
%setup -q


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

install -m 755 ftpd ${RPM_BUILD_ROOT}%{_prefix}/sbin/in.ftpd
install -m 444 ftpd.8 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/in.ftpd.8

strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%{_prefix}/sbin/in.ftpd
%{_prefix}/share/man/man8/in.ftpd.8*


%changelog
* Wed Feb 06 2002 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
