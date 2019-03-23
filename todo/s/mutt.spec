Summary       : The Mutt Mail User Agent
Summary(de)   : Der Mutt Mail-User-Agent 
Summary(fr)   : Agent courrier Mutt
Name          : mutt
Version       : 1.3.23
Release       : 1
Copyright     : GPL
Group         : Applications/Mail

Packager      : Guido Flohr <guido@freemint.de>
Vendor        : Sparemint
URL           : http://www.mutt.org/

Requires      : smtpdaemon
Conflicts     : mutt-ssl

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.guug.de/pub/mutt/%{name}-%{version}i.tar.gz
Source1: mutt.wmconfig
Source2: muttrc.sparemint
Patch0:  mutt-1.3.23-MINMAX.patch


%description
Mutt is a small but very poweful full-screen Unix mail client.
Features include MIME support, color, POP3 support, message threading,
bindable keys, and threaded sorting mode.

Note that this is the international version of Mutt.  Export restrictions
may apply, be warned.

%description -l de
Mutt ist ein kleiner aber leistungsfähiger Vollbild-Mail-Client für Unix mit
MIME-Unterstützung, Farbe, POP3-Unterstützung, Nachrichten-Threading,
zuweisbaren Tasten und Sortieren nach Threads.

Dies ist die internationale Version von Mutt. Eventuell kommen Export-
Beschränkungen zum Tragen!

%description -l fr
mutt est un client courrier Unix plein écran, petit mais très puissant.
Il dispose de la gestion MIME, des couleurs, de la gestion POP, des fils
de discussion, des touches liées et d'un mode de tri sur les fils.

Cette distribution de Mutt est internationale!  Il est bien possible
qu'il y a des restrictions de l'exportation!


%prep
%setup -q
%patch0 -p1 -b .MINMAX


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_prefix}/share/man \
	--sysconfdir=/etc \
	--enable-pop \
	--enable-imap \
	--disable-warnings
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man \
	sysconfdir=${RPM_BUILD_ROOT}/etc \
	docdir=${RPM_BUILD_ROOT}%{_prefix}/doc/mutt

install -m644 $RPM_SOURCE_DIR/muttrc.sparemint $RPM_BUILD_DIR
install -m644 $RPM_BUILD_DIR/mutt-%{version}/Muttrc ${RPM_BUILD_ROOT}/etc/Muttrc

mkdir -p ${RPM_BUILD_ROOT}/etc/X11/wmconfig
install -m 644 $RPM_SOURCE_DIR/mutt.wmconfig ${RPM_BUILD_ROOT}/etc/X11/wmconfig/mutt

# sample sparemint config
mkdir -p ${RPM_BUILD_ROOT}/etc/skel
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}/etc/skel/.muttrc

# also add it to the docs
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/doc/mutt

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=96k ${RPM_BUILD_ROOT}%{_prefix}/bin/mutt ||:
chmod g-s ${RPM_BUILD_ROOT}%{_prefix}/bin/mutt

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc %{_prefix}/doc/mutt
%config(missingok) /etc/X11/wmconfig/mutt
%config /etc/Muttrc
%config /etc/skel/.muttrc
/etc/mime.types
%{_prefix}/bin/*
%{_prefix}/share/man/man*/*
%{_prefix}/share/locale/*/LC_MESSAGES/*


%changelog
* Fri Nov 16 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.3.23

* Mon Aug 16 1999 Guido Flohr <guido@freemint.de>
- First version for Sparemint
