Summary       : A utility for determining file types.
Summary(de)   : Ein Hilfsmittel, um Dateitypen zu bestimmen.
Name          : file
Version       : 3.36
Release       : 2
License       : Distributable
Group         : Applications/File
Group(de)     : Applikationen/Datei
Group(pl)     : Aplikacje/Pliki

Packager      : Edgar Aichinger <eaiching@t0.or.at>
Vendor        : Sparemint

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
Source1: zisofs.magic
Source2: magic.mime
Patch0: file-3.36-sparc.patch
Patch1: file-3.36-tfm.patch
Patch2: file-3.36-ia64.patch
Patch3: file-3.36-elf.patch
Patch4: file-3.36-mint.patch


%description
This package is useful for finding out what type of file you are
looking at on your system. For example, if an fsck results in a file
being stored in lost+found, you can run file on it to find out if it's
safe to 'more' it or if it's a binary. It recognizes many file types,
including ELF binaries, system libraries, RPM packages, and many
different graphics formats.

%description -l de
Sie k�nnen dieses Paket verwenden, um zu bestimmen, welches Format
eine bestimmte Datei hat. Wird durch fsck eine Datei in lost+found
gespeichert, k�nnen Sie 'file' ausf�hren, um herauszufinden, ob Sie
sie mit 'more' einsehen k�nnen, oder ob es sich um ein Bin�rprogramm
handelt Das Programm erkennt u.a. ELF-Bin�rprogramme,
System-Libraries, RPM-Pakete und viele Grafikformate.

%description -l fr
Ce paquetage sert � trouver le type du fichier que vous recherchez sur
votre syst�me. Par exemple, si un fsck fait qu'un fichier a �t� stock�
dans lost+found, vous pouvez lancer file dessus pour savoir si on peut
faire un more, ou s'il s'agit d'un binaire. Il reconna�t de nombreux
types de fichiers dont les binaires ELF, les biblioth�ques syst�mes,
les paquetages RPM et de nombreux formats graphiques diff�rents.

%description -l pl
Pakiet ten jest przydatny je�eli chcesz rozpozna� typ plik�w w twoim
systemie. Na przyk�ad je�eli fsck zdeponuje jakie� pliki w katalogu
lost+found, mo�esz uruchomi� file na zdeponowanym pliku i zobaczy�
jaki to jest typ pliku, jest to metoda bezpieczniejsza ni� 'more', ze
wzgl�du na to, �e to mo�e by� plik binarny. File potrafi rozpozna�
wiele typ�w plik�w np. binarny ELF, biblioteki systemowe, pakiety RPM
oraz wiele r�nych format�w graficznych i d�wi�kowych.

%description -l tr
file, bir dosyay� inceleyerek ne t�r bir dosya oldu�u konusunda size
bir fikir verebilir. B�ylece uzant�s�ndan ve ad�ndan ne oldu�unu
��karamad���n�z bir dosyay� hangi yaz�l�m ile kullanabilece�inize ya
da ne yapaca��n�za karar verebilisiniz. file, temel dosya tiplerini,
�o�u grafik format�n�, �al��t�r�labilir dosyalar�, sistem
kitapl�klar�n� vs. tan�yabilir.


%prep
%setup -q
%patch0 -p1 -b .sparc
%patch1 -p1 -b .tfm
%patch2 -p1 -b .ia64
%patch3 -p1 -b .elf
%patch4 -p1 -b .mint


%build
aclocal
autoconf
rm -f install-sh missing mkinstalldirs
automake --copy --add-missing

CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--enable-fsect-man5

make CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

cat %{SOURCE1} >> ${RPM_BUILD_ROOT}%{_prefix}/share/magic
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/share/

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

./file -m ${RPM_BUILD_ROOT}%{_prefix}/share/magic -c -C

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/share/magic*
%{_prefix}/share/man/man*/*


%changelog
* Thu Sep 13 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 3.36

* Fri Apr 21 2000 Edgar Aichinger <eaiching@t0.or.at>
- build against mintlibs 0.55.2

* Tue Apr 4 2000 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT 
- compressed man pages
