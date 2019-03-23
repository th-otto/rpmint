Summary       : Extremely simple, and feature-rich, HTML/text editor for GTK/GNOME.
Name          : gnotepad+
Version       : 1.3.3
Release       : 1
Copyright     : GPL
Group         : Applications/System

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://gnotepad.sourceforge.net/

BuildRequires : gtk+ >= 1.2.0 glib >= 1.2.0
Requires      : gtk+ >= 1.2.0 glib >= 1.2.0

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz


%description
gnotepad+ is an easy-to-use, yet fairly feature-rich, simple HTML/text
editor for systems running X11 and using GTK+/GNOME. It is designed
for as little bloat as possible, while still providing many of the
common features found in a modern GUI-based text editor.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=${RPM_BUILD_ROOT}%{_prefix}

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc AUTHORS HACKING NEWS README TODO ChangeLog
%attr(755,root,root)
%{_prefix}/bin/gnp
%{_prefix}/share/locale/*/*/*
%{_prefix}/share/man/man1/gnp.1.gz
%{_prefix}/share/gnome/apps/Applications/*
%{_prefix}/share/gnome/help/gnotepad+
%{_prefix}/share/gnotepad+


%changelog
* Fri Jan 05 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
