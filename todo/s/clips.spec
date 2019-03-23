Summary: The C Language Integrated Production System
Name: clips
Version: 6.10
Release: 1
Copyright: Distributables
Group: Development/Languages
URL: http://www.ghg.net/clips/
Source0: http://www.ghg.net/clips/download/source/clipssrc.tar.Z
Source1: http://www.ghg.net/clips/download/source/makefile.Z
Source2: http://www.ghg.net/clips/download/source/x-prjct.tar.Z
Source4: clips-6.10-doc.tar.gz
Patch0: clips-6.10-gfl.patch
Patch1: clips-6.10-xgfl.patch
Buildroot: /var/tmp/clips
Prefix: %{_prefix}
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): Das C-Language-Integrated-Production-System

%description
CLIPS is an expert system tool developed by the Software Technology
Branch (STB) NASA/Lyndon B. Johnson Space Center.  Since its first
release in 1986, CLIPS has undergone continual refinement and
improvement.  It is now used by thousands of people around the world.
The Internet news group comp.ai.shells often has discussions of CLIPS.

CLIPS is designed to facilitate the development of software to model
human knowledge or expertise.

There are three ways to represent knowledge in CLIPS:

o Rules, which are primarily intended for heuristic knowledge based on
  experience.

o Deffunctions and generic functions, which are primarily intended for
  procedural knowledge.
  
o Object-oriented programming, also primarily intended for procedural
  knowledge.  The five generally accepted features of object-oriented
  programming are supported: classes, message-handlers, abstraction,
  encapsulation, inheritance, polymorphism.  Rules may pattern match
  on objects and facts.

You can develop software using only rules, only objects, or a mixture
of objects and rules.

CLIPS has also been designed for full integration with other languages
such as C and Ada.  In fact, CLIPS is an acronym for C Language 
Integrated Production System.  Rules and objects form an integrated
system too since rules can pattern-match on facts and objects.  In
addition to being used as a stand-alone tol, CLIPS can be called from
a procedural language, perform its function, and then return control
back to the calling program.  Likewse, procedural code can be defined
as external functions and called from CLIPS.  When the external code 
completes execution, control returns to CLIPS.

If you are already familiar with object-oriented programming in other
languages such as C++, Smalltalk, Object C or Turbo Pascal, you know
the advantages of objects in developing software.  If you are not
familiar with object-oriented programming, you will find that CLIPS
is an excellent tool for learning this new concept in software
development.

%description -l de
CLIPS ist ein Expertensystem-Werkzeug, das vom Software Technology
Branch (STB), NASA/Lyndon B. Johnson Space Center entwickelt wurde.
Seit der ersten Veröffentlichung 1986, wurde CLIPS einer kontinuierlichen
Verfeinerung und Verbesserungen unterzogen. Heute wird es von Tausenden
von Menschen auf der ganzen Welt verwendet. Die Internet-News-Gruppe
comp.ai.shells führt oft Diskussionen über CLIPS.

Entwurfsziel von CLIPS ist es, die Entwicklung von Software zur
Nachbildung menschlischen Wissens bzw. Expertenwissens zu vereinfachen.

Wissen kann in CLIPS auf drei Arten repräsentiert werden:

o Mit Regeln, für vornehmlich heuristisches, erfahrungsbasiertes
  Wissen,

o mit generischen und benutzerdefinierten Funktionen (sogenannten 
  »deffunctions«), die vornehmlich für prozedurales Wissen vorgesehen 
  sind,

o mit objekt-orientierter Programmierung, ebenfalls in erster Linie
  für prozedurales Wissen vorgesehen. Die fünf allgemein anerkannten
  Merkmale objekt-orientierter Programmierung sind voll ausgebildet:
  Klassen, Nachrichten-Behandlung, Abstrahierung, Einkapselung,
  Vererbung und Polymorphismus. Regeln können auf Objekte und Tatsachen
  passend angewendet werden.

Software kann entweder nur mit Regeln, nur mit Objekten oder mit einer
Mischung aus beiden entwickelt werden.

Ein weiteres Entwursziel von CLIPS ist die volle Integrierbarkeit mit
anderen Sprachen, wie C und Ada. Tatsächlich ist CLIPS die Abkürzung für
»C Language Integrated Production System« (Integriertes Produktionssystem
der Sprache C). Regeln und Objekte bilden ebenfalls ein integriertes
System, weil Regeln auf Objekte und Fakten passend angewendet werden können.
Zusätzlich zur Verwendung als eigenständiges Werkzeug kann CLIPS auch
aus einer prozeduralen Sprache aufgerufen werden, eine bestimmte Funktion
ausführen und dann die Kontrolle an das aufrufende Programm zurückgeben.
Ebenso kann prozeduraler Code als externe Funktionen definiert und aus
CLIPS heraus aufgerufen werden. Wenn die Ausführung des externen Codes
abgeschlossen ist, wird die Kontrolle an CLIPS zurückgegeben.

Wer bereits mit objekt-orientierter Programmierung in anderen Sprachen
wie C++, Smalltalk, Object C oder Turbo Pascal vertraut ist, wird die
Vorteile des objekt-orientierten Ansatzes bei der Software-Entwicklung
kennen. Diejenigen, die mit objekt-orientierter Programmierung noch
nicht vertraut sind, lernen mit CLIPS ein vorzügliches Werkzeug kennen,
um dieses neue Konzept der Software-Entwicklung zu erlernen.

%package doc
Group: Documentation
# Bug or feature in rpm 3.0.2: The main package would inherit the
# build architecture from the subpackage which is not what we want.
# Leave it as it is for the moment.
#BuildArchitectures: noarch
Summary: Documentation for CLIPS as Adobe PDF
Summary(de): Dokumentation für CLIPS als Adobe PDF

%description doc
This package contains the documentation for CLIPS in the Portable 
Document Format PDF.

%description -l de doc
Dieses Paket enthält die Dokumentation zu CLIPS im Portablen 
Dokument-Format PDF.

%prep
%setup -q -c
gunzip -c $RPM_SOURCE_DIR/makefile.Z >source/makefile

%ifnarch m68kmint
# No GUI for MiNT yet.
tar xzf $RPM_SOURCE_DIR/x-prjct.tar.Z
cp x-prjct/xinterface/* source
cp x-prjct/makefile/makefile.x source
%endif

tar xzf $RPM_SOURCE_DIR/clips-%{version}-doc.tar.gz
mv Documentation/* .

%patch0 -p1 -b .gfl

%ifnarch m68kmint
%patch1 -p1 -b .xgfl
%endif

%build
cd source
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" -f makefile
%ifnarch m68kmint
rm *.o
# xclips cannot be optimized (dumps core).
make RPM_OPT_FLAGS="" -f makefile.x
cd ../x-prjct/color
gcc -o color -I. -I/usr/X11R6/include -L/usr/X11R6/lib \
  color.c -lXaw -lXmu -lXt -lXext -lX11 -lm 
%endif

%install
cd source
rm -rf $RPM_BUILD_ROOT
mkdir -p "$RPM_BUILD_ROOT"%{_prefix}/bin
install -s -m 755 clips "$RPM_BUILD_ROOT"%{_prefix}/bin
%ifnarch m68kmint
install -s -m 755 xclips "$RPM_BUILD_ROOT"%{_prefix}/bin
cd ../x-prjct/color
install -s -m 755 color "$RPM_BUILD_ROOT"%{_prefix}/bin
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.clips examples
%{_prefix}/bin/clips
%ifnarch m68kmint
%{_prefix}/bin/xclips
%{_prefix}/bin/color
%endif

%files doc
%defattr(-,root,root)
%doc *.pdf

%changelog
* Sun Oct 24 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Also build the color tool for X Windows.
- Put pdf documentation into separate package.

* Fri Oct 22 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Allow build for Linux (resp. other systems with X Windows)
- Added documentation in Portable Document Format

* Thu Oct 21 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- First build for Sparemint.

