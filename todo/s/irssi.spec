Summary       : IRC-Client. Mixture of bitchX and IRCII
Name          : irssi
Version       : 0.8.4
Release       : 2
Copyright     : GPL
Group         : Applications/Internet

Packager      : Daniel Pralle <pralle@informatik.uni-hannover.de>
Vendor        : Sparemint
URL           : http://www.irssi.org/

Requires      : perl ncurses
BuildRequires : perl ncurses-devel glib

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.irssi.org/files/irssi-%{version}.tar.gz


%description
IRSSI is client program for IRC (Internet Relay Chat). It is text-console
based like ircII, but has some nice automatizations.

Install irssi if you need a simple to use IRC-Client for console.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=/etc \
	--disable-shared \
	--disable-etags

make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	PREFIX=${RPM_BUILD_ROOT}%{_prefix} \
	sysconfdir=${RPM_BUILD_ROOT}/etc

# strip binaries
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING NEWS README TODO
%doc %{_prefix}/share/doc/irssi
/etc/irssi.conf
%attr(0755,root,root) %{_prefix}/bin/*
%{_prefix}/share/irssi


%changelog
* Fri Apr 26 2002 Daniel Pralle <pralle@informatik.uni-hannover.de>
- updated description

* Thu Apr 25 2002 Daniel Pralle <pralle@informatik.uni-hannover.de>
- initial Sparemint release
