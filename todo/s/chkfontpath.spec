Summary       : Simple interface for editing the font path for the X font server.
Name          : chkfontpath
Version       : 1.7
Release       : 2
Copyright     : GPL
Group         : System Environment/Base

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Requires      : XFree86-xfs

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz


%description 
This is a simple terminal mode program for configuring the directories
in the X font server's path. It is mostly intended to be used
`internally' by RPM when packages with fonts are added or removed, but
it may be useful as a stand-alone utility in some instances.


%prep
%setup -q


%build
make RPM_OPT_FLAGS="${RPM_OPT_FLAGS}"


%install
rm -rf ${RPM_BUILD_ROOT}

make INSTROOT=${RPM_BUILD_ROOT} install
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*
strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_prefix}/sbin/chkfontpath
%{_prefix}/share/man/man8/*


%changelog
* Mon Dec 18 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
