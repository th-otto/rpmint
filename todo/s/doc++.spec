Summary       : DOC++ - A Documentation System for C, C++, IDL and Java
Summary(es)   : DOC++ - Un sistema de documentacion para C, C++, IDL y Java
Summary(fr)   : DOC++ - Un gИnИrateur de documentation pour C, C++, IDL et Java
Summary(ro)   : DOC++ - Generator de documentatii pentru C, C++, IDL si Java
Summary(ru)   : DOC++ - Система документирования исходных текстов для C, C++, IDL и Java
Summary(sv)   : DOC++ - Ett dokumentationsgenereringssystem fЖr C, C++, IDL och Java
Name          : doc++
Version       : 3.4.8
Release       : 2
Copyright     : GPL
Group         : Development/Tools

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://docpp.sourceforge.net

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://sunsite.unc.edu/pub/Linux/apps/doctools/doc++-%{version}.tar.gz


%description
DOC++ is a documentation system for C, C++, IDL and Java, generating both TeX
output for high quality hardcopies and HTML output for sophisticated online
browsing of your documentation. The documentation is extracted directly
from the C/C++/IDL header/source files or Java class files.

%description -l es
DOC++ es un sistema de documentacion para C, C++, IDL y Java, que genera
textos en TeX para crear copias de alta calidad de la
documentaciСn y en HTML para poder navegar por ella. La
documentaciСn se extrae directamente de lso ficheros de cabecera
C/C++/IDL o de los ficheros de clase en Java.

%description -l fr 
DOC++ est un systХme de documentation pour C, C++, IDL et Java. Il peut
gИnИrer au choix un document TeX pour produire une documentation
imprimИe de qualitИ, ou un fichier HTML pour un parcours en-ligne aisИ
de la documentation. La documentation est extraite directement du
fichier d'en-tЙte C/C++/IDL ou du fichier des classes Java.

%description -l ro
DOC++ este un generator de documentatii pentru C, C++, IDL si Java, producand
iesire atat in format TeX pentru copii de calitate cat si HTML pentru navigare
on-line prin documentatie. Documentatia este extrasa direct din fisierele
header/sursa C/C++/IDL sau din fisierele de tip clasa Java.

%description -l ru
DOC++ -- система документирования исходных текстов для языков C, C++, IDL и
Java.  Поддерживается вывод в формате TeX для печати и HTML -- для
создания гипертекстовых справочников.  Документация располагается
непосредственно в исходном тексте, с использованием комментариев
специального формата.

%description -l sv
DOC++ Дr ett dokumentationsgenereringssystem fЖr C, C++, IDL och Java som
genererar bЕde TeX-kod fЖr hЖgkvalitativa utskrifter och HTML fЖr
sofistikerad webbvisning av dokumentationen. Dokumentationen
extraheras direkt frЕn C/C++/IDL-headerfilen eller javaklassfilen.


%prep
%setup -q

cp /usr/lib/rpm/config.{guess,sub} .


%build
CXXFLAGS="-D_GNU_SOURCE" \
LIBS=-lintl \
./configure \
	--prefix=%{_prefix}

make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	gnulocaledir=${RPM_BUILD_ROOT}%{_prefix}/share/locale

stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS PLATFORMS README REPORTING-BUGS doc/manual doc/doc++.conf doc/docxx-br.sty doc/docxx-fr.sty doc/docxx-ja.sty doc/docxx-ro.sty doc/docxx.sty
%{_prefix}/bin/doc++
%{_prefix}/bin/docify
%{_prefix}/bin/promote
%{_prefix}/share/locale/*/*/*


%changelog
* Mon Sep 03 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
