Summary       : A text-based Web browser.
Summary(de)   : Ein text-basierter Web-Browser
Name          : lynx-ssl
Version       : 2.8.4
Release       : 1
Copyright     : GPL
Group         : Applications/Internet

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://lynx.isc.org/

# conflicts with the normal version
Conflicts     : lynx
Requires      : indexhtml ncurses termcap
Provides      : webclient

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
Buildroot     : %{_tmppath}/%{name}-root

Source: http://sol.slcc.edu/lynx/current/lynx%{version}.tar.gz
Patch0: lynx-2.8.4-sparemint-ssl.patch
Patch1: lynx2-8-2-telnet.patch
Patch2: lynx-2.8.3-snews.patch


%description
Lynx is a text-based Web browser. Lynx does not display any images,
but it does support frames, tables and most other HTML tags. Lynx's
advantage over graphical browsers is its speed: Lynx starts and exits
quickly and swiftly displays Web pages.

Install lynx if you would like to try this fast, non-graphical browser
(you may come to appreciate its strengths).

==========================================================================
This packages was compiled with -m68020-060. This means you need at least
a machine with an 68020 CPU and an FPU to use the programs herein.
==========================================================================

%description -l de
Lynx ist ein text-basierter Web-Browser.  Lynx zeigt keine Bilder an,
aber unterstützt Frames, Tabellen und die meisten anderen HTML-Tags.
Der Vorteil von Lynx gegenüber anderen Browser ist die Geschwindigkeit:
Lynx startet und beendet sich sehr schnell und zeigt Web-Seiten flott an.

Die Installation von Lynx als nicht-graphischem Web-Browser ist einen
Versuch wert, man gewöhnt sich sehr schnell an seine Stärken.

==========================================================================
This packages was compiled with -m68020-060. This means you need at least
a machine with an 68020 CPU and an FPU to use the programs herein.
==========================================================================


%prep
%setup -q -n lynx2-8-4
%patch0 -p1 -b .sparemint
%patch1 -p1 -b .telnet
%patch2 -p1 -b .snews


%build
CFLAGS="${RPM_OPT_FLAGS} -m68020-60" \
./configure \
	--prefix=%{_prefix} \
	--libdir=/etc \
	--enable-warnings \
	--enable-default-colors \
	--enable-read-eta \
	--enable-nested-tables \
	--enable-source-cache \
	--enable-externs \
	--enable-cgi-links \
	--enable-exec-links \
	--enable-exec-scripts \
	--enable-internal-links \
	--enable-nsl-fork \
	--enable-persistent-cookies \
	--with-ssl \
	--with-zlib \
	--with-screen=ncurses \
	--disable-gopher \
#	\
#	--enable-prettysrc \
#	--disable-finger \
#	--disable-news
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man/man1 \
	libdir=${RPM_BUILD_ROOT}/etc

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/lynx
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/lynx ||:

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc docs README INSTALLATION samples
%doc test lynx.hlp lynx_help
%{_prefix}/bin/lynx
%{_prefix}/share/man/man1/lynx.1.gz
%config /etc/lynx.cfg


%changelog
* Tue Oct 30 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.8.4, compiled with SSL support

* Tue May 19 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.8.3, compiled with SSL support

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- correct Packager and Vendor
