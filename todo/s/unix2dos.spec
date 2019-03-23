Summary      : unix2dos - UNIX to DOS text file format converter
Name         : unix2dos
Version      : 2.2
Release      : 1
Copyright    : distributable
Group        : Applications/Text

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: unix2dos-%{version}.src.tar.gz
Patch0: unix2dos-mkstemp.patch


%description
A utility that converts plain text files in UNIX format to DOS format.


%prep
%setup -q -c
%patch -p1


%build
gcc $RPM_OPT_FLAGS -o unix2dos unix2dos.c


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/{bin,share/man/man1}

install -m755 unix2dos ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m444 unix2dos.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* |:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,0755)
%doc COPYRIGHT
%{_prefix}/bin/unix2dos
%{_prefix}/share/man/*/*


%changelog
* Thu Sep 06 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
