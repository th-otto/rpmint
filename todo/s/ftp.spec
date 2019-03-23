Summary       : The standard UNIX FTP (File Transfer Protocol) client.
Name          : ftp
Version       : 0.17
Release       : 2
Copyright     : BSD
Group         : Applications/Internet

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.uk.linux.org/pub/linux/Networking/netkit-devel/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

%define	_snapshot -pre20000412

Source: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit-devel/netkit-ftp-%{version}%{_snapshot}.tar.gz
Patch0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit-devel/netkit-combo-0.16-SECURITY.patch
Patch1: netkit-ftp-0.17-pre20000412.pasv-security.patch
Patch2: netkit-ftp-0.17-pre20000412-mint.patch


%description
The ftp package provides the standard UNIX command-line FTP (File
Transfer Protocol) client.  FTP is a widely used protocol for
transferring files over the Internet and for archiving files.

If your system is on a network, you should install ftp in order to do
file transfers.


%prep
%setup -q -n netkit-ftp-%{version}%{_snapshot}
%patch0 -p2
%patch1 -p1
%patch2 -p1 -b .mint


%build
CFLAGS="${RPM_OPT_FLAGS}" \
LIBS=-lsocket \
./configure

perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS),;
    s,^BINDIR=.*$,BINDIR=%{_prefix}/bin,;
    s,^MANDIR=.*$,MANDIR=%{_prefix}/share/man,;
    s,^SBINDIR=.*$,SBINDIR=%{_prefix}/sbin,;
    ' MCONFIG

make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5

make INSTALLROOT=${RPM_BUILD_ROOT} install

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:

# fix symlinks
( cd ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1;
  for file in *.1; do \
    echo "processing $file ..."; \
    target=`readlink $file`; \
    ln -s $target.gz $file.gz; \
    rm $file; \
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_prefix}/bin/ftp
%{_prefix}/bin/pftp
%{_prefix}/share/man/man1/ftp.*
%{_prefix}/share/man/man1/pftp.*
%{_prefix}/share/man/man5/netrc.*


%changelog
* Wed Apr 04 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
