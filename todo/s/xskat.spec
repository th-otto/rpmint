Summary       : Skat, a card game
Name          : xskat
Version       : 4.0
Release       : 1
Copyright     : Free
Group         : X11/Games

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.xskat.de/

BuildRequires : XFree86-devel
Requires      : XFree86

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.xskat.de/xskat-%{version}.tar.gz
Patch0: xskat-3.4-def-german-card.patch


%description
Skat is a popular game in Germany.  A card game for the X Window
System, with full featured network support.  Also via IRC. -
It follows the "Deutsche Skat-Ordnung" or with popular addition
strategies. 
Now with "Ramsch", "Schieberamsch", "Revolution" and more...

Authors:
--------
    Gunter Gerhardt <gerhardt@draeger.com>


%prep
%setup -q
%patch0 -p1 -b .def-german-card
xmkmf -a


%build
make DEFINES='-DDEFAULT_LANGUAGE=\"german\" -DDEFAULT_IRC_SERVER=\"irc.freenet.de\"'


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

install -m755 -d ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin
install -m755 -d ${RPM_BUILD_ROOT}%{_prefix}/X11R6/include/X11/bitmaps
install -m755 -d ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/man6
install -m755 xskat ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/xskat
install -m644 icon.xbm ${RPM_BUILD_ROOT}%{_prefix}/X11R6/include/X11/bitmaps/xskat.xbm
install -m644 xskat.man ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/man6/xskat.6

strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}/usr/X11R6/man/man6/xskat.6


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc CHANGES README
%{_prefix}/X11R6/bin/xskat
%{_prefix}/X11R6/include/X11/bitmaps/xskat.xbm
%{_prefix}/X11R6/man/man6/xskat.6.gz


%changelog -n xskat
* Fri May 28 2004 Frank Naumann <fnaumann@freemint.de>
- updated to version 4.0

* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
