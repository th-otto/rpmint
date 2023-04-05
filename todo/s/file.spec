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
Sie können dieses Paket verwenden, um zu bestimmen, welches Format
eine bestimmte Datei hat. Wird durch fsck eine Datei in lost+found
gespeichert, können Sie 'file' ausführen, um herauszufinden, ob Sie
sie mit 'more' einsehen können, oder ob es sich um ein Binärprogramm
handelt Das Programm erkennt u.a. ELF-Binärprogramme,
System-Libraries, RPM-Pakete und viele Grafikformate.

%description -l fr
Ce paquetage sert à trouver le type du fichier que vous recherchez sur
votre système. Par exemple, si un fsck fait qu'un fichier a été stocké
dans lost+found, vous pouvez lancer file dessus pour savoir si on peut
faire un more, ou s'il s'agit d'un binaire. Il reconnaît de nombreux
types de fichiers dont les binaires ELF, les bibliothèques systèmes,
les paquetages RPM et de nombreux formats graphiques différents.

%description -l pl
Pakiet ten jest przydatny je¿eli chcesz rozpoznaæ typ plików w twoim
systemie. Na przyk³ad je¿eli fsck zdeponuje jakie¶ pliki w katalogu
lost+found, mo¿esz uruchomiæ file na zdeponowanym pliku i zobaczyæ
jaki to jest typ pliku, jest to metoda bezpieczniejsza ni¿ 'more', ze
wzglêdu na to, ¿e to mo¿e byæ plik binarny. File potrafi rozpoznaæ
wiele typów plików np. binarny ELF, biblioteki systemowe, pakiety RPM
oraz wiele ró¿nych formatów graficznych i d¼wiêkowych.

%description -l tr
file, bir dosyayý inceleyerek ne tür bir dosya olduðu konusunda size
bir fikir verebilir. Böylece uzantýsýndan ve adýndan ne olduðunu
çýkaramadýðýnýz bir dosyayý hangi yazýlým ile kullanabileceðinize ya
da ne yapacaðýnýza karar verebilisiniz. file, temel dosya tiplerini,
çoðu grafik formatýný, çalýþtýrýlabilir dosyalarý, sistem
kitaplýklarýný vs. tanýyabilir.


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
