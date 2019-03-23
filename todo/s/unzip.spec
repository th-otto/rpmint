Summary: A utility for unpacking zip files.
Summary(de): Ein Tool zum Entpacken von zip Files.
Summary(cs): Programy pro rozbalov�n� soubor� ve form�tu ZIP.
Name: unzip
Version: 5.50
Release: 1 
Copyright: distributable
Group: Applications/Archiving
Source: ftp://ftp.info-zip.org/pub/infozip/src/unzip550.tar.gz 
Patch0: unzip-5.50-mint.patch
BuildRoot: /var/tmp/unzip-root
Packager: Frank Naumann <fnaumann@freemint.de>
Vendor: Sparemint

%description
The unzip utility is used to list, test, or extract files from a zip
archive.  Zip archives are commonly found on MS-DOS systems.  The zip
utility, included in the zip package, creates zip archives.  Zip and
unzip are both compatible with archives created by PKWARE(R)'s PKZIP for
MS-DOS, but the programs' options and default behaviors do differ in some
respects.

Install the unzip package if you need to list, test or extract files from
a zip archive.

%description -l de
Das unzip Tool kann zip Archive testen, auspacken oder den Inhalt anzeigen.
Zip Archive finden sich vorrangig auf MS-DOS Systemen. Das unzip Tool ist
kompatibel zu PKUNZIP.

Installiere das unzip Paket wenn du zip Archive testen, auspacken oder
den Inhalt auflisten willst.

%description -l cs
Program unzip umo��uje otestovat, rozbalit nebo vypsat soubory z arch�vu
form�tu ZIP (zn�m� z prost�ed� DOSu). Dal�� program zip vytv��� archivy
ZIP; oba programy jsou slu�iteln� s archivy vytvo�en�mi programy
PKZIP a PKUNZIP pro MS-DOS od firmy PKWARE, ale volby program�
a jejich v�choz� chov�n� je v mnoha p��padech odli�n�.

Nainstalujte si bal��ek unzip, pokud pot�ebujete testovat, rozbalovat,
nebo vypisovat soubory z arch�v� ve form�tu ZIP.

%prep
%setup -q
ln -s unix/Makefile Makefile
%patch0 -p1

%build
make m68k-atari-mint

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT/usr install

strip $RPM_BUILD_ROOT/usr/bin/unzip
strip $RPM_BUILD_ROOT/usr/bin/funzip
strip $RPM_BUILD_ROOT/usr/bin/unzipsfx
stack --fix=96k $RPM_BUILD_ROOT/usr/bin/unzip || :
stack --fix=96k $RPM_BUILD_ROOT/usr/bin/funzip || :
stack --fix=96k $RPM_BUILD_ROOT/usr/bin/unzipsfx || :
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README BUGS COPYING INSTALL
/usr/bin/unzip
/usr/bin/funzip
/usr/bin/unzipsfx
/usr/bin/zipinfo
/usr/man/man1/unzip.1.gz
/usr/man/man1/unzipsfx.1.gz
/usr/man/man1/zipinfo.1.gz
/usr/man/man1/funzip.1.gz

%changelog
* Sat Feb 18 2003 Jan Krupka <jkrupka@volny.cz>
- update to 5.50
- added %description cs and Summary(cs)

* Thu Mar 23 2000 Frank Naumann <fnaumann@freemint.de>
- update to 5.40

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
- added %description de and Summary(de)

