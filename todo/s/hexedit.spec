Summary: Show a file both in ASCII and in hexadecimal.
Name: hexedit
Version: 1.0.0
Release: 1
Copyright: GPL
Group: Applications/Editors
Url: http://www.chez.com/prigaux 
Source: ftp://sunsite.unc.edu/pub/Linux/utils/file/hex/%{name}-%{version}.src.tgz
Buildroot: /var/tmp/hex-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Summary(de): Zeigt eine Datei hexadezimal und in ASCII an.

%description
Hexedit shows a file both in ASCII and in hexadecimal. The file can be a 
device as the file is not whole read. You can modify the file and search 
through it. You have also copy&paste and save to file functions, and you 
can truncate or append to the file. Modifications are shown in bold.

Install hexedit if you need a tool for showing files in ASCII and in 
hexadecimal.

%description -l de
Mit hexedit können Sie eine Datei hexadezimal oder in ASCII ansehen und 
editieren. Die Datei kann auch eine Gerätedatei sein, da sie nicht als 
ganzes gelesen wird. Sie können die Datei verändern und in ihr suchen. 
Es gibt auch Copy&Paste und Exportfunktionen, und Sie können die Datei 
verkürzen oder verlängern. Veränderungen werden hervorgehoben.

Installieren Sie hexedit, falls Sie ein Werkzeug benötigen, das Dateien 
in ASCII oder hexadezimal anzeigen kann.

%prep
%setup -q -n hexedit

%build
./configure --prefix=/usr
make 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1

install -m 755 -o root -g root -s hexedit $RPM_BUILD_ROOT/usr/bin
strip $RPM_BUILD_ROOT/usr/bin/%{name}

install -m 644 -o root -g root $RPM_BUILD_DIR/hexedit/%{name}.1 $RPM_BUILD_ROOT/usr/man/man1 
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/%{name}.1

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING TODO hexedit-1.0.0.lsm
/usr/bin/hexedit
/usr/man/man1/hexedit.1.gz

%changelog
* Sun Sep 12 1999 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT 
                