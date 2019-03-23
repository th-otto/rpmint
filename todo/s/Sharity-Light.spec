Summary       : Sharity-Light - remount samba exports as NFS
Name          : Sharity-Light
Version       : 1.2
Release       : 5
Copyright     : GPL
Group         : System Environment/Daemons

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.obdev.at/Products/

Conflicts     : Sharity

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz
Patch0: Sharity-Light-1.2-mint.patch
Patch1: Sharity-Light-1.2-syslog.patch


%description
If you know smbfs for Linux: Sharity-Light is roughly the same. It is
derived from smbfs, but runs as a user level program, not in the kernel.
If you know samba: Sharity-Light is roughly the opposite: a client for the
Lanmanager protocol. If you know neither of these: Sharity-Light lets you
mount drives exported by Windows (f.Workgroups/95/NT), Lan Manager, OS/2
etc. on Unix machines.

Sharity-Light has previously been called rumba. However, it turned out that
Wall Data Incorporated owns the trademark "RUMBA". To avoid confusion and
a violation of the trademark rights, the program has been renamed to
"Sharity-Light". The name has been chosen because Sharity-Light implements
the same protocol (CIFS/SMB) as the more professional program "Sharity",
which is also available from our web site at

    http://www.obdev.at/Products/Sharity.html


%prep
%setup -q
%patch0 -p1 -b .mint
%patch1 -p1 -b .syslog


%build 
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

install -m755 shlight ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m755 unshlight.sh ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m644 smbmount.8 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/shlight.8

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files 
%defattr(-,root,root)
%doc Changelog Copying FAQ.txt README
%{_prefix}/bin/*
%{_prefix}/share/man/man*/*


%changelog
* Wed Mar 06 2002 Frank Naumann <fnaumann@freemint.de>
- increased the stacksize a little bit; this fixes some timeout problems

* Wed Feb 27 2002 Frank Naumann <fnaumann@freemint.de>
- better syslog output, small bugfix failed mounts

* Tue Feb 26 2002 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
