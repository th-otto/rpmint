Summary       : lrzsz - sz, rz, and friends
Name          : lrzsz
Version       : 0.12.20
Release       : 1
Copyright     : GPL
Group         : Applications/Communications

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.ohse.de/uwe/releases/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source : ftp://ftp.ohse.de/uwe/releases/%{name}-%{version}.tar.gz


%description
This collection of commands can be used to download and upload
files using the Z, X, and Y protocols.  Many terminal programs
(like minicom) make use of these programs to transfer files.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--program-transform-name=s/l//
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make prefix=${RPM_BUILD_ROOT}%{_prefix} install

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/{rb,rx,rz,sb,sx,sz} ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/{rb,rx,rz,sb,sx,sz} ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/*/*

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc AUTHORS COMPATABILITY ChangeLog NEWS README README.gettext
%doc TODO THANKS README.cvs README.isdn4linux README.tests
%{_prefix}/bin/sz
%{_prefix}/bin/sb
%{_prefix}/bin/sx
%{_prefix}/bin/rz
%{_prefix}/bin/rb
%{_prefix}/bin/rx
%{_prefix}/share/man/man1/sz.1.gz
%{_prefix}/share/man/man1/rz.1.gz


%changelog
* Wed Mar 14 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
