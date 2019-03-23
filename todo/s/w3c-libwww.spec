Summary       : HTTP library of common code
Summary(de)   : Eine allgemein gehaltene HTTP-Bibliothek
Name          : w3c-libwww
Version       : 5.3.2
Release       : 1
Copyright     : W3C (see: http://www.w3.org/Consortium/Legal/copyright-software.html)
Group         : System Environment/Libraries

Packager      : Edgar Aichinger <eaiching@t0.or.at>
Vendor        : Sparemint
URL           : http://www.w3.org/Library/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.w3.org/Library/Distribution/%{name}-%{version}.tar.gz


%description
Libwww is a general-purpose Web API written in C for Unix, MiNT and and 
Windows (Win32). With a highly extensible and layered API, it can accommodate 
many different types of applications including clients, robots, etc.
The purpose of libwww is to provide a highly optimized HTTP sample 
implementation as well as other Internet protocols and to serve as a testbed 
for protocol experiments.

%description -l de
Libwww ist ein allgemein gehaltenes Web-API in C für Unix, MiNT und Windows
(Win32). Mit einem erweiterbaren und geschichteten API, kann es für viele 
verschiedene Arten von Anwendungen, z. B. Clients, Roboter, usw benützt werden.
Die Absicht von libwww ist, eine hochoptimierte Beispiel-Implementierung
von HTTP und anderen Internet-Protokollen bereitzustellen, sowie als
Testfeld für Protokoll-Experimente zu dienen.

%package devel
Summary       : Libraries and header files for programs that use libwww.
Summary(de)   : Bibliotheken und Headerdateien für libwww-Programme.
Group         : Development/Libraries
Requires      : w3c-libwww = %{version}

%description devel
Static libraries and header files for libwww, which are available as public
libraries.

%description devel -l de
öffentlich erhältliche statische Bibliotheken und Headerdateien für libwww.

%package apps
Summary       : Applications built using Libwww web library: e.g. Robot, command line tool, etc.
Summary(de)   : Mit libwww erstellte Anwendungen: z.B. robot und Kommandozeilen-Tool usw.
Group         : Applications/Internet
Requires      : w3c-libwww = %{version}

%description apps
Web applications built using Libwww: Robot, Command line tool, 
line mode browser.  The Robot can crawl web sites faster, and
with lower load, than any other web walker that we know of, 
due to its extensive pipelining and use of HTTP/1.1.

The command line tool (w3c) is very useful for manipulation of 
Web sites that implement more than just HTTP GET (e.g. PUT, 
POST, etc.).

The line mode browser is a minimal line mode web browser; 
often useful to convert to ascii text.  Currently unavailable
until someone updates it to some new interfaces. (hint, hint...)

%description apps -l de
Web-Anwendungen, die mit Libwww erstellt wurden: Robot, das 
Kommandozeilen-Tool, und ein Zeilenmodus-Browser. Robot kann Websites
schneller und mit geringerer Auslastung als jeder andere "web walker",
den wir kennen, absuchen, wegen seinem extensiven Pipelining und 
der Verwendung von HTTP/1.1.

Das Kommandozeilen-Tool (w3c) ist sehr nützlich, um Websites zu
manipulieren, die mehr als nur HTTP GET implementieren (z.B. PUT, 
POST, usw.).

Der Zeilenmodus-Browser ist ein minimaler Web-Browser im Zeilenmodus; 
oft nützlich, um nach ASCII zu konvertieren. Momentan nicht erhältlich
bis ihm jemand einige neue Interfaces verpaßt. (Tips, Tips...)


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
CXXFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--disable-shared \
	--with-gnu-ld \
	--with-regex \
	--with-zlib \
	--host=m68k-atari-mint
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}%{_prefix}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* || :

mv ${RPM_BUILD_ROOT}%{_prefix}/include/wwwconf.h \
	${RPM_BUILD_ROOT}%{_prefix}/include/w3c-libwww/


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc *.html */*.html */*/*.html Icons/*/*.gif
%{_prefix}/share/w3c-libwww

%files apps
%defattr(-,root,root)
%{_prefix}/bin/webbot
%{_prefix}/bin/w3c
%{_prefix}/bin/www

%files devel
%defattr(-,root,root)
%{_prefix}/bin/libwww-config
%{_prefix}/include/w3c-libwww
%{_prefix}/lib/lib*.a
%{_prefix}/lib/lib*.la


%changelog
* Thu Mar 15 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 5.3.2

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Tue Nov 09 1999 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT 
