Summary: An interpreted, interactive object-oriented programming language.
Summary(de): Eine interpretierte, interaktive, objektorientierte Programmiersprache
Name: python
Version: 2.3.4
Release: 1
Vendor: Sparemint
Packager: Mark Duckworth <mduckworth@atari-source.com>
Copyright: distributable
Group: Development/Languages
Source0: ftp://ftp.python.org/pub/python/2.3.4/Python-2.3.4.tar.bz2
Patch0: python-no_ndbm.patch
Patch1: python-path.patch
Patch2: python-mintsetupdist.patch
Patch3: python-mintnosharedmod.patch
Patch4: python-mintsocketmodule.patch
Buildroot: /var/tmp/python-root
#MiNT Specific
BuildRequires: readline-devel >= 4.2
BuildRequires: zlib-devel >= 1.2.1

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that
need a programmable interface. This package contains most of the
standard Python modules, as well as modules for interfacing to the
Tix widget set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%description -l de
Python ist eine interpretierte, interaktive, objektorientierte
Programmiersprache, vergleichbar zu Tcl, Perl, Scheme oder Java. Python
enthält Module, Klassen, Exceptions, High-Level dynamische Datentypen und
dynamisches Typisieren. Python unterstützt Interfaces zu vielen
Systemaufrufen und Libraries, sowie verschiedene Fenstersysteme (X11, Motif,
Tk, Mac und MFC)

Programmierer können neue built-in-Module für Python in C oder C++
schreiben. Python kann auch als Erweiterungssprache für Applikationen
benutzt werden, die ein programmierbares Interface brauchen. Dieses Paket
enthält die meisten Standard-Python-Module, und Module zum Ansprechen von
Tix (Tk-widget set) und RPM.

Dokumentationen zu Python sind in python-docs enthalten.

%package devel
Summary: The libraries and header files needed for Python development.
Summary(de): Libraries und Header-Dateien fuer Python-Entwicklung.
Requires: python = 2.3.4
Group: Development/Libraries

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%description -l de devel
Des Python-Programmiersprachen-Interpreter kann durch dynamisch ladbare
Erweiterungen erweitert und in andere Programme eingebunden werden.
Dieses Paket enthält die Header und Libraries für diese Aufgaben.

Installieren Sie python-devel, wenn Sie Python-Erweiterungen entwickeln
wollen. Sie brauchen außerdem das Python-Paket. Wahrscheinlich brauchen Sie
auch python-docs, das Python-Dokumentationen enthält.

%package docs
Summary: Documentation for the Python programming language.
Summary(de): Dokumentation zur Python-Programmiersprache.
Group: Documentation

%description docs
The python-docs package contains documentation on the Python
programming language and interpreter.  The documentation is provided
in ASCII text files and in LaTeX source files.

Install the python-docs package if you'd like to use the documentation
for the Python language.

%description -l de docs
Das python-docs-Paket enthält Dokumentationen zur Python-Programmiersprache
und dem Interpreter. Die Dokumentation ist als ASCII-Text und als
LaTeX-Source enthalten.

Installieren Sie python-docs, wenn Sie die Dokumentation zur Python-Sprache
brauchen.

%prep
%setup -q -n Python-2.3.4
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# I really have no idea why this is necessary, but should be no harm.
%patch4 -p1

if ! [ -e /usr/lib/libdb1* ]; then # glibc < 2.1.x
  for i in 1 2 3 4 5; do
    perl -p -i -e "s/db1/db/" Modules/Setup.dist
  done
fi

cp Lib/lib-old/rand.py Lib

%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" MACHDEP=$RPM_ARCH ./configure --prefix=/usr --with-threads --with-pth

make OPT="-pipe $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
stack -S 512K ./python
strip ./python
make install DESTDIR=$RPM_BUILD_ROOT

rm -f modules-list.full
for n in $RPM_BUILD_ROOT/usr/lib/python2.3/*; do
  [ -d $n ] || echo $n
done >> modules-list.full

sed -e "s|$RPM_BUILD_ROOT||g" < modules-list.full > modules-list

%clean
rm -rf $RPM_BUILD_ROOT
rm -f modules-list modules-list.full

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
/usr/lib/python2.3/*

%files devel
%defattr(-,root,root)
/usr/include/python2.3

%files docs
%defattr(-,root,root)
%doc LICENSE Doc

%changelog
* Wed Sep 14 2004 Mark Duckworth <mduckworth@atari-source.com>
- Updated to the latest version

* Mon Aug 30 2004 Mark Duckworth <mduckworth@atari-source.com>
- Built against latest gemlib
- Fixed stacksize issues
- Fixed lack of stripped binary

* Sat Mar 20 2004 Mark Duckworth <mduckworth@atari-source.com>
- Changed packager due to new maintainer
- gdbm, zlib and sockets all work fine as far as I can tell.
- Bittorrent client tested works (curses one fails, headless works)

* Tue Sep 19 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- 1st release for Sparemint.
- Removed gdbm and zlib support until such time as I can get
  them to work with Python. These two modules, plus the socket module
	fail, although sockets only fail because of MiNTNet's limitations.
- Removed the tkinter package, as it doesn't really make sense for MiNT.

* Thu Sep 14 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- 1st built for Sparemint
