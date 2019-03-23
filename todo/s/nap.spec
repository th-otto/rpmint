Summary       : A Ncurses based Napster Clone
Name          : nap
Version       : 1.4.4
Release       : 1
Copyright     : distributable
Group         : Applications/Internet

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.gis.net/~nite/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://download.sourceforge.net/nap/%{name}-%{version}.tar.gz
Patch0: nap-1.4.4-mint.patch


%description
This is a clone of napster using the ncurses library.


%prep
%setup -q
%patch0 -p1 -b .mint


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}
make
cp nap.conf.dist nap.conf


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=${RPM_BUILD_ROOT}%{_prefix}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%doc nap.conf
%{_prefix}/bin/*


%changelog
* Thu Jan 09 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
