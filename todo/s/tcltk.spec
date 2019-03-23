%define	tclvers		8.0.5
%define tclXvers	8.0.4
%define	expvers		5.28
%define	Tixvers		4.1.0
%define	itclvers	3.0.1

Summary: A Tcl/Tk development environment: tcl, tk, tix, tclX, expect, and itcl.
Name: tcltk
Version: %{tclvers}
Release: 1
Copyright: BSD
Group: Development/Languages
Source0: ftp://ftp.scriptics.com/pub/tcl/tcl8_0/tcl%{tclvers}.tar.gz
Source1: ftp://ftp.scriptics.com/pub/tcl/tcl8_0/tk%{tclvers}.tar.gz
Source2: ftp://ftp.cme.nist.gov/pub/expect/expect.tar.gz
Source3: ftp://ftp.neosoft.com/pub/tcl/TclX/tclX%{tclXvers}.tar.gz
Source4: ftp://ftp.xpi.com/pub/ioi/Tix%{Tixvers}.006.tar.gz
Source5: ftp://ftp.tcltk.com/pub/itcl/itcl%{itclvers}.tar.gz
Patch0:  tcltk-8.0-ieee.patch
Patch1:  tcl8.0.3-glibc21.patch
Patch2:  tcl8.0.5-sigpwr.patch
Patch10: expect-5.24-mkpasswd.patch
Patch11: expect-5.26-alpha.patch
Patch12: expect-5.26-glibc21.patch
Patch13: expect-5.28-jbj.patch
Patch14: expect-autopasswd.patch
Patch20: tix-4.1.0.6-perf.patch
Patch30: tclX-8.0.4-jbj.patch
Patch31: tclX-runtcl.patch
Patch33: tcltk-8.0.5-mint.patch
Packager: Frank Naumann <fnaumann@freemint.de>
Vendor: Sparemint
Prefix: %{_prefix}
Docdir: %{_prefix}/doc
BuildRoot: %{_tmppath}/%{name}-root

%description
Tcl is a simple scripting language designed to be embedded into other
applications.  Tcl is designed to be used with Tk, a widget set.

%package -n tcl
Summary: An embeddable scripting language.
Group: Development/Languages
URL: http://www.scriptics.com

%description -n tcl
Tcl is a simple scripting language designed to be embedded into other
applications.  Tcl is designed to be used with Tk, a widget set, which
is provided in the tk package.  This package also includes tclsh, a
simple example of a Tcl application.

If you're installing the tcl package and you want to use Tcl for
development, you should also install the tk and tclx packages.

%package -n tk
Summary: The Tk GUI toolkit for Tcl, with shared libraries.
Group: Development/Languages
URL: http://www.scriptics.com

%description -n tk
Tk is a widget set for the X Window System that is designed to work
closely with the Tcl scripting language. It allows you to write simple
programs with full featured GUI's in only a little more time then it
takes to write a text based interface. Tcl/Tk applications can also be
run on Windows and Macintosh platforms.

%package -n expect
Version: %{expvers}
Summary: A tcl extension for simplifying program-script interaction.
Group: Development/Languages

%description -n expect
Expect is a tcl extension for automating interactive applications such
as telnet, ftp, passwd, fsck, rlogin, tip, etc.  Expect is also useful
for testing those applications.  Expect makes it easy for a script to
control another program and interact with it.

Install the expect package if you'd like to develop scripts which
interact with interactive applications.  You'll also need to install
the tcl package.

%package -n tclx
Summary: Tcl/Tk extensions for POSIX systems.
Group: Development/Languages
URL: http://www.neosoft.com/

%description -n tclx
TclX is a set of extensions which make it easier to use the Tcl
scripting language for common UNIX/Linux programming tasks.  TclX
enhances Tcl support for files, network access, debugging, math,
lists, and message catalogs.  TclX can be used with both Tcl and
Tcl/Tk applications.

Install TclX if you are developing applications with Tcl/Tk.  You'll
also need to install the tcl and tk packages.

%package -n tix
Version: %{Tixvers}.6
Summary: A set of capable widgets for Tk.
Group: Development/Languages

%description -n tix
Tix (Tk Interface Extension), an add-on for the Tk widget set, is an
extensive set of over 40 widgets.  In general, Tix widgets are more
complex and more capable than the widgets provided in Tk.  Tix widgets
include a ComboBox, a Motif-style FileSelectBox, an MS Windows-style
FileSelectBox, a PanedWindow, a NoteBook, a hierarchical list, a
directory tree and a file manager.

Install the tix package if you want to try out more complicated
widgets for Tk.  You'll also need to have the tcl and tk packages
installed.

%package -n itcl
Version: %{itclvers}
Summary: Object-oriented mega-widgets for Tcl.
Group: Development/Languages

%description -n itcl
[incr Tcl] is an object-oriented extension of the Tcl language and was
created to support more structured programming in Tcl.  Tcl scripts
longer than a few thousand lines become extremely difficult to
maintain because the building blocks of vanilla Tcl are procedures and
global variables. All of these building blocks must reside in a single
global namespace and there is no support for protection or
encapsulation.

To help out with this problem, [incr Tcl] introduces the notion of
objects.  Each object is a bag of data with a set of procedures or
"methods" that are used to manipulate it.  Objects are organized into
"classes" with identical characteristics, and classes can inherit
functionality from one another.  This object-oriented paradigm adds
another level of organization on top of the basic variable/procedure
elements, and the resulting code is easier to understand and
maintain.

Install itcl if you're programming with Tcl, and you need the
object-oriented functionality that [incr Tcl] can provide.

%prep

%setup -q -c -a 1 -a 2 -a 3 -a 4 -a 5

cd tcl%{tclvers}
#%patch0 -p2 -b .ieee
%patch1 -p2 -b .glibc21
%patch2 -p2 -b .sigpwr
cd ..

cd expect-%{expvers}
%patch10 -p2 -b .mkpasswd
%patch11 -p2 -b .alpha
%patch12 -p2 -b .glibc21
%patch13 -p2 -b .jbj
%patch14 -p2 -b .autopasswd
cd ..

cd Tix%{Tixvers}
%patch20 -p2 -b .perf
cd ..

cd tclX%{tclXvers}
%patch30 -p2 -b .wrongtclXvers
cd ..

# OK, this really touches both expect & tclX
%patch31 -p1 -b .runtcl

# at last the mint patches
%patch33 -p1 -b .mint

#==========================================
%build

# make the libraries reentrant
# RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D_REENTRANT"

#------------------------------------------
# Tcl
#
cd tcl%{tclvers}/unix
rm -f configure
autoconf
libtoolize --copy --force
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix}
make
cd ../..

#------------------------------------------
# Tk
#
cd tk%{tclvers}/unix
rm -f configure
autoconf
libtoolize --copy --force
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix}
make
cd ../..

#------------------------------------------
# tclX
#
cd tclX%{tclXvers}/unix
rm -f configure
autoconf
libtoolize --copy --force
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix}
make
cd ../..

#------------------------------------------
# Expect
#
cd expect-%{expvers}
autoconf
libtoolize --copy --force
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix} \
	--with-tclconfig=../tcl%{tclvers}/unix \
	--with-tkconfig=../tk%{tclvers}/unix \
	--with-tclinclude=../tcl%{tclvers}/generic \
	--with-tkinclude=../tk%{tclvers}/generic

# XXX drill out HAVE_OPENPTY for now
# perl -pi -e 's,HAVE_OPENPTY,HAVE_OPENPTY_BUT_DONT_USE_IT,g' expect_cf.h || :
# XXX drill in HAVE_PTMX for now
# perl -pi -e 's,/* #undef HAVE_PTMX */,#define HAVE_PTMX 1,g' expect_cf.h || :
# 
# make Makefile
# 
# XXX drill out HAVE_OPENPTY for now
# perl -pi -e 's,HAVE_OPENPTY,HAVE_OPENPTY_BUT_DONT_USE_IT,g' expect_cf.h || :
# XXX drill in HAVE_PTMX for now
# perl -pi -e 's,/* #undef HAVE_PTMX */,#define HAVE_PTMX 1,g' expect_cf.h || :

make
cd ..

#------------------------------------------
# Tix
#
cd Tix%{Tixvers}/unix
rm -f configure
autoconf
libtoolize --copy --force
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix} \
	--disable-cdemos
cd tk8.0
rm -f configure
autoconf
libtoolize --copy --force
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix} \
	--disable-cdemos \
	--with-tcl=../../../tcl%{tclvers} \
	--with-tk=../../../tk%{tclvers}
make
cd ../../..

#------------------------------------------
# itcl
#
cd itcl%{itclvers}
rm -f configure
autoconf
libtoolize --copy --force
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix} \
	--exec-prefix=/foo
make
cd ..

#==========================================
%install

rm -rf $RPM_BUILD_ROOT
rm -fv *.files*

mkdir -p $RPM_BUILD_ROOT%{_prefix}

#------------------------------------------
# Tcl
#
cd tcl%{tclvers}/unix
make INSTALL_ROOT=$RPM_BUILD_ROOT install
# ln -sf libtcl8.0.so $RPM_BUILD_ROOT%{_prefix}/lib/libtcl.so
ln -sf tclsh8.0 $RPM_BUILD_ROOT%{_prefix}/bin/tclsh
cd ../..
(find $RPM_BUILD_ROOT%{_prefix}/bin $RPM_BUILD_ROOT%{_prefix}/include \
	$RPM_BUILD_ROOT%{_prefix}/man -type f -o -type l;
 find $RPM_BUILD_ROOT%{_prefix}/lib/*) | sort > tcl.files

#------------------------------------------
# Tk
#
cd tk%{tclvers}/unix
make INSTALL_ROOT=$RPM_BUILD_ROOT install
# ln -sf libtk8.0.so $RPM_BUILD_ROOT%{_prefix}/lib/libtk.so
ln -sf wish8.0 $RPM_BUILD_ROOT%{_prefix}/bin/wish
cd ../..
(find $RPM_BUILD_ROOT%{_prefix}/bin $RPM_BUILD_ROOT%{_prefix}/include \
	$RPM_BUILD_ROOT%{_prefix}/man -type f -o -type l;
 find $RPM_BUILD_ROOT%{_prefix}/lib/*) | cat - tcl.files \
	| sort | uniq -u > tk.files

#------------------------------------------
# TclX
#
cd tclX%{tclXvers}/unix
make INSTALL_ROOT=$RPM_BUILD_ROOT install
# ln -sf libtkx%{tclXvers}.so $RPM_BUILD_ROOT%{_prefix}/lib/libtkx.so
# ln -sf libtclx%{tclXvers}.so $RPM_BUILD_ROOT%{_prefix}/lib/libtclx.so
cd ../..
(find $RPM_BUILD_ROOT%{_prefix}/bin $RPM_BUILD_ROOT%{_prefix}/include \
	$RPM_BUILD_ROOT%{_prefix}/man -type f -o -type l;
 find $RPM_BUILD_ROOT%{_prefix}/lib/*) | cat - tcl.files tk.files \
	| sort | uniq -u > tclx.files

#------------------------------------------
# Expect
#
cd expect-%{expvers}
make prefix=$RPM_BUILD_ROOT%{_prefix} install
cd ..
(find $RPM_BUILD_ROOT%{_prefix}/bin $RPM_BUILD_ROOT%{_prefix}/include \
	$RPM_BUILD_ROOT%{_prefix}/man -type f -o -type l;
 find $RPM_BUILD_ROOT%{_prefix}/lib/*) | cat - tcl.files tk.files tclx.files \
	| sort | uniq -u > expect.files

# for files in expect.files, sed the #! at the top...
for n in `cat expect.files`; do
	if head -1 $n | grep '#!'; then
		cp -a $n $n.in
		chmod u+w $n
		sed "s|$RPM_BUILD_ROOT||" < $n.in > $n
		rm -f $n.in
	fi
done

#------------------------------------------
# Tix
#
cd Tix%{Tixvers}/unix
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_prefix}/lib make prefix=$RPM_BUILD_ROOT%{_prefix} install
cd ../..
mv $RPM_BUILD_ROOT%{_prefix}/man/mann/tixwish.1 $RPM_BUILD_ROOT%{_prefix}/man/man1/tixwish.1
# ln -sf libtix4.1.8.0.so $RPM_BUILD_ROOT%{_prefix}/lib/libtix.so
(find $RPM_BUILD_ROOT%{_prefix}/bin $RPM_BUILD_ROOT%{_prefix}/include \
	$RPM_BUILD_ROOT%{_prefix}/man -type f -o -type l;
 find $RPM_BUILD_ROOT%{_prefix}/lib/*) | cat - tcl.files tk.files tclx.files expect.files\
	| sort | uniq -u > tix.files

for n in `cat tix.files`; do
        if head -1 $n | grep '#!'; then
                cp -a $n $n.in
		chmod u+w $n
                sed "s|$RPM_BUILD_ROOT||" < $n.in > $n
		rm -f $n.in
        fi
done

#------------------------------------------
# itcl
#
cd itcl%{itclvers}
make INSTALL_ROOT=$RPM_BUILD_ROOT exec_prefix=%{_prefix} install
# ln -sf libitk3.0.so $RPM_BUILD_ROOT%{_prefix}/lib/libitk.so
# ln -sf libitcl3.0.so $RPM_BUILD_ROOT%{_prefix}/lib/libitcl.so
cd ..
(find $RPM_BUILD_ROOT%{_prefix}/bin $RPM_BUILD_ROOT%{_prefix}/include \
	$RPM_BUILD_ROOT%{_prefix}/man -type f -o -type l;
 find $RPM_BUILD_ROOT%{_prefix}/lib/*) | cat - tcl.files tk.files tclx.files expect.files tix.files \
	| sort | uniq -u > itcl.files

for n in `cat itcl.files`; do
        if head -1 $n | grep '#!'; then
                cp -a $n $n.in
		chmod u+w $n
                sed "s|$RPM_BUILD_ROOT||" < $n.in > $n
		rm -f $n.in
        fi
done

#------------------------------------------
# this is too annoying to watch
set +x
for n in *.files; do
	mv $n $n.in
	sed "s|.*%{_prefix}|%{_prefix}|" < $n.in | while read file; do
	    if [ -d $RPM_BUILD_ROOT/$file ]; then
		echo -n '%dir '
	    fi
	    echo $file
	done > $n
	rm -f $n.in
done
set -x

# strip the binaries
strip $RPM_BUILD_ROOT%{_prefix}/bin/* ||:
stack --fix=256k $RPM_BUILD_ROOT%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf $RPM_BUILD_ROOT%{_prefix}/man/*/*

# man pages are compressed
for file in *.files ; do 
    mv $file $file.in
    sed -e 's|%{_prefix}/man/man.*$|&\*|' < $file.in > $file
    rm -f $file.in
done

#==========================================
#%#post -p /sbin/ldconfig -n tcl
#%#post -p /sbin/ldconfig -n tk
#%#post -p /sbin/ldconfig -n expect
#%#post -p /sbin/ldconfig -n tclx
#%#post -p /sbin/ldconfig -n tix
#%#post -p /sbin/ldconfig -n itcl

#%#postun -p /sbin/ldconfig -n tcl
#%#postun -p /sbin/ldconfig -n tk
#%#postun -p /sbin/ldconfig -n expect
#%#postun -p /sbin/ldconfig -n tclx
#%#postun -p /sbin/ldconfig -n tix
#%#postun -p /sbin/ldconfig -n itcl

%clean
rm -rf $RPM_BUILD_ROOT
rm -f *.files*

%files -f tcl.files -n tcl
%files -f tk.files -n tk
%files -f tclx.files -n tclx
%files -f expect.files -n expect
%files -f tix.files -n tix
%files -f itcl.files -n itcl

%changelog
* Thu Nov 16 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
