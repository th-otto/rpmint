Summary: A program for making transparent GIFs from non-transparent GIFs.
Name: giftrans
Version: 1.12.2
Release: 3
Copyright: BSD
Group: Applications/Multimedia
Source: ftp://ftp.rz.uni-karlsruhe.de/pub/net/www/tools/giftrans-1.12.2.tar.gz
Patch: giftrans.mint.patch
Buildroot: /var/tmp/giftrans-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Summary(de): Ein Programm, das transparente GIFs aus nicht-transparenten GIFs erzeugt.

%description
Giftrans will convert an existing GIF87 file to GIF89 format. In other
words, Giftrans can make one color in a .gif image (normally the
background) transparent.

Install the giftrans package if you need a quick, small, one-purpose
graphics program to make transparent .gifs out of existing .gifs.

%description -l de
Giftrans konvertiert eine bestehende GIF87 Datei ins GIF89-Format. Anders
ausgedrückt, kann giftrans eine Farbe in einem .gif Bild (normalerweise der 
Hintergrund) transparent machen.

Installieren Sie giftrans, wenn Sie ein schnelles, kleines Grafikprogramm
brauchen, um transparente .gifs aus bestehenden Bildern zu erzeugen.

%prep
%setup
%patch -p1 -b .mint

%build
gcc -Dvoidd=void $RPM_OPT_FLAGS -s -o giftrans giftrans.c
strip giftrans

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/doc/giftrans-1.12.2
mkdir -p $RPM_BUILD_ROOT/usr/lib/giftrans
install -s -m 755 giftrans $RPM_BUILD_ROOT/usr/bin
install giftrans.1 $RPM_BUILD_ROOT/usr/man/man1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/%{name}.1
install README.MiNT $RPM_BUILD_ROOT/usr/doc/giftrans-1.12.2
install rgb.txt $RPM_BUILD_ROOT/usr/lib/giftrans

%clean
rm -rf $RPM_BUILD_ROOT
 

%files
/usr/bin/giftrans
/usr/man/man1/giftrans.1.gz
/usr/lib/giftrans/rgb.txt
%doc README.MiNT

%changelog
* Fri Sep 03 1999 Edgar Aichinger <eaiching@t0.or.at>
- corrected missing readme
- strip binary

* Thu Sep 02 1999 Edgar Aichinger <eaiching@t0.or.at>
- changed location of "rgb.txt" (in /usr/lib/giftrans/)
- added docs in /usr/doc/giftrans-1.12.2
- adapted specfile to reflect these changes
- compressed man page

* Tue Aug 31 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT 
- added Requires, Vendor, Packager, german Summary/Description
