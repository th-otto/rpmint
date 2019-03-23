Summary: Generates function prototypes and variable declarations from C code.
Name: cproto
Version: 4.6
Release: 2
Copyright: Public Domain
Group: Development/Tools
Source: ftp://ftp.oce.com/pub/cproto/cproto-%{version}.tar.gz
Patch0: cproto-4.6-4.6.1-patch
Prefix: %{_prefix}
BuildRoot: /var/tmp/%{name}-root
Distribution: Sparemint
Vendor: Sparemint
Packager: Edgar Aichinger <eaiching@t0.or.at>
Summary(de): Erzeugt Funktionsprototypen und Variablendeklarationen aus C-Quellcode.

%description
Cproto generates function prototypes and variable declarations from
C source code.  Cproto can also convert function definitions between the
old style and the ANSI C style.  This conversion will overwrite the
original files, however, so be sure to make a backup copy of your original
files in case something goes wrong.  Since cproto uses a Yacc generated
parser, it shouldn't be confused by complex function definitions as much
as other prototype generators) because it uses a Yacc generated parser.  

Cproto will be useful for C programmers, so install cproto if you are going
to do any C programming.

%description -l de
Cproto erzeugt Funktionsprototypen und Variablendeklarationen aus C-
Quellcode.  Cproto kann auch Funktionsdefinitionen zwischen altem K&R-
und dem ANSI C Stil konvertieren.  Diese Umwandlung wird aber die
Originaldateien überschreiben, also machen Sie Backup-Kopien Ihrer
Originaldateien für den Fall, daß etwas schiefgeht.  Da cproto einen von
Yacc generierten Parser verwendet, sollte es, anders als andere Prototyp-
Generatoren, auch durch komplexe Funktionsdefinitionen nicht so leicht
zu verwirren sein.  

Cproto ist für C-Programmierer vonnutzen, also installieren Sie es,
falls Sie in C programmieren wollen.

%prep
%setup -q
%patch0 -p1 -b .4_6

%build
#CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --exec-prefix=/usr

%configure --exec-prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=${RPM_BUILD_ROOT}%{_prefix} bindir=${RPM_BUILD_ROOT}%{_prefix}/bin install

( cd $RPM_BUILD_ROOT
  strip .%{_prefix}/bin/cproto
  stack -S 64k .%{_prefix}/bin/cproto
  gzip -9nf .%{_prefix}/man/man1/%{name}.1
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES README
%{_prefix}/bin/cproto
%{_prefix}/man/man1/cproto.1.gz

%changelog
* Wed Nov 03 1999 Edgar Aichinger <eaiching@t0.or.at>
- corrected specfile (german summary)

* Sat Oct 23 1999 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT 
- compressed manpage
