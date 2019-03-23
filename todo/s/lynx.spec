Summary: A text-based Web browser.
Name: lynx
Version: 2.8.1
Release: 2
Copyright: GPL
Group: Applications/Internet
Source0: ftp://www.slcc.edu/pub/lynx/current/lynx2.8.1rel.2.tar.gz
Source1: lynx.wmconfig
Patch0: lynx2-8-1-redhat.patch
Patch1: lynx2-8-1-overflow.patch
Patch2: lynx-cookiefoo.patch
Patch3: lynx2-8-1-mint.patch
Patch100: lynx2.8.1rel.2-981106.patch
Patch101: lynx2.8.1rel.2-981118.patch
Patch102: lynx2.8.1rel.2-981204.patch
Vendor: Sparemint
Packager: Frank Naumann <fnaumarnn@prinz-atm.cs.uni-magdeburg.de>
Summary(de): Ein text-basierter Web-Browser
Requires: indexhtml
Provides: webclient
%define VER 2-8-1
Buildroot: /var/tmp/lynx-root

%description
Lynx is a text-based Web browser. Lynx does not display any images,
but it does support frames, tables and most other HTML tags. Lynx's
advantage over graphical browsers is its speed: Lynx starts and exits
quickly and swiftly displays Web pages.

Install lynx if you would like to try this fast, non-graphical browser
(you may come to appreciate its strengths).

%description -l de
Lynx ist ein text-basierter Web-Browser.  Lynx zeigt keine Bilder an,
aber unterstützt Frames, Tabellen und die meisten anderen HTML-Tags.
Der Vorteil von Lynx gegenüber anderen Browser ist die Geschwindigkeit:
Lynx startet und beendet sich sehr schnell und zeigt Web-Seiten flott an.

Die Installation von Lynx als nicht-graphischem Web-Browser ist einen
Versuch wert, man gewöhnt sich sehr schnell an seine Stärken.

%prep
%setup -n lynx%{VER}
%patch100 -p1 -b .lynxpatch1
%patch101 -p1 -b .lynxpatch2
%patch102 -p1 -b .lynxpatch3
%patch0 -p1 -b .redhat
%patch1 -p1 -b .overflow
%patch2 -p1 -b .cookiefoo
%patch3 -p1 -b .mint

%build
LIBS="-lport" CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --libdir=/etc \
	--enable-warnings \
	--enable-default-colors --enable-externs \
	--enable-internal-links \
	--enable-persistent-cookies --with-zlib \
	--with-screen=ncurses --enable-cgi-links \
	--enable-exec-links --enable-exec-scripts
make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/usr libdir=$RPM_BUILD_ROOT/etc
#mkdir -p $RPM_BUILD_ROOT/etc/X11/wmconfig
#install -m644 $RPM_SOURCE_DIR/lynx.wmconfig \
#	$RPM_BUILD_ROOT/etc/X11/wmconfig/lynx
strip $RPM_BUILD_ROOT/usr/bin/lynx
gzip -9nf $RPM_BUILD_ROOT/usr/man/*/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc docs README INSTALLATION samples
%doc test lynx.hlp lynx_help
/usr/bin/lynx
/usr/man/man1/lynx.1.gz
%config /etc/lynx.cfg

%changelog
* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- correct Packager and Vendor
