Summary: A utility which provides statistics based on the output of diff.
Name: diffstat
Version: 1.27
Release: 1
Group: Development/Tools
Copyright: distributable
Prefix: /usr
Source: ftp.clark.net:/pub/dickey/diffstat/%{name}-%{version}.tgz
BuildRoot: /var/tmp/%{name}-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Requires: diffutils
Summary(de): Ein Utility, das Statistiken über die Ausgaben von diff liefert.

%description
The diff command compares files line by line.  Diffstat reads the output
of the diff command and displays a histogram of the insertions, deletions
and modifications in each file.  Diffstat is commonly used to provide
a summary of the changes in large, complex patch files.

Install diffstat if you need a program which provides a summary of the
diff command's output.  You'll need to also install diffutils.

%description -l de
Das Kommando diff vergleicht Dateien Zeile für Zeile. Diffstat liest die
Ausgaben von diff und stellt ein Histogramm über Einfügungen, Löschungen
und Veränderungen in jeder Datei dar. Diffstat wird häufig benützt, um eine
Zusammenfassung der Änderungen in großen, komplexen patch-Dateien zu erzeugen.

Installieren Sie diffstat, falls Sie ein Programm brauchen, das eine Zusammenfassung
der Ausgaben von diff liefert. Sie werden auch diffutils installieren müssen.

%prep
%setup -q

%build
./configure --prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT/usr exec_prefix=$RPM_BUILD_ROOT/usr install
strip $RPM_BUILD_ROOT/usr/bin/diffstat
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/%{name}.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/diffstat
/usr/man/man1/diffstat.1.gz

%changelog
* Sat Sep 25 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT (new version)
