Summary       : A nice X11 demo or screensaver.
Name          : xswarm
Version       : 2.3
Release       : 1
Copyright     : MIT
Group         : Amusements/Graphics

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

BuildRequires : XFree86-devel
Requires      : XFree86

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz


%description
The well known xswarm screensaver or X11 demo program. Similiar
to ATARI's lines.app that was shipped with MultiTOS.

Author:
--------
    Jeff Butterworth <butterwo@cs.unc.edu>


%prep
%setup -q


%build
xmkmf -a
make


%install
rm -rf ${RPM_BUILD_ROOT}

make DESTDIR=${RPM_BUILD_ROOT} install install.man

strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/*/*


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README
%{_prefix}/X11R6/bin/xswarm
%{_prefix}/X11R6/man/man1/xswarm.1x*


%changelog
* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
