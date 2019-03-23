Summary       : A PostScript(TM) interpreter and renderer.
Name          : ghostscript-68000
Version       : 6.50
Release       : 2
License       : Aladdin Free Public License, Aladdin Enterprises
Group         : Applications/Graphics

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://gnu-gs.sourceforge.net/

Requires      : urw-fonts >= 1.1, ghostscript-fonts >= 6.0
Conflicts     : ghostscript

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.cs.wisc.edu/ghost/aladdin/gs601/ghostscript-%{version}.tar.gz
Source1: ftp://ftp.cs.wisc.edu/ghost/aladdin/gs601/ghostscript-%{version}jpeg.tar.gz
Source2: ftp://ftp.cs.wisc.edu/ghost/aladdin/gs601/ghostscript-%{version}libpng.tar.gz
Source3: ftp://ftp.cs.wisc.edu/ghost/aladdin/gs601/ghostscript-%{version}zlib.tar.gz
Patch0:  ghostscript-%{version}-config.patch


%description
Ghostscript is a set of software that provides a PostScript(TM)
interpreter, a set of C procedures (the Ghostscript library, which
implements the graphics capabilities in the PostScript language) and
an interpreter for Portable Document Format (PDF) files.  Ghostscript
translates PostScript code into many common, bitmapped formats, like
those understood by your printer or screen.  Ghostscript is normally
used to display PostScript files and to print PostScript files to
non-PostScript printers.

If you need to display PostScript files or print them to
non-PostScript printers, you should install ghostscript.  If you
install ghostscript, you also need to install the ghostscript-fonts
package.


%prep
#
# unpack main sources
%setup -q -n gs%{version}
#
# unpack jpeg
%setup -q -T -D -a 1 -n gs%{version}
# For gs 5.50 and later, rename jpeg subdirectory
mv $RPM_BUILD_DIR/gs%{version}/jpeg-6b  $RPM_BUILD_DIR/gs%{version}/jpeg
#
# unpack libpng
%setup -q -T -D -a 2 -n gs%{version}
# For gs 5.50 and later, rename libpng subdirectory
mv $RPM_BUILD_DIR/gs%{version}/libpng-1.0.8  $RPM_BUILD_DIR/gs%{version}/libpng
#
# unpack zlib
%setup -q -T -D -a 3 -n gs%{version}
# For gs 5.50 and later, rename zlib subdirectory
mv $RPM_BUILD_DIR/gs%{version}/zlib-1.1.3  $RPM_BUILD_DIR/gs%{version}/zlib
#
# copy the makefile, then patch the new copy
cp $RPM_BUILD_DIR/gs%{version}/src/unix-gcc.mak $RPM_BUILD_DIR/gs%{version}/Makefile
cp $RPM_BUILD_DIR/gs%{version}/Makefile $RPM_BUILD_DIR/gs%{version}/Makefile.backup

%patch0 -p1 -b .config


%build
make prefix=%{_prefix} \
	XCFLAGS="$RPM_OPT_FLAGS -m68000" \
	XLDFLAGS="$RPM_OPT_FLAGS -m68000"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/{bin,man,doc}
make install prefix=${RPM_BUILD_ROOT}%{_prefix} \
	XCFLAGS="$RPM_OPT_FLAGS -m68000" \
	XLDFLAGS="$RPM_OPT_FLAGS -m68000"

mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share
chmod 644 ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:
ln -sf gs.1.gz ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/ghostscript.1.gz
( cd ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1;
  for file in *.1; do \
    echo "processing $file ..."; \
    target=`readlink $file`; \
    ln -s $target.gz $file.gz; \
    rm $file; \
  done
)

ln -sf gs ${RPM_BUILD_ROOT}%{_prefix}/bin/ghostscript
strip -R .comment ${RPM_BUILD_ROOT}%{_prefix}/bin/gs
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/bin/gs


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_prefix}/doc/ghostscript-%{PACKAGE_VERSION}
%{_prefix}/bin/*
%dir %{_prefix}/share/ghostscript/%{PACKAGE_VERSION}
%{_prefix}/share/ghostscript/%{PACKAGE_VERSION}/lib
%{_prefix}/share/ghostscript/%{PACKAGE_VERSION}/examples
%{_prefix}/share/man/*/*


%changelog
* Sun Dec 31 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
