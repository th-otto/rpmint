#
# spec file for udo
#
# Written by Volker Janzen
#
# Build RPMs with: rpm -ba udo.spec
#
# Query example: rpm -q -l -p udo-6.2.1-1.i386.rpm
#
# These things have to be fixed for a new RPM:
# - Release: increase by 1, if no new upstream version is packaged,
#            else set it back to 1
# - Version: change if upstream version has changed
# - Source : change if new upstream version is packaged
#
Summary       : Universal DOcument (UDO) - text processing utility
Name          : udo
Version       : 6.4.1
Release       : 1
Copyright     : GPL
Group         : Applications/Text

Packager      : Martin Tarenskeen <m.tarenskeen@zonnet.nl>
Vendor        : Sparemint
URL           : http://www.udo-open-source.org/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.udo-open-source.org/download/sources/udo_%{version}_src.tar.gz


%description
UDO is a powerful and multipurpose utility for making documentation or any
other text file that is needed in one text format or more. UDO documents can
be converted to ASCII, HTML, LaTeX, nroff, PostScript, RTF, ST-Guide and many
more. Though UDO is powerful, it's quite easy to understand and to use.

%package -n udo-doc-en
Summary: UDO Documentation (English)
Group         : Applications/Text

%description -n udo-doc-en
English documentation for UDO.
UDO is a powerful and multipurpose utility for making documentation or any
other text file that is needed in one text format or more. UDO documents can
be converted to ASCII, HTML, LaTeX, nroff, PostScript, RTF, ST-Guide and many
more. Though UDO is powerful, it's quite easy to understand and to use.

%package -n udo-doc-de
Summary: UDO Dokumentation (Deutsch)
Group         : Applications/Text

%description -n udo-doc-de
Deutsche Dokumentation fšr UDO
UDO ist ein m„chtiges und multifunktionales Werkzeug um Dokumentationen 
oder andere Textdateien zu erstellen, die in mehr als einem Format 
ben”tigt werden. UDO Dokumente k”nnen unter anderem in ASCII, HTML, 
LaTeX, nroff, PostScript, RTF und ST-Guide konvertiert werden. UDO ist 
dadurch m„chtig, aber immer noch einfach zu verstehen und zu benutzen.

%prep
%setup -q -n udo_%{version}

%build
cd Source
make -f Makefile.linux CFLAGS="$RPM_OPT_FLAGS -Wall -D__LINUX__"
stack -S 128K udo
install -d ../Guide/eng/tmp/udo
install -d ../Guide/eng/tmp/html
install -d ../Guide/ger/tmp/udo
install -d ../Guide/ger/tmp/html

cd ../Guide/eng/manual
cp -r images ../tmp/html/
cp -rf * ../tmp/udo

../../../Source/udo --nroff -o ../tmp/udo.1 manpage.u
gzip -9 ../tmp/udo.1

../../../Source/udo -a -o ../tmp/udo.txt index.u 
../../../Source/udo --html -o ../tmp/html/index.html index.u

cd ../../ger/manual
cp -r images ../tmp/html/ 
cp -rf * ../tmp/udo

../../../Source/udo -a -o ../tmp/udo.txt index.u  
../../../Source/udo --html -o ../tmp/html/index.html index.u


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd Source
install -d ${RPM_BUILD_ROOT}%{_mandir}/man1
install -d -p ${RPM_BUILD_ROOT}%{_bindir}
install -d ${RPM_BUILD_ROOT}%{_docdir}/udo-%{version}
install -m 644 ../Guide/eng/tmp/udo.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1
install -m 644 ../README ${RPM_BUILD_ROOT}%{_docdir}/udo-%{version}
install -m 755 udo ${RPM_BUILD_ROOT}%{_bindir}
strip ${RPM_BUILD_ROOT}%{_bindir}/udo

install -d -p ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-en-%{version}/udo
install -d ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-de-%{version}/udo
install -d ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-en-%{version}/html/images
install -d ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-de-%{version}/html/images
cp -r ../Guide/eng/manual ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-en-%{version}/udo/
cp ../Guide/eng/tmp/udo.txt ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-en-%{version}/
rm -f ../Guide/eng/tmp/html/index.ulh
cp -r ../Guide/eng/tmp/html ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-en-%{version}/
cp ../Guide/eng/tmp/udo.txt ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-en-%{version}/
cp -r ../Guide/ger/manual ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-de-%{version}/udo/
cp ../Guide/ger/tmp/udo.txt ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-de-%{version}/
rm -f ../Guide/ger/tmp/html/index.ulh
cp -r ../Guide/ger/tmp/html ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-de-%{version}/
cp ../Guide/ger/tmp/udo.txt ${RPM_BUILD_ROOT}%{_docdir}/udo-doc-de-%{version}/

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_mandir}/man1/*

%files -n udo-doc-en
%defattr(-,root,root)
%doc Guide/eng/tmp/udo Guide/eng/tmp/html Guide/eng/tmp/udo.txt

%files -n udo-doc-de
%defattr(-,root,root)
%doc Guide/ger/tmp/udo Guide/ger/tmp/html Guide/ger/tmp/udo.txt

%changelog
* Sat Oct 10 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- Updated to udo_6.4.1
- English and German documentation packages

* Tue Jan 13 2004 Frank Naumann <fnaumann@freemint.de>
- corrected specfile for Sparemint
* Wed Jan 07 2004 Volker Janzen <webmaster@udo-open-source.org>
- new manpage is used now
* Sat Dec 27 2003 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- revised specfile
