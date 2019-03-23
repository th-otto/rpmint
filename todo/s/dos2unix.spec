Summary       : Text file format converter
Name          : dos2unix
Version       : 3.1
Release       : 1
Copyright     : Freely distributable
Group         : Applications/Text

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: dos2unix-%{version}.tar.gz
Patch0: dos2unix-3.1.patch


%description
Dos2unix converts DOS or MAC text files to UNIX format.


%prep
%setup -q
%patch0 -p1 -b .orig


%build
make clean
make CFLAGS="${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/{bin,share/man/man1}

install -m755 dos2unix ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m444 dos2unix.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* |:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,0755)
%doc COPYRIGHT
%{_prefix}/bin/dos2unix
%{_prefix}/share/man/*/*


%changelog
* Thu Sep 06 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
