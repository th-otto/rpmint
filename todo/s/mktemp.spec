Summary: mktemp - a program for safely making tmp files
Name: mktemp
%define version 1.4
Version: %{version}
Release: 1
Copyright: BSD
Group: Utilities/System
Source: ftp://freestuff.cs.colorado.edu/pub/OpenBSD/src/usr.bin/mktemp-1.4.tar.gz
Patch: mktemp-1.4-linux.patch
Url: http://www.openbsd.org
Buildroot: /var/tmp/mktemp
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): mktemp - ein Programm zur Erstellung von sicheren tmp-Dateien
Summary(fr): mktemp - un program pour créer des fichiers temporaires en toute sécurité.
Summary(tr): Güvenli bir þekilde geçici dosya oluþturma programý

%description
mktemp is a small utility that interfaces to the mktemp() function
call to allow shell scripts and other programs to use files in /tmp
safely.

%description -l de
mktemp ist ein kleines Utility, das eine Schnittstelle zum mktemp()-
Funktionsaufruf bereitstellt, damit Shell-Skripts und andere Programme 
Dateien in /tmp ohne Risiko benutzen können. 

%description -l fr
mktemp est un petit utilitaire qui s'interface a l'appel de la
fonction mktemp() pour permettre aux scripts shell et aux autres
programmes d'utiliser sans danger les fichiers de /tmp.

%description -l tr
mktemp, kabuk yorumlayýcýlarý ve diðer programlarca /tmp dizininde güvenli bir
þekilde dosya oluþturmada kullanýlan mktemp() fonksiyonuna arayüz saðlayan
ufak bir programdýr.

%prep
%setup
%patch -p1

%build
make CFLAGS="$RPM_OPT_FLAGS -D__progname=program_invocation_short_name"

%install
mkdir -p /var/tmp/mktemp/usr/bin /var/tmp/mktemp/usr/man/man1
make ROOT="$RPM_BUILD_ROOT" install
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/mktemp.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
/bin/mktemp
/usr/man/man1/mktemp.1.gz

