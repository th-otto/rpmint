Summary: A C library for parsing command line parameters.
Name: popt
Version: 1.3
Release: 4
Copyright: LGPL
Group: System Environment/Libraries
Source: ftp://ftp.redhat.com/pub/redhat/code/popt/popt-%{version}.tar.gz
Patch0: popt-1.3-mintcnf.patch
BuildRoot: /var/tmp/%{name}-root
Packager: Guido Flohr <guido@freemint.de>
Vendor: Sparemint
Summary(de): Eine C-Bibliothek zur Analyse von Kommondozeilen-Optionen.
Prefix: %{_prefix}

%description
Popt is a C library for parsing command line parameters.  Popt
was heavily influenced by the getopt() and getopt_long() functions,
but it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments.  Popt allows command
line arguments to be aliased via configuration files and includes
utility functions for parsing arbitrary strings into argv[] arrays
using shell-like rules.

Install popt if you're a C programmer and you'd like to use its
capabilities.

%description -l de
Popt ist eine C-Bibliothek zur Analyse von Kommandozeilen-Optionen.
Popt wurde stark von den Funktionen getopt() und getopt_long()
beeinflusst, aber verbessert diese, indem mächtigere
Argument-Expansionen erlaubt werden. Popt kann beliebige Felder
im Stile von argv[] analysieren. Popt erlaubt auch das Aliasing
von Kommandozeilen-Optionen über Konfigurationsdateien und
beeinhaltet Hilfsfunktionen für die lexikalische Analyse von
argv[]-Feldern im Stile einer Shell.

Popt sollte von C-Programmierinnen installiert werden, die diese
Fähigkeiten nutzen möchten.

%prep
%setup -q
%patch0 -p1 -b .mint

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} --disable-shared
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
gzip -9nf $RPM_BUILD_ROOT/%{_prefix}/man/man3/popt.3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/lib/libpopt.a
%{_prefix}/include/popt.h
%{_prefix}/man/man3/popt.3.gz

%changelog
* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Tue Sep 14 1999 Guido Flohr <guido@freemint.de>
- Initial Sparemint version
