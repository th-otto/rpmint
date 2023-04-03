%define pkgname xskat

%rpmint_header

Summary       : Skat, a card game
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 4.0
Release       : 2
License       : Public Domain
Group         : X11/Games

Packager:       Thorsten Otto <admin@tho-otto.de>
URL           : http://www.xskat.de/

%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
Requires      : cross-mint-XFree86
%else
BuildRequires : XFree86-devel
Requires      : XFree86
%endif

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.xskat.de/xskat-%{version}.tar.gz
Patch0: xskat-3.4-def-german-card.patch

%rpmint_build_arch

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
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 020
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	%{_rpmint_target}-xmkmf -DCpuOption="${CPU_CFLAGS}" -a
	make DEFINES='-DDEFAULT_LANGUAGE=\"german\" -DDEFAULT_IRC_SERVER=\"irc.freenet.de\"'
done


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -m755 -d %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin
install -m755 -d %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/bitmaps
install -m755 -d %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man6
install -m755 xskat %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xskat
install -m644 icon.xbm %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/bitmaps/xskat.xbm
install -m644 xskat.man %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man6/xskat.6

%{_rpmint_target}-strip %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:
%{_rpmint_target}-stack --fix=256k %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man6/xskat.6


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%doc CHANGES README
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xskat
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/bitmaps/xskat.xbm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man6/xskat.6.gz


%changelog -n xskat
* Wed Mar 22 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri May 28 2004 Frank Naumann <fnaumann@freemint.de>
- updated to version 4.0

* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
