Summary       : A PostScript(TM) interpreter and renderer.
Name          : ghostscript
Version       : 8.15
Release       : 1
License       : GNU
Group         : Applications/Graphics

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.ghostscript.com

Requires      : urw-fonts >= 1.1, ghostscript-fonts >= 6.0
Conflicts     : ghostscript-68000

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://mirror.cs.wisc.edu/pub/mirrors/ghost/GPL/gs815/ghostscript-%{version}.tar.gz
Source1: ftp://mirror.cs.wisc.edu/pub/mirrors/ghost/GPL/gs815/jpegsrc.v6b.tar.gz
Source2: ftp://mirror.cs.wisc.edu/pub/mirrors/ghost/GPL/gs815/libpng-1.2.6.tar.gz
Source3: ftp://mirror.cs.wisc.edu/pub/mirrors/ghost/GPL/gs815/zlib-1.2.1.tar.gz
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

==========================================================================
This packages was compiled with -m68020-060. This means you need at least
a machine with an 68020 CPU and an FPU to use the programs herein.
==========================================================================

Install the ghostscript-68000 package if you have an ST or an Falcon
without FPU.


%prep
#
# unpack main sources
%setup -q -n ghostscript-%{version}
#
# unpack jpeg
%setup -q -T -D -a 1 -n ghostscript-%{version}
# For gs 5.50 and later, rename jpeg subdirectory
mv $RPM_BUILD_DIR/ghostscript-%{version}/jpeg-6b  $RPM_BUILD_DIR/ghostscript-%{version}/jpeg
#
# unpack libpng
%setup -q -T -D -a 2 -n ghostscript-%{version}
# For gs 5.50 and later, rename libpng subdirectory
mv $RPM_BUILD_DIR/ghostscript-%{version}/libpng-1.2.6  $RPM_BUILD_DIR/ghostscript-%{version}/libpng
#
# unpack zlib
%setup -q -T -D -a 3 -n ghostscript-%{version}
# For gs 5.50 and later, rename zlib subdirectory
mv $RPM_BUILD_DIR/ghostscript-%{version}/zlib-1.2.1  $RPM_BUILD_DIR/ghostscript-%{version}/zlib
#
# copy the makefile, then patch the new copy
cp $RPM_BUILD_DIR/ghostscript-%{version}/src/unix-gcc.mak $RPM_BUILD_DIR/ghostscript-%{version}/Makefile
cp $RPM_BUILD_DIR/ghostscript-%{version}/Makefile $RPM_BUILD_DIR/ghostscript-%{version}/Makefile.backup

%patch0 -p1 -b .config


%build
make prefix=%{_prefix} \
	XCFLAGS="$RPM_OPT_FLAGS -m68020-60 -m68881 -DA4" \
	XLDFLAGS="$RPM_OPT_FLAGS -m68020-60 -m68881 -DA4"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/doc
make install prefix=${RPM_BUILD_ROOT}%{_prefix} \
	XCFLAGS="$RPM_OPT_FLAGS -m68020-60 -m68881 -DA4" \
	XLDFLAGS="$RPM_OPT_FLAGS -m68020-60 -m68881 -DA4"

#mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share
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


%post
cat <<EOF
==========================================================================
This packages was compiled with -m68020-060. This means you need at least
a machine with an 68020 CPU and an FPU to use the programs herein.
==========================================================================
EOF


%files
%defattr(-,root,root)
%{_prefix}/doc/ghostscript-%{PACKAGE_VERSION}
%{_prefix}/bin/*
%dir %{_prefix}/share/ghostscript/%{PACKAGE_VERSION}
%{_prefix}/share/ghostscript/%{PACKAGE_VERSION}/lib
%{_prefix}/share/ghostscript/%{PACKAGE_VERSION}/examples
%{_prefix}/share/man/*/*


%changelog
* Sun Nov 07 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- updated to GNU Ghostscript 8.15
- new URL in specfile header
* Tue Sep 30 2003 Markus Lutz <markus@gmlutz.de>
- updated to version 8.11
* Sun Oct 28 2001 Markus Lutz <markus_lutz@t-online.de>
- updated to version 7.03
* Sun Dec 31 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint