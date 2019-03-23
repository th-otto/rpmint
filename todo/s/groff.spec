Summary: A document formatting system.
Name: groff
Version: 1.15
Release: 3
Copyright: GPL
Group: Applications/Publishing
Source0: ftp://prep.ai.mit.edu/pub/gnu/groff-1.15.tar.gz
Source1: troff-to-ps.fpi
Patch0:  groff-1.15-make.patch
Patch1: groff-1.11-safer.patch
Requires: mktemp
Buildroot: /var/tmp/groff-root
Obsoletes: groff-tools
Packager: Frank Naumann <fnaumann@freemint.de>
Vendor: Sparemint

%description
Groff is a document formatting system.  Groff takes standard text and
formatting commands as input and produces formatted output.  The
created documents can be shown on a display or printed on a printer. 
Groff's formatting commands allow you to specify font type and size, bold
type, italic type, the number and size of columns on a page, and more.

You should install groff if you want to use it as a document formatting
system.  Groff can also be used to format man pages. If you are going
to use groff with the X Window System, you'll also need to install the
groff-gxditview package.

%package perl
Summary: Parts of the groff formatting system that require Perl.
Group: Applications/Publishing

%description perl
groff-perl contains the parts of the groff text processor
package that require Perl. These include the afmtodit
font processor used to create PostScript font files, the
grog utility that can be used to automatically determine
groff command-line options, and the troff-to-ps print filter.


%prep
%setup -q
%patch0 -p1 -b .make
%patch1 -p1 -b .safer

%build
CC='gcc' CXX='g++' \
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
LDFLAGS=-s \
./configure \
	--prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
make install prefix=$RPM_BUILD_ROOT/usr

strip $RPM_BUILD_ROOT/usr/bin/* || :
stack --fix=96k $RPM_BUILD_ROOT/usr/bin/* || :
stack --fix=384k $RPM_BUILD_ROOT/usr/bin/grops || :
gzip -9nf $RPM_BUILD_ROOT/usr/man/*/*

ln -s tmac.s		$RPM_BUILD_ROOT/usr/lib/groff/tmac/tmac.gs
ln -s tmac.mse		$RPM_BUILD_ROOT/usr/lib/groff/tmac/tmac.gmse
ln -s tmac.m		$RPM_BUILD_ROOT/usr/lib/groff/tmac/tmac.gm
ln -s troff		$RPM_BUILD_ROOT/usr/bin/gtroff
ln -s tbl		$RPM_BUILD_ROOT/usr/bin/gtbl
ln -s pic		$RPM_BUILD_ROOT/usr/bin/gpic
ln -s eqn		$RPM_BUILD_ROOT/usr/bin/geqn
ln -s neqn		$RPM_BUILD_ROOT/usr/bin/gneqn
ln -s refer		$RPM_BUILD_ROOT/usr/bin/grefer
ln -s lookbib		$RPM_BUILD_ROOT/usr/bin/glookbib
ln -s indxbib		$RPM_BUILD_ROOT/usr/bin/gindxbib
ln -s soelim		$RPM_BUILD_ROOT/usr/bin/gsoelim
ln -s nroff		$RPM_BUILD_ROOT/usr/bin/gnroff
ln -s eqn.1.gz		$RPM_BUILD_ROOT/usr/man/man1/geqn.1.gz
ln -s indxbib.1.gz	$RPM_BUILD_ROOT/usr/man/man1/gindxbib.1.gz
ln -s lookbib.1.gz	$RPM_BUILD_ROOT/usr/man/man1/glookbib.1.gz
ln -s nroff.1.gz	$RPM_BUILD_ROOT/usr/man/man1/gnroff.1.gz
ln -s pic.1.gz		$RPM_BUILD_ROOT/usr/man/man1/gpic.1.gz
ln -s refer.1.gz	$RPM_BUILD_ROOT/usr/man/man1/grefer.1.gz
ln -s soelim.1.gz	$RPM_BUILD_ROOT/usr/man/man1/gsoelim.1.gz
ln -s tbl.1.gz		$RPM_BUILD_ROOT/usr/man/man1/gtbl.1.gz
ln -s troff.1.gz	$RPM_BUILD_ROOT/usr/man/man1/gtroff.1.gz
mkdir -p $RPM_BUILD_ROOT/usr/lib/rhs/rhs-printfilters
install -m755 $RPM_SOURCE_DIR/troff-to-ps.fpi \
	$RPM_BUILD_ROOT/usr/lib/rhs/rhs-printfilters

find $RPM_BUILD_ROOT/usr/bin $RPM_BUILD_ROOT/usr/man -type f -o -type l \
	| grep -v afmtodit \
	| grep -v grog \
	| grep -v mdoc.samples \
	| sed "s|$RPM_BUILD_ROOT||g" \
	| sed "s|\.[0-9]|\.*|g" > groff-files

%files -f groff-files
%defattr(-,root,root)
/usr/lib/groff

%files perl
%defattr(-,root,root)
/usr/bin/grog
/usr/bin/afmtodit
/usr/man/man1/afmtodit.*
/usr/man/man1/grog.*
/usr/lib/rhs/*/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon May 10 2000 Frank Naumann <fnaumann@freemint.de>
- recompiled against new MiNTLib
- increased stack sizes

* Mon Jan 31 2000 Frank Naumann <fnaumann@freemint.de>
- first SpareMiNT release
