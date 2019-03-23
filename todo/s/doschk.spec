Summary: doschk checks filenames for DOS, TOS and SYSV compatibility
Name: doschk
Version: 1.1
Release: 1
Source: ftp://ftp.gnu.org/gnu/doschk/%{name}-%{version}.tar.gz
Copyright: GPL
Group: Applications/File
BuildRoot: /var/tmp/doschk-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Distribution: Sparemint
Vendor: Sparemint
Summary(de): doschk überprüft Dateinamen auf DOS-, TOS- und SYSV-Kompatibilität.

%description
Doschk is a utility to help software developers and users ensure that their source
file names are distinguishable on  platforms with short filenames, e.g. MS-DOS,
Atari TOS and SYSV. To perform this task, doschk reads a list of filenames
and produces a report of all the conflicts that would arise if the files were
transferred to such a filesystem.

Install doschk if you want to find out which conflicts would appear when
copying files to DOS, TOS or SYSV filesystems.

%description -l de
Doschk ist ein Utility, das Entwicklern und Anwendern hilft, sicherzustellen, daß
die Dateinamen ihre Quelltexte auf Plattformen mit kurzen Dateinamen (z.B. MS-DOS,
Atari TOS und SYSV) unterscheidbar sind. Um diese Aufgabe zu erfüllen, liest 
doschk eine Liste von Dateinamen und erzeugt einen Report aller Konflikte, die
auftauchen würden, wenn man diese Dateien auf so ein Dateisystem kopieren würde.

Installieren Sie doschk, falls Sie herausfinden möchten, welche Konflikte sich ergäben, 
wenn Sie Dateien auf ein DOS-, TOS- or SYSV-Dateisystem kopieren würden.

%prep
%setup -q
./configure --prefix=/usr

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
make prefix=$RPM_BUILD_ROOT/usr exec_prefix=$RPM_BUILD_ROOT/usr install
strip $RPM_BUILD_ROOT/usr/bin/doschk

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/doschk
%doc ChangeLog README COPYING

%changelog
* Fri Oct 22 1999 Edgar Aichinger <eaiching@t0.or.at>
- first relase for Sparemint
