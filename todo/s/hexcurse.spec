Name          : hexcurse
Summary       : Binary Hexadecimal Editor
Version       : 1.55
Release       : 2
Copyright     : GPL
Group         : Applications/Editors

Packager      : Keith Scroggins <kws@radix.net>
Vendor        : Sparemint
URL           : http://jewfish.net/description.php?title=HexCurse

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source        : %{name}-%{version}.tar.gz

%description
Hexcurse is a versatile ncurses-based hex editor written in C that
provides the user with many features. It currently supports searching, hex
and decimal address output, jumping to specified locations in the file, an
"undo" command, "bolded" modifications, and quick keyboard shortcuts to
commands.  It is very small, and works over telnet connections flawlessly!  
Currently works in the *AES shell, over telnet connections, but not on the 
native console session, display is fine, problem with keybindings.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
CXXFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
        prefix=${RPM_BUILD_ROOT}%{_prefix} \
        mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files 
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README
%{_prefix}/bin/*
%{_prefix}/share/man/man*/*


%changelog
* Thu Feb 5 2004 Keith Scroggins <kws@radix.net>
- Initial build of hexcurse for MiNT
