Summary: GNU Stream Editor
Name: sed
Version: 4.2.1
Release: 1
Copyright: GPL
Group: Utilities/Text
Source0: http://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.bz2
Prereq: /sbin/install-info
Buildroot: /var/tmp/sed-root
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): GNU Stream Editor
Summary(fr): Éditeur de flot de GNU
Summary(tr): GNU dosya iþleme aracý

%description
Sed copies the named files (standard input default) to the standard output, 
edited according to a script of commands.

%description -l de
Sed kopiert die genannten Dateien (Standardeingabe-Einstellung) nach
Bearbeitung anhand eines Befehlsskripts auf die Standardausgabe.  

%description -l fr
sed copie les fichiers indiqués (l'entrée standard par défaut), modifiés en 
fonction d'un script de commandes, vers la sortie standard.

%description -l tr
Sed, belirtilen dosyalarý, verilen komutlara göre iþleyerek standart çýktýya
kopyalar. Genellikle, metin dosyalarýnda bir katarýn yerine baþka bir katar
yazmakta kullanýlýr.

%prep
%setup -q

%build
gl_cv_func_working_mkstemp=yes \
CFLAGS="$RPM_OPT_FLAGS" \
./configure --prefix=/usr

make
strip sed/sed
stack --fix=256k sed/sed
#cat <<EOF
#WARNING: The test suite (especially the dc test) may take considerable
#time.  If you are fed up with waiting log into another console and
#kill the sed process.  This will not terminate the build process.
#EOF
#make check || :

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT/usr exec_prefix=$RPM_BUILD_ROOT/usr install

( cd $RPM_BUILD_ROOT
  mkdir bin
  mv usr/bin/sed bin/sed
  rmdir usr/bin
  gzip -9nf usr/share/info/sed.info*
  rm -f usr/info/dir
  gzip -9nf usr/share/man/man1/sed.1
)

%post
/sbin/install-info /usr/share/info/sed.info.gz /usr/share/info/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete /usr/share/info/sed.info.gz /usr/share/info/dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS BUGS NEWS README
/bin/sed 
/usr/share/info/sed.info*
/usr/share/man/man1/sed.1.gz

%changelog
* Fri Aug 20 2010 Keith Scroggins <kws@radix.net>
- Built latest version

* Fri Aug 13 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Removed test (never fails but takes a helluva long time)
