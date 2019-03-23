Summary:  two small programs and a script to show C call structures
Name: cflow        
Version: 2.0 
Release: 1
Group: Development/Tools
Prefix: /usr
Source: %{name}-%{version}.tar.gz
URL: http://sunsite.unc.edu/devel/C
Copyright: distributable
Buildroot: /var/tmp/%{name}-root
Distribution: Sparemint
Vendor: Sparemint
Packager: Edgar Aichinger <eaiching@t0.or.at>
Summary(de): zwei Programme und ein Shellskript, um C-Aufrufgraphen anzuzeigen

%description
The package cflow contains the programs prcc and prcg, and a shell script 
called cflow which is a frontend to these. Cflow can create call graphs of C 
source files. You can use command line options to control output in a flexible 
way. This is an enhanced version of cflow, which works well with GNU make, 
gcc and bash.

Install Cflow if you are a C programmer and want to examine the call structure 
of your C source files.

%description -l de
Das Paket Cflow beinhaltet die Programme prcc und prcg, und ein Shellskript 
namens cflow, um diese zu bedienen. Cflow kann Aufrufgraphen von C-Quelltexten 
erstellen. Die Ausgabe kann über Kommandozeilenargumente flexibel gesteuert 
werden. Dies ist eine verbesserte Version von cflow, die gut mit GNU make, 
gcc und bash zusammenarbeitet.

Installieren Sie Cflow, falls Sie C-Programmierer sind und die Aufrufstruktur 
Ihrer C-Quelltexte untersuchen wollen.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/bin
make PREFIX=$RPM_BUILD_ROOT/usr install

install -d $RPM_BUILD_ROOT/usr/man/man1
install -m 644 %{name}.1 $RPM_BUILD_ROOT/usr/man/man1

strip $RPM_BUILD_ROOT/usr/bin/prcc
strip $RPM_BUILD_ROOT/usr/bin/prcg
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/%{name}.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc INSTALL README README.MiNT TODO cflow.txt 
/usr/bin/prcc
/usr/bin/prcg
/usr/bin/cflow
/usr/man/man1/%{name}.1.gz

%changelog
* Tue Oct 05 1999 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT (new package)

