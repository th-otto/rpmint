Summary: The TeX text formatting system.
Name: tetex
Version: 1.0.6
Release: 1
Copyright: distributable
Group: Applications/Publishing
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Requires: tmpwatch, dialog, ed
Prereq: /sbin/install-info
Source0: ftp://ftp.duke.edu/tex-archive/systems/unix/teTeX-beta/teTeX-src-%{PACKAGE_VERSION}.tar.gz
Source1: ftp://ftp.duke.edu/tex-archive/systems/unix/teTeX-beta/teTeX-texmf-%{PACKAGE_VERSION}.tar.gz
Source2: dvi-to-ps.fpi
Source3: ftp://ftp.duke.edu/tex-archive/systems/unix/teTeX-beta/teTeX-texmfsrc-%{PACKAGE_VERSION}.tar.gz
Source10: tetex.cron
Source11: texmf.cnf

Patch0: teTeX-1.0-varconfig.patch  
Patch2: teTeX-1.0-italian.patch
Patch3: teTeX-0.9-arm.patch
Patch4: teTeX-1.0-texmfcnf.patch
Patch5: teTeX-1.0-fmtutil.patch
Patch6: teTeX-texmf-pdftex.diff
Patch7: teTeX-texmf-dvipsgeneric.diff

Patch8: teTeX-1.0-mint.patch
Patch9: teTeX-1.0-mint-cnf.patch
Patch10: teTeX-1.0-mint-selfautofix.patch

Url: http://www.tug.org/teTeX/
BuildRoot: /var/tmp/tetex-root
Requires: tetex-fonts = %{version}
Obsoletes: tetex-texmf-src

%description
TeTeX is an implementation of TeX for Linux or UNIX systems. TeX takes
a text file and a set of formatting commands as input and creates a
typesetter independent .dvi (DeVice Independent) file as output.
Usually, TeX is used in conjunction with a higher level formatting
package like LaTeX or PlainTeX, since TeX by itself is not very
user-friendly.

Install tetex if you want to use the TeX text formatting system.  If
you are installing tetex, you will also need to install tetex-afm (a
PostScript(TM) font converter for TeX), tetex-dvilj (for converting
.dvi files to HP PCL format for printing on HP and HP compatible
printers), tetex-dvips (for converting .dvi files to PostScript format
for printing on PostScript printers), tetex-latex (a higher level
formatting package which provides an easier-to-use interface for TeX)
and tetex-xdvi (for previewing .dvi files in X).  Unless you're an
expert at using TeX, you'll also want to install the tetex-doc
package, which includes the documentation for TeX.

%package latex
Summary: The LaTeX front end for the TeX text formatting system.
Group: Applications/Publishing
Requires: tetex = %{PACKAGE_VERSION}

%description latex
LaTeX is a front end for the TeX text formatting system.  Easier to
use than TeX, LaTeX is essentially a set of TeX macros which provide
convenient, predefined document formats for users.

If you are installing tetex, so that you can use the TeX text
formatting system, you will also need to install tetex-latex.  In
addition, you will need to install tetex-afm (for converting
PostScript font description files), tetex-dvilj (for converting .dvi
files to HP PCL format for printing on HP and HP compatible printers),
tetex-dvips (for converting .dvi files to PostScript format for
printing on PostScript printers) and tetex-xdvi (for previewing .dvi
files in X).  If you're not an expert at TeX, you'll probably also
want to install the tetex-doc package, which contains documentation
for TeX.

%package dvips
Summary: A DVI to PostScript converter for the TeX text formatting system.
Group: Applications/Publishing
Requires: tetex = %{PACKAGE_VERSION}

%description dvips
Dvips converts .dvi files produced by the TeX text formatting system
(or by another processor like GFtoDVI) to PostScript(TM) format.
Normally the PostScript file is sent directly to your printer.

If you are installing tetex, so that you can use the TeX text
formatting system, you will also need to install tetex-dvips.  In
addition, you will need to install tetex-afm (for converting
PostScript font description files), tetex-dvilj (for converting .dvi
files to HP PCL format for printing on HP and HP compatible printers),
tetex-latex (a higher level formatting package which provides an
easier-to-use interface for TeX) and tetex-xdvi (for previewing .dvi
files in X).  If you're installing TeX and you're not an expert at it,
you'll also want to install the tetex-doc package, which contains
documentation for the TeX system.

%package dvilj
Summary: A DVI to HP PCL (Printer Control Language) converter.
Group: Applications/Publishing
Requires: tetex = %{PACKAGE_VERSION}

%description dvilj
Dvilj and dvilj's siblings (included in this package) will convert TeX
text formatting system output .dvi files to HP PCL (HP Printer Control
Language) commands.  Using dvilj, you can print TeX files to HP
LaserJet+ and fully compatible printers.  With dvilj2p, you can print
to HP LaserJet IIP and fully compatible printers. And with dvilj4, you
can print to HP LaserJet4 and fully compatible printers.

If you are installing tetex, so that you can use the TeX text
formatting system, you will also need to install tetex-dvilj.  In
addition, you will need to install tetex-afm (for converting
PostScript font description files), tetex-dvips (for converting .dvi
files to PostScript format for printing on PostScript printers),
tetex-latex (a higher level formatting package which provides an
easier-to-use interface for TeX) and tetex-xdvi (for previewing .dvi
files in X).  If you're installing TeX and you're not a TeX expert,
you'll also want to install the tetex-doc package, which contains
documentation for TeX.

%package afm
Summary: A converter for PostScript(TM) font metric files, for use with TeX.
Group: Applications/Publishing
Requires: tetex = %{PACKAGE_VERSION}

%description afm
Tetex-afm provides afm2tfm, a converter for PostScript font metric
files.  PostScript fonts are accompanied by .afm font metric files
which describe the characteristics of each font.  To use PostScript
fonts with TeX, TeX needs .tfm files that contain similar information.
Afm2tfm will convert .afm files to .tfm files.

If you are installing tetex in order to use the TeX text formatting
system, you will need to install tetex-afm.  You will also need to
install tetex-dvilj (for converting .dvi files to HP PCL format for
printing on HP and HP compatible printers), tetex-dvips (for
converting .dvi files to PostScript format for printing on PostScript
printers), tetex-latex (a higher level formatting package which
provides an easier-to-use interface for TeX) and tetex-xdvi (for
previewing .dvi files in X).  Unless you're an expert at using TeX,
you'll probably also want to install the tetex-doc package, which
includes documentation for TeX.

%package fonts
Summary: The font files for the TeX text formatting system.
Group: Applications/Publishing

%description fonts
The tetex-fonts package contains fonts used by both the Xdvi previewer and
the TeX text formatting system.

You will need to install tetex-fonts if you wish to use either tetex-xdvi
(for previewing .dvi files in X) or the tetex package (the core of the TeX
text formatting system).

%package doc
Summary: The documentation files for the TeX text formatting system.
Group: Applications/Publishing

%description doc
The tetex-doc package contains documentation for the TeX text
formatting system.

If you want to use TeX and you're not an expert at it, you should
install the tetex-doc package.  You'll also need to install the tetex
package, tetex-afm (a PostScript font converter for TeX), tetex-dvilj
(for converting .dvi files to HP PCL format for printing on HP and HP
compatible printers), tetex-dvips (for converting .dvi files to
PostScript format for printing on PostScript printers), tetex-latex (a
higher level formatting package which provides an easier-to-use
interface for TeX) and tetex-xdvi (for previewing .dvi files).

%prep
%setup -q -n teTeX-1.0
%patch0 -p1 -b .rhconfig
%patch3 -p1 -b .arm
%patch5 -p1 -b .fmtutil
%patch8 -p1 -b .mint
%patch10 -p1 -b .mint-selfautofix

mkdir texmf
tar xzf %{SOURCE1} -C texmf
%patch2 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1

%build
sh ./reautoconf

CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr \
	--with-system-ncurses --with-system-zlib --with-system-pnglib \
	--disable-multiplatform --without-dialog --without-texinfo \
	--datadir=/usr/share \
	--without-dviljk \
	--without-oxdvik \
	--without-xdvik \
	--without-x
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/texmf
mkdir -p $RPM_BUILD_ROOT/var/lib/texmf

tar cf - texmf | tar xf - -C $RPM_BUILD_ROOT/usr/share
rm $RPM_BUILD_ROOT/usr/share/texmf/web2c/texmf.cnf

make install prefix=$RPM_BUILD_ROOT/usr \
	texmf=$RPM_BUILD_ROOT/usr/share/texmf \
	texmfmain=$RPM_BUILD_ROOT/usr/share/texmf

rm -f $RPM_BUILD_ROOT/usr/info/dir
gzip -9nf $RPM_BUILD_ROOT/usr/info/*info*
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/* ||:
( cd $RPM_BUILD_ROOT/usr/man/man1;
  for file in *.1; do \
    echo "processing $file ..."; \
    target=`$RPM_BUILD_ROOT/usr/bin/readlink $file`; \
    ln -s $target.gz $file.gz; \
    rm $file; \
  done
)
chmod 644 $RPM_BUILD_ROOT/usr/man/man1/* ||:

# install the new magic print filter for converting dvi to ps
mkdir -p $RPM_BUILD_ROOT/usr/lib/rhs/rhs-printfilters
install -m755 $RPM_SOURCE_DIR/dvi-to-ps.fpi $RPM_BUILD_ROOT/usr/lib/rhs/rhs-printfilters

mkdir -p $RPM_BUILD_ROOT/etc/cron.daily
install -m755 $RPM_SOURCE_DIR/tetex.cron $RPM_BUILD_ROOT/etc/cron.daily

# Strip binaries
strip $RPM_BUILD_ROOT/usr/bin/* || :

# fix stacksize, default all to 128k
stack --fix=128k $RPM_BUILD_ROOT/usr/bin/* || :

### Files list
find $RPM_BUILD_ROOT -type f -or -type l | \
	sed -e "s|$RPM_BUILD_ROOT||g" | \
	grep -v "^/etc" | grep -v ".orig$" | \
	sed -e "s|.*\.cnf$|%config &|" \
	    -e "s|/usr/share/texmf/dvips/config/config.ps|%config &|" \
						> filelist.full

# subpackages
grep -v "/doc/" filelist.full | grep latex | \
	grep -v dvilj				> filelist.latex

grep -v "/doc/" filelist.full | grep dvips | \
	grep -v "/usr/share/texmf/tex"		> filelist.dvips
echo "/usr/bin/dvired"				>> filelist.dvips
echo "/usr/bin/dvi2fax"				>> filelist.dvips
echo "/usr/lib/rhs/rhs-printfilters/dvi-to-ps.fpi"
						>> filelist.dvips

grep -v "/doc/" filelist.full | grep dvilj	> filelist.dvilj

grep -v "/doc/" filelist.full | grep -v afm | \
	grep "/usr/share/texmf/fonts" | \
	grep -v "/usr/share/texmf/fonts/source" > filelist.fonts

grep -v "/doc/" filelist.full | grep afm 	> filelist.afm

grep "/doc/" filelist.full 			> filelist.doc

# now files listed only once are in the main  package
cat filelist.full filelist.latex filelist.dvips \
   filelist.dvilj filelist.afm filelist.fonts filelist.doc | \
   sort | uniq -u > filelist.main 

%clean
rm -rf $RPM_BUILD_ROOT
rm -f filelist.*

# make sure ls-R used by teTeX is updated after an install

%post
/sbin/install-info /usr/info/web2c.info.gz /usr/info/dir
/sbin/install-info /usr/info/kpathsea.info.gz /usr/info/dir
/usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post latex
/sbin/install-info /usr/info/latex.info.gz /usr/info/dir
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post dvips
/sbin/install-info /usr/info/dvips.info.gz /usr/info/dir
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post dvilj
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post fonts
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post afm
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun latex
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun dvips
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun dvilj
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun fonts
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun afm
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%preun
if [ "$1" = 0 ]; then
	/sbin/install-info --delete /usr/info/kpathsea.info.gz /usr/info/dir
	/sbin/install-info --delete /usr/info/web2c.info.gz /usr/info/dir
fi

%preun dvips
if [ "$1" = 0 ]; then
	/sbin/install-info --delete /usr/info/dvips.info.gz /usr/info/dir
fi

%preun latex
if [ "$1" = 0 ]; then
	/sbin/install-info --delete /usr/info/latex.info.gz /usr/info/dir
fi

%files -f filelist.main
%defattr(-,root,root)
%attr(1777,root,root) %dir /var/lib/texmf
%config /etc/cron.daily/tetex.cron

%files -f filelist.latex latex
%defattr(-,root,root)

%files -f filelist.dvips dvips
%defattr(-,root,root)

%files -f filelist.dvilj dvilj
%defattr(-,root,root)

%files -f filelist.fonts fonts
%defattr(-,root,root)

%files -f filelist.afm afm
%defattr(-,root,root)

%files -f filelist.doc doc
%defattr(-,root,root)

%changelog
* Sun Nov 28 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- updated to 1.0.6
- adpated all Redhat changes

* Wed Sep 13 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- first release
