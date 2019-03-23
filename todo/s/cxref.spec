%define  ver	 1.5c
%define  rel	 1
%define  prefix  /usr

Summary:	A C program cross-referencing & documentation tool
Name:		cxref
Version: 	%ver
Release: 	%rel
Copyright: 	GPL
Group: 		Development/Tools
Source: 	ftp.demon.co.uk/pub/unix/tools/%{name}-%{version}.tgz
Prefix: 	%prefix
BuildRoot: 	/var/tmp/%{name}-root
Distribution: 	Sparemint
Vendor: 	Sparemint
Packager: 	Edgar Aichinger <eaiching@t0.or.at>
Summary(de):	Ein Querverweis- und Dokumentationstool für C-Programme

%description
Cxref is a program that takes as input a series of C source files and
produces documentation (in LaTeX, HTML, RTF or SGML) containing cross-
references of the files/functions/variables in the program, including
documentation taken from suitably formatted source code comments.

The documentation is stored in the C source file in specially
formatted comments, making it simple to maintain. The cross
referencing includes lists of functions called, callers of each
function, usage of global variables, header file inclusion, macro
definitions and type definitions.

Works for ANSI C, including most gcc extensions.

%description -l de
Cxref ist ein Programm, das eine Gruppe von C-Quelltextdateien liest
und LaTeX oder HTML-Dokumente erzeugt, die die Querverweise der
Dateien/Funktionen/Variablen in dem Programm enthalten, wie auch
Dokumentation, die aus entsprechend formatierten Quelltextkommentaren
gewonnen wird.

Die Dokumentation wird in der C-Quelldatei in auf bestimmte Weise
formatierten Kommentaren gespeichert, wodurch sie leicht gewartet
werden kann. Die Analyse umfasst Listen der aufgerufenen Funktionen,
Aufrufern jeder Funktion, Zugriff auf globale Variablen,
eingebundener Headerdateien, Makrodefinitionen und Typdefinitionen.

Für ANSI C, einschliesslich der meisten gcc-Erweiterungen.

%prep
%setup -q

%build
configure --prefix=%prefix
make

%install
make prefix=$RPM_BUILD_ROOT%prefix exec_prefix=$RPM_BUILD_ROOT%prefix \
	mandir=$RPM_BUILD_ROOT%prefix/share/man install
strip $RPM_BUILD_ROOT%prefix/bin/%{name}
stack -S128k $RPM_BUILD_ROOT%prefix/bin/%{name}
strip $RPM_BUILD_ROOT%prefix/bin/%{name}-query
gzip -9nf $RPM_BUILD_ROOT%prefix/share/man/man1/%{name}.1
gzip -9nf $RPM_BUILD_ROOT%prefix/share/man/man1/%{name}-query.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/*
/usr/share/man/*/*
%doc README ANNOUNCE NEWS FAQ ChangeLog TODO COPYING

%changelog
* Sun Jun 24 2001 Edgar Aichinger <eaiching@t0.or.at>
- updated to version 1.5c

* Mon Feb 07 2000 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT
