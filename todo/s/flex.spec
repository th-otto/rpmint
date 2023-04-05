Summary: A tool for creating scanners (text pattern recognizers).
Summary(de): Ein Tool zum Generieren von Scannern (text pattern recognizers).
Name: flex
Version: 2.5.4a
Release: 5
Copyright: GPL
Group: Development/Tools
Packager: Frank Naumann <fnaumann@freemint.de>
Vendor: Sparemint
Source: ftp://prep.ai.mit.edu:/pub/gnu/flex-2.5.4a.tar.gz
BuildRoot: /var/tmp/flex-root

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as output.
The output file is compiled and linked with a library to produce an
executable.  The executable searches through its input for occurrences of
the regular expressions.  When a match is found, it executes the
corresponding C code.  Flex was designed to work with both Yacc and Bison,
and is used by many programs as part of their build process.

You should install flex if you are going to use your system for
application development.

%description -l de
Das flex Programm generiert Scanner. Scanner sind Programme welche
lexikalische Muster in Texten erkennen. Flex benutzt Regular Expressions
und C Fragmente als Eingabe und generiert daraus ein C Source File indem
die Regular Expression durch entsprechenden C Code ersetzt werden.
Flex ist auf die Zusammenarbeit mit Yacc oder Bison abgestimmt. Flex wird
von vielen Programmen während des Build Prozesses benötigt.

Man sollte flex installieren wenn man sein System für Applikations-
Entwicklung nutzen will.

%prep
%setup -q -n flex-2.5.4

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s ./configure --prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT/usr install

( cd $RPM_BUILD_ROOT
  strip ./usr/bin/flex
  stack --fix=256k ./usr/bin/flex || :
  gzip -9nf ./usr/man/man1/*
  ln -sf flex ./usr/bin/lex
  ln -s flex.1.gz ./usr/man/man1/lex.1.gz
  ln -s flex.1.gz ./usr/man/man1/flex++.1.gz
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING NEWS README
/usr/bin/lex
/usr/bin/flex
/usr/bin/flex++
/usr/man/man1/lex.1.gz
/usr/man/man1/flex.1.gz
/usr/man/man1/flex++.1.gz
/usr/lib/libfl.a
/usr/include/FlexLexer.h

%changelog
* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
- added %description de and Summary(de)
