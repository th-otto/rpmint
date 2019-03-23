Summary       : NANO - Nano's ANOther editor, a pico like editor
Name          : nano
Version       : 1.0.0
Release       : 1
Copyright     : GPL
Group         : Console/Editors

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.asty.org/nano/

Requires      : ncurses

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.asty.org/nano/dist/nano-1.0.0.tar.gz


%description
nano (Nano's ANOther editor) is the editor formerly known as TIP (TIP Isn't 
Pico). It aims to emulate Pico as closely as possible while also offering a
few enhancements.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
LIBS=-lintl \
./configure \
	--prefix=%{_prefix} \
	--enable-extra
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/locale/es/LC_MESSAGES
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/locale/de/LC_MESSAGES
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/locale/fr/LC_MESSAGES
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/locale/it/LC_MESSAGES
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/locale/id/LC_MESSAGES
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/locale/fi/LC_MESSAGES

install nano ${RPM_BUILD_ROOT}%{_prefix}/bin
install nano.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
install po/es.gmo ${RPM_BUILD_ROOT}%{_prefix}/share/locale/es/LC_MESSAGES/nano.mo
install po/de.gmo ${RPM_BUILD_ROOT}%{_prefix}/share/locale/de/LC_MESSAGES/nano.mo
install po/fr.gmo ${RPM_BUILD_ROOT}%{_prefix}/share/locale/fr/LC_MESSAGES/nano.mo
install po/it.gmo ${RPM_BUILD_ROOT}%{_prefix}/share/locale/it/LC_MESSAGES/nano.mo
install po/id.gmo ${RPM_BUILD_ROOT}%{_prefix}/share/locale/id/LC_MESSAGES/nano.mo
install po/fi.gmo ${RPM_BUILD_ROOT}%{_prefix}/share/locale/fi/LC_MESSAGES/nano.mo

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/nano
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/nano

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README COPYING ChangeLog AUTHORS BUGS INSTALL NEWS TODO nano.1.html faq.html
%{_prefix}/bin/nano
%{_prefix}/share/man/man1/nano.1.gz
%{_prefix}/share/locale/es/LC_MESSAGES/nano.mo
%{_prefix}/share/locale/de/LC_MESSAGES/nano.mo
%{_prefix}/share/locale/fr/LC_MESSAGES/nano.mo
%{_prefix}/share/locale/it/LC_MESSAGES/nano.mo
%{_prefix}/share/locale/id/LC_MESSAGES/nano.mo
%{_prefix}/share/locale/fi/LC_MESSAGES/nano.mo


%changelog
* Tue Mar 27 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
