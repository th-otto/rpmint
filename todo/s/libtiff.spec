Summary       : A library of functions for manipulating TIFF format image files.
Name          : libtiff
Version       : 3.5.5
Release       : 1
Copyright     : distributable
Group         : Development/Libraries

Packager      : Guido Flohr <guido@freemint.de>
Vendor        : Sparemint
URL           : http://www.libtiff.org/

BuildRequires : zlib-devel libjpeg-devel
Requires      : zlib-devel libjpeg-devel

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: http://www.libtiff.org/tiff-v%{version}.tar.gz
Source1: tiff-to-ps.fpi
Patch0:  tiff-v3.5-shlib.patch
Patch1:  libtiff-v3.4-arm.patch
Patch2:  libtiff-v3.5.4-codecs.patch
Patch3:  libtiff-v3.5.4-mandir.patch
Patch4:  libtiff-v3.5.5-buildroot.patch
Patch5:  libtiff-v3.5.5-test.patch
Patch6:  libtiff-v3.5.5-steve.patch
Patch7:  libtiff-v3.5.5-mint-config.patch
Patch8:  libtiff-mintcnf.patch


Summary(de)   : Library zum Verwalten von TIFF-Dateien
Summary(fr)   : Bibliothèque de gestion des fichiers TIFF
Summary(tr)   : TIFF dosyalarýný iþleme kitaplýðý

%description
This package is a library of functions that manipulate TIFF images.

%package devel
Summary: headers and static libraries for developing programs using libtiff
Group: Development/Libraries
Requires: libtiff
Summary(de): Headers und statische Libraries zur Entwicklung von Programmen  unter Verwendung von libtiff
Summary(fr): en-têtes et bibliothèques statiques pour développement avec libtiff"
Summary(tr): libtiff kitaplýðýyla geliþtirme için gerekli dosyalar

%description devel
This package is all you need to develop programs that manipulate tiff
images.

%description -l de devel
Dieses Paket enthält alles, was Sie zum Entwickeln von Programmen
zum Bearbeiten von tiff-Bildern benötigen.

%description -l de
Eine Library von Funktionen zur Manipulation von TIFFs.

%description -l fr devel
Ce package contient tout le nécessaire pour réaliser des programmes
manipulant des images au format tiff.

%description -l fr
Bibliothèque de fonctions pour manipuler des images TIFF."

%description -l tr devel
tiff resimlerini iþleyen programlar yazmak için gerekli dosyalar bu pakette
yer alýr.

%description -l tr
Bu paket TIFF resimlerini iþleyen fonksiyonlardan oluþan bir kitaplýktýr.


%prep
%setup -q -n tiff-v%{version}
#%patch0 -p1 -b .shlib
%patch1 -p1 -b .arm
#%patch2 -p1 -b .codecs
%patch3 -p1 -b .mandir
%patch4 -p1 -b .buildroot
%patch5 -p1 -b .test
%patch6 -p1 -b .steve
%patch7 -p1 -b .mint-config
find . -type d -name CVS | xargs -r rm -frv


%build
./configure <<EOF
no
%{_prefix}/bin
%{_prefix}/lib
%{_prefix}/include
%{_prefix}/share/man
${RPM_DOC_DIR}/%{name}-%{version}
bsd-source-cat
yes
EOF
mv libtiff/port.h libtiff/port.h.generated
patch -p1 -i ${RPM_SOURCE_DIR}/libtiff-mintcnf.patch
make COPTS="-Dunix" OPTIMIZER="${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/{bin,include,lib}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/{man1,man3}

make install

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/rhs/rhs-printfilters
install -m755 %{SOURCE1} ${RPM_BUILD_ROOT}%{_prefix}/lib/rhs/rhs-printfilters

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=96k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc COPYRIGHT README VERSION
%{_prefix}/bin/*
%{_prefix}/lib/rhs/*/*
%{_prefix}/share/man/man1/*

%files devel
%defattr(-,root,root)
%doc TODO html
%{_prefix}/include/*
%{_prefix}/lib/libtiff.a
%{_prefix}/share/man/man3/*


%changelog
* Sat Dec 23 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 3.5.5

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55
