Summary       : Arc archiver 
Name          : arc
Version       : 5.21e
Release       : 2
License       : distributable 
Group         : Applications/Archiving

Packager      : Jan Krupka <jkrupka@volny.cz>
Vendor        : Sparemint

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.freebsd.org/pub/FreeBSD/distfiles/arc521e.pl8.tar.Z
Patch: arc-5.21e-timeh.patch

%description
Arc file archiver and compressor. Long since superseded by zip/unzip
but useful if you have old .arc files you need to unpack.


%prep
%setup -c -q
%patch -p1


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

install -m 755 -d ${RPM_BUILD_ROOT}%{_prefix}/bin
install -m 755 -d ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1

install -m 755 arc ${RPM_BUILD_ROOT}%{_prefix}/bin/arc
install -m 755 marc ${RPM_BUILD_ROOT}%{_prefix}/bin/marc
install arc.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/arc.1

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-, root, root, 0755)
%doc Arc521.doc Arcinfo Changes.521 README
%{_prefix}/bin/*
%{_prefix}/share/man/man*/*


%changelog
* Mon Jun 21 2004 Jan Krupka <jkrupka@volny.cz>
- Initial package.
