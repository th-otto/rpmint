Summary       : Battleships against the computer (character-cell graphics)
Name          : bs
Version       : 2.6
Release       : 2
License       : GPL
Group         : Games

Packager      : Keith Scroggins <kws@radix.net>
Vendor        : Sparemint
URL           : http://www.catb.org/~esr/bs/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz
Patch: bs-2.6-make.patch


%description
The classic game of Battleships against the computer.
Uses character-cell graphics with a visual point-and-shoot interface.
If you're using an xterm under Linux the mouse will work.


%prep
%setup -q
%patch0 -p 1


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	DESTDIR="${RPM_BUILD_ROOT}" \
	mandir=%{_prefix}/share/man

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc READ.ME COPYING
%{_prefix}/bin/bs
%{_prefix}/share/man/man*/*


%changelog
* Tue Jan 13 2004 Frank Naumann <fnaumann@freemint.de>
- corrected specfile for Sparemint

* Mon Dec 29 2003 Keith Scroggins <kws@radix.net>
- Initial build for MiNT
