Summary       : A simple getty.
Name          : gogetty
Version       : 0.1.6
Release       : 1
License       : GPL
Group         : Utilities/Terminal

URL	      : http://web.onetel.net.uk/~elephant/john/programs/linux/gogetty/download/gogetty-%{version}.tar.gz
Patch0: %{name}-%{version}.mint.patch
 
Packager      : Marc-Anton Kehr <m.kehr@ndh.net>
Vendor        : Sparemint

Requires      : bash

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : /tmp/%{name}-root

Source: gogetty-%{version}.tar.gz


%description
gogetty is a simple getty for software terminals.
It can be used to start login or a fully functional shell on
one terminal from another, and correctly handles session ids.

%prep
%setup -q
%patch -p1

./configure --prefix=/usr

%build
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/usr/sbin
install gogetty $RPM_BUILD_ROOT/usr/sbin/gogetty
install login-agent $RPM_BUILD_ROOT/usr/sbin/login-agent
strip $RPM_BUILD_ROOT/usr/sbin/*



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc AUTHORS
%doc COPYING
%doc INSTALL
%doc README
%doc NEWS
%doc TODO
/usr/sbin/gogetty
/usr/sbin/login-agent


%changelog
* Mon Mar 10 2003 M.A. Kehr <m.kehr@ndh.net>
- initial Sparemint release

