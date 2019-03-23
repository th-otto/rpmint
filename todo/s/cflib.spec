# cflib specfile

# Please note this file is maintained in the freemint CVS repository as
# "lib/cflib/cflib.spec.in". Most current version is avaible there and
# any modification should be stored there.

Summary       : Christian Felsch's GEM utility library
Name          : cflib
Version       : 21
Release       : 1
Copyright     : LGPL
Group         : Development/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://sparemint.atariforge.net/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz


%description
This is a utility library/toolkit that provide a lot of helper functions
for developping GEM applications.  Sorry, the documentation is all
German.

NOTE: This package has experimental support for installing ST-Guide
hypertexts with rpm.  They will get installed in /usr/GEM/stguide.
Please make sure that this directory is located on a file system that
supports long filenames.  You should then edit your stguide.inf to
make sure that ST-Guide will search that directory for hypertexts.
Also make sure that stool (or stool.tos or stool.ttp) is found either 
in /usr/GEM/stguide or in your $PATH.

You should install cflib if you would like to write GEM applications
that support recent GEM extensions without having to care about 
compatibility issues.

%description -l de
Dies ist eine Hilfsbibliothek bzw. ein Toolkit, das eine Menge n�tzlicher
Funktionen f�r die Entwicklung von GEM-Applikationen enth�lt.  Hurra,
die Dokumentation ist komplett auf Deutsch!

BEMERKUNG: Dieses Paket hat experimentellen Support f�r die Installation
von ST-Guide-Hypertexten. Sie werden in /usr/GEM/stguide installiert.
Dieses Verzeichnis muss auf einem Dateisystem liegen, dass lange
Dateinamen unterst�tzt.  Die Konfigurationsdatei stguide.inf sollte
entsprechend ge�ndert werden, damit der ST-Guide in diesem Verzeichnis
nach Hypertexten sucht. Es ist ferner sicherzustellen, dass stool
(oder stool.tos oder stool.ttp) entweder in /usr/GEM/stguide oder
in $PATH gefunden werden kann.

Sie sollten die Cflib installieren, wenn Sie GEM-Applikationen schreiben
wollen, die alle neueren GEM-Erweiterungen unterst�tzen, ohne sich um 
den ganzen Kompatibilit�ts-Kram k�mmern zu m�ssen.


%prep
%setup -q -n %{name}-%{version}


%build
cd cflib
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd cflib
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/include
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib
install -m 644 libcflib.a ${RPM_BUILD_ROOT}%{_prefix}/lib
install -m 644 libcflib16.a ${RPM_BUILD_ROOT}%{_prefix}/lib
install -m 644 cflib.h ${RPM_BUILD_ROOT}%{_prefix}/include

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/GEM/include
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/GEM/lib
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/GEM/stguide
ln -s %{_prefix}/lib/libcflib.a ${RPM_BUILD_ROOT}%{_prefix}/GEM/lib/
ln -s %{_prefix}/lib/libcflib16.a ${RPM_BUILD_ROOT}%{_prefix}/GEM/lib/
ln -s %{_prefix}/include/cflib.h ${RPM_BUILD_ROOT}%{_prefix}/GEM/include/
install -m 644 cflib.hyp     ${RPM_BUILD_ROOT}%{_prefix}/GEM/stguide
install -m 644 cflib.ref     ${RPM_BUILD_ROOT}%{_prefix}/GEM/stguide


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
# Try to run ST-Guide's stool.
found_stool=yes
PATH=%{_prefix}/GEM/stguide:/usr/local/GEM/stguide:/usr/GEM/stguide:"$PATH"
export PATH
stool  >/dev/null 2>&1 || \
stool.tos  >/dev/null 2>&1 || \
stool.ttp  >/dev/null 2>&1 || \
found_stool=no
if test $found_stool = "no"; then
	exec 1>&2
	echo "WARNING: Could not run stool to update ST-Guide"
	echo "catalog file.  If you have stool you should "
	echo "install it in "%{_prefix}/GEM/stguide" or"
	echo "in your PATH as stool, stool.tos or stool.ttp."
fi

%postun
# Try to run ST-Guide's stool.
found_stool=yes
PATH=%{_prefix}/GEM/stguide:/usr/local/GEM/stguide:/usr/GEM/stguide:"$PATH"
export PATH
stool  >/dev/null 2>&1 || \
stool.tos  >/dev/null 2>&1 || \
stool.ttp  >/dev/null 2>&1 \
found_stool=no
if test $found_stool = "no"; then
	exec 1>&2
	echo "WARNING: Could not run stool to update ST-Guide"
	echo "catalog file.  If you have stool you should "
	echo "install it in "%{_prefix}/GEM/stguide" or"
	echo "in your PATH as stool, stool.tos or stool.ttp."
fi


%files
%defattr(-,root,root)
%doc cflib/COPYING.LIB cflib/LiesMich
%doc cflib/demo cflib/intrface
%doc cflib/ChangeLog*
%{_prefix}/lib/lib*.a
%{_prefix}/include/*.h
%{_prefix}/GEM/lib/lib*.a
%{_prefix}/GEM/include/*.h
%{_prefix}/GEM/stguide/cflib.hyp
%{_prefix}/GEM/stguide/cflib.ref


%changelog
* Sun Jul 18 2004 Frank Naumann <fnaumann@freemint.de>
- updated to version 0.21.0, using the new gemlib 0.43.2

* Tue Jan  6 2004 Standa Opichal <opichals@seznam.cz>
- updated to version 0.20.1, using the new gemlib 0.43.1

* Thu Feb 15 2001 Frank Naumann <fnaumann@freemint.de>
- updated to version 0.20.0

* Mon May 26 2000 Frank Naumann <fnaumann@freemint.de>
- patch in objc.c for new MiNTLib, replaced itoa by ltoa

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55
- small patch for new MiNTLib
- removed CR in cflib.h

* Thu Oct 21 1999 Guido Flohr <guido@freemint.de>
- Initial version for Sparemint
