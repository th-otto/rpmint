%define pkgname XFree86

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary       : The basic fonts, programs and docs for an X workstation.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 4.0
Release       : 1
License       : MIT
Group         : System/X11

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : ftp://ftp.xfree86.org/%{version}/source/

%rpmint_essential
BuildRequires : groff
%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-gdbm-devel >= 1.8.0
BuildRequires : cross-mint-zlib-devel
BuildRequires : cross-mint-ncurses-devel
BuildRequires : gdbm-devel-32bit
BuildRequires : ncurses-devel-32bit
BuildRequires : zlib-devel-32bit
%else
BuildRequires : gdbm >= 1.8.0
BuildRequires : zlib-devel
BuildRequires : ncurses-devel
%endif

Prefix        : %{_prefix}
Docdir        : %{_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

%define baseversion 400

#
# Patches are already applied in the source archive.
# For a history, look at https://github.com/th-otto/xfree86
#
# Source0: ftp://ftp.xfree86.org/%%{version}/source/X%%{baseversion}src-1.tgz
# Source1: ftp://ftp.xfree86.org/%%{version}/source/X%%{baseversion}src-2.tgz
# Source2: ftp://ftp.xfree86.org/%%{version}/source/X%%{baseversion}src-3.tgz
Source0: %{pkgname}-%{version}.tar.xz
Source3: xfree86-euro.xmod
Source4: xfree86-eurofonts-X11.tar.gz
Source5: xfree86-xfs.config
Source6: xfree86-xfs.init

%rpmint_build_arch


%package tools
Summary       : Various tools for XFree86
Group         : System/X11
Requires      : %{name}

%package xfs
Summary       : A font server for the X Window System.
Group         : System Environment/Daemons
%if "%{buildtype}" != "cross"
Prereq        : /sbin/chkconfig fileutils sed
%endif
#Requires      : initscripts >= 5.20

%package twm
Summary       : A simple window manager
Group         : System/X11
Requires      : %{name}
Provides      : windowmanager

%package devel
Summary       : X11R6 static libraries, headers and programming man pages.
Group         : Development/Libraries
Requires      : %{name} = %{version}
%if "%{buildtype}" == "cross"
Provides      : cross-mint-libX11-devel
%else
Provides      : libX11-devel
%endif

%package doc
Summary       : Documentation on various X11 programming interfaces.
Group         : Documentation

%package xdm
Summary       : X Display Manager
Requires      : %{name} = %{version}
Group         : System/X11

%package 100dpi-fonts
Summary       : X Window System 100dpi fonts.
Group         : System/X11
%if "%{buildtype}" != "cross"
Prereq        : chkfontpath
%endif

%package 75dpi-fonts
Summary       : A set of 75 dpi resolution fonts for the X Window System.
Group         : System/X11
%if "%{buildtype}" != "cross"
Prereq        : chkfontpath
%endif

%package cyrillic-fonts
Summary       : Cyrillic fonts for X.
Group         : System/X11
%if "%{buildtype}" != "cross"
Prereq        : chkfontpath
%endif

#%package ISO8859-2-100dpi-fonts
#Summary       : ISO 8859-2 fonts in 100 dpi resolution for the X Window System.
#Group         : System/X11
%if "%{buildtype}" != "cross"
#Prereq        : chkfontpath
%endif
#
#%package ISO8859-2-75dpi-fonts
#Summary       : A set of 75 dpi Central European language fonts for X.
#Group         : System/X11
%if "%{buildtype}" != "cross"
#Prereq        : chkfontpath
%endif
#
#%package Xnest
#Summary       : A nested XFree86 server.
#Group         : System/X11 Hardware Support
#Requires      : %%{name} = %%{version}



%description
The X Window System provides the base technology for developing
graphical user interfaces. Simply stated, X draws the elements
of the GUI on the user's screen and builds methods for sending
user interactions back to the application. X also supports remote
application deployment--running an application on another computer
while viewing the input/output on your machine.  X is a powerful
environment which supports many different applications, such as
games, programming tools, graphics programs, text editors, etc.
XFree86 is the version of X which runs on Linux, as well as on other
platforms.

This package contains the basic fonts, programs and documentation
for an X workstation.  However, this package doesn't provide the
program which you will need to drive your video hardware.  To
control your video card, you'll need the particular X server
package which corresponds to your computer's video card.

If you are going to develop applications that run as X clients you
will need to install XFree86-devel.

%description tools
Various tools for X, including listres, xbiff, xedit, xeyes, xcalc, xload
and xman, among others.

If you're using X, you should install XFree86-tools.  You will also
need to install the XFree86 package, the XFree86 package which
corresponds to your video card, one of the XFree86 fonts packages, the
Xconfigurator package and the XFree86-libs package.

Finally, if you are going to develop applications that run as X clients,
you will also need to install XFree86-devel.

This package contains all applications that used to be in X11R6-contrib
in older releases.

%description xfs
XFree86-xfs contains the font server for XFree86.  Xfs can also serve
fonts to remote X servers. The remote system will be able to use all
fonts installed on the font server, even if they are not installed on
the remote computer.

You'll need to install XFree86-xfs if you're installing the X Window
System. You'll also need to install the following packages: XFree86,
the XFree86 X server for your video card, the XFree86 fonts package(s)
appropriate for your system, Xconfigurator and XFree86-libs.

%description twm
A simple and lightweight window manager

%description devel
XFree86-devel includes the libraries, header files and documentation
you'll need to develop programs which run as X clients. XFree86-devel
includes the base Xlib library as well as the Xt and Xaw widget sets.

Install XFree86-devel if you are going to develop programs which
will run as X clients.

%description doc
XFree86-doc provides a great deal of documentation, in PostScript
format, on the various X APIs, libraries, and other interfaces.  If
you need low level X documentation, you will find it here.  Topics
include the X protocol, the ICCCM window manager standard, ICE
session management, the font server API, etc.

%description xdm
X Display Manager.

%description 100dpi-fonts
The XFree86-100dpi-fonts package contains a set of 100 dpi fonts used
on most Linux systems. If you're going to use the X Window System and
you have a high resolution monitor capable of 100 dpi, you should
install XFree86-100dpi-fonts.

If you are installing the X Window System, you will also need to
install the following packages: XFree86, the XFree86 server package
for your video card, Xconfigurator, XFree86-xfs and
XFree86-libs. You may also need to install other XFree86 fonts
packages. If you are going to develop applications that run as X
clients, you will also need to install the XFree86-devel package.

%description 75dpi-fonts
XFree86-75dpi-fonts contains the 75 dpi fonts used on most X Window
Systems. If you're going to use the X Window System, you should
install this package, unless you have a monitor which can support 100
dpi resolution.  In that case, you may prefer the 100dpi fonts
available in the XFree86-100dpi-fonts package.

To install the X Window System, you will also need to install the
following packages: XFree86, the XFree86 server for your video card,
Xconfigurator, XFree86-xfs and XFree86-libs. Finally,
if you are going to develop applications that run as X clients, you
will also need to install the XFree86-devel package.

%description cyrillic-fonts
The XFree86-cyrillic-fonts package includes the Cyrillic fonts
included with XFree86 3.3.2 and higher. If you use a language that
requires the Cyrillic character set, you should install
XFree86-cyrillic-fonts.

If you are installing the X Window System, you will also need to
install the following packages: XFree86, the XFree86 package
corresponding to your video card, Xconfigurator,
XFree86-xfs and XFree86-libs. You may also need to install other
XFree86 fonts packages. If you are going to develop applications that
run as X clients, you will also need to install the XFree86-devel
package.

#%description ISO8859-2-100dpi-fonts
#The XFree86-ISO8859-2-100dpi-fonts package includes Central European
#(ISO 8859-2) fonts, in 100 dpi resolution, for the X Window System.
#
#If you need to display the special characters used by Central European
#languages on your X Window System, and your monitor can support 100 dpi
#resolution, you should install the XFree86-ISO8859-2-100dpi-fonts
#package.  You may need to install one or more of the other XFree86
#fonts packages, as well.  To install the X Window System, you will need
#to install the XFree86 package, the XFree86 video card package which
#corresponds to your video card, the Xconfigurator package and the
#XFree86-libs package.
#If you're going to develop applications which run as X clients, you'll
#also need to install XFree86-devel.
#
#%description ISO8859-2-75dpi-fonts
#The XFree86-ISO8859-2-75dpi-fonts package contains a set of Central
#European language fonts in 75 dpi resolution for the X Window System.
#If you have a high resolution monitor capable of supporting 100 dpi,
#you should install the 100 dpi version of this package instead.
#
#If you are installing the X Window System and you need to display
#Central European language characters in 75 dpi resolution, you should
#install this package.  You may also need to install one or more of the
#other XFree86 fonts packages as well.  To install the X Window System,
#you will need to install the XFree86 package, the XFree86 video card
#package that corresponds to your video card, the Xconfigurator package and the
#XFree86-libs package.
#If you are going to develop applications that will run as X clients, you
#will also need to install XFree86-devel.
#
#%description Xnest
#Xnest is an X Window System server which runs in an X window.
#Xnest is actually a client of the real X server, which manages
#windows and graphics requests for Xnest, while Xnest manages the
#windows and graphics requests for its own clients.
#
#You will need to install Xnest if you require an X server which
#will run as a client of your real X server (perhaps for testing
#purposes).


%prep
%setup -q -n %{pkgname}-%{version}

# isn't installed otherwise???
touch xc/programs/xterm/XTerm-col.ad

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%define _isysconfdir /etc

cd xc
build_dir=`pwd`

# needed when compiling libX11, otherwise some include file are not found
ln -s include X11

# build the tools for the host
rm -f config/cf/host.def
cp ../cross.def config/cf/host.def
make World 

# copy the tools we need
mkdir -p host-tools
cp programs/mkfontdir/mkfontdir host-tools
cp programs/bdftopcf/bdftopcf host-tools
cp programs/xkbcomp/xkbcomp host-tools
cp config/util/makestrs host-tools
cp config/pswrap/pswrap host-tools
cp config/util/lndir host-tools
cp config/imake/imake host-tools
if test -f programs/rgb/rgb; then cp programs/rgb/rgb host-tools; fi

# cleanup from build. "make clean" does not work very well when switching configurations
find . -name "*.o" | xargs rm

# now build for target

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	rm -f config/cf/host.def
	cp ../host.def config/cf/host.def

	echo "CPUOPTION = -DCpuOption=${CPU_CFLAGS}" > cpuoption.mk
	make World BOOTSTRAPCFLAGS="-D__MINT__"
	
	# Now recompile some tools that were build for the host
	echo Recompile target tools
	rm -f config/cf/host.def
	echo "" > config/cf/host.def
	# lndir
	cd config/util
	%{_rpmint_target}-gcc -O2 -fomit-frame-pointer -I../../exports/include/ -o lndir lndir.c
	# imake
	cd ../imake
	%{_rpmint_target}-gcc -O2 -fomit-frame-pointer -I../.. -I../../exports/include -I../../include -I../../exports/include/X11 -D__MINT__ -o imake imake.c
	# pswrap was already compiled for target
	# makestrs was already compiled for target
	# revpath was already compiled for target
	# mkfontdir was already compiled for target
	# xkbcomp was already compiled for target
	# makeg is a script and does not need any changes
	# makedepend
	cd ../makedepend
	../../host-tools/imake -I../../config/cf  -DTOPDIR=../.. -DCURDIR=config/makedepend -D__MINT__
	make clean
	make
	cd ../..
	
	# do not install our temporary host.def
	rm -f config/cf/host.def
	echo "" > config/cf/host.def

	make DESTDIR=%{buildroot}%{_isysroot} install install.man

	#
	# install symlinks in <prefix>/lib
	#
	mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib${multilibdir}
	cd %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib
          if test "${multilibdir}" != ""; then
              subdir="${multilibdir#/}"
              mkdir "$subdir"
              mv *.a "$subdir"
              cd "$subdir"
              subdir=../
          else
              subdir=
          fi
	  for i in *.a; do
	    ln -s ../${subdir}X11R6/lib${multilibdir}/$i ../../${subdir}lib${multilibdir}/$i;
	  done
	cd "$build_dir"
	
	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/*
		rm -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/xkb/xkbcomp
	fi
	%endif

	# cleanup from build. "make clean" does not work very well when switching configurations
	find . -name "*.o" | xargs rm
done
	
echo PACKAGING DOCUMENTATION
# rezip these - they are in the old compress format
find doc/hardcopy -name \*.PS.Z | xargs gzip -df
find doc/hardcopy -name \*.PS | xargs gzip

# Generate docs
groff -Tascii -ms doc/misc/RELNOTES.ms             > doc/hardcopy/RELNOTES.txt
# rm doc/hardcopy/BDF/*
groff -Tascii -ms doc/specs/BDF/bdf.ms             > doc/hardcopy/BDF/bdf.txt
# rm doc/hardcopy/CTEXT/*
groff -Tascii -ms doc/specs/CTEXT/ctext.tbl.ms     > doc/hardcopy/CTEXT/ctext.tbl.txt
# rm doc/hardcopy/FSProtocol/*
groff -Tascii -ms doc/specs/FSProtocol/protocol.ms > doc/hardcopy/FSProtocol/protocol.txt
# rm doc/hardcopy/ICCCM/*
groff -Tascii -ms doc/specs/ICCCM/icccm.ms         > doc/hardcopy/ICCCM/icccm.txt
# rm doc/hardcopy/ICE/*
groff -Tascii -ms doc/specs/ICE/ICElib.ms          > doc/hardcopy/ICE/ICElib.txt
groff -Tascii -ms doc/specs/ICE/ice.ms             > doc/hardcopy/ICE/ice.txt
cp doc/specs/PM/PM_spec doc/hardcopy/ICE/PM_spec.txt
# rm doc/hardcopy/SM/*
groff -Tascii -ms doc/specs/SM/SMlib.ms            > doc/hardcopy/SM/SMlib.txt
# rm doc/hardcopy/XDMCP/*
groff -Tascii -ms doc/specs/XDMCP/xdmcp.ms         > doc/hardcopy/XDMCP/xdmcp.txt
# rm doc/hardcopy/XIM/*
groff -Tascii -ms doc/specs/XIM/xim.ms             > doc/hardcopy/XIM/xim.txt
# rm doc/hardcopy/XLFD/*
groff -Tascii -ms doc/specs/XLFD/xlfd.tbl.ms       > doc/hardcopy/XLFD/xlfd.tbl.txt


%install

%rpmint_cflags

cd xc
build_dir=`pwd`

# we don't want the libz.a from XFree86 -- it's broken
rm -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/libz.a

# explicitly create X authdir
mkdir -p %{buildroot}%{_isysroot}%{_rpmint_localstatedir}/lib/xdm/authdir
chmod 0700 %{buildroot}%{_isysroot}%{_rpmint_localstatedir}/lib/xdm/authdir

# we install our own config files for the xfs package
mkdir -p %{buildroot}%{_isysroot}%{_isysconfdir}/X11/fs
install -m 644 %{S:5} %{buildroot}%{_isysroot}%{_isysconfdir}/X11/fs/config
mkdir -p %{buildroot}%{_isysroot}%{_isysconfdir}/rc.d/init.d
install -m 755 %{S:6} %{buildroot}%{_isysroot}%{_isysconfdir}/rc.d/init.d/xfs

# Fix up symlinks
mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/{bin,include,lib,man}
ln -sf X11R6			%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11
ln -sf ../X11R6/bin		%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/bin/X11
ln -sf ../X11R6/include/DPS	%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/include/DPS
ln -sf ../X11R6/include/X11	%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/include/X11
ln -sf ../X11R6/lib/X11		%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/X11
ln -sf ../X11R6/man		%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/man/X11
cd %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/
for i in app-defaults lbxproxy proxymngr rstart xsm; do
	rm -f $i
	ln -s ../../../../etc/X11/$i $i
done
cd "$build_dir"

# no need to be SUID
if test -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xload; then
	chmod 755 %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xload
fi
# need to be SUID
if test -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xterm; then
	chmod 755 %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xterm
	chmod u+s %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xterm
fi

bdftopcf=${build_dir}/host-tools/bdftopcf
mkfontdir=${build_dir}/host-tools/mkfontdir

# EURO support
(cd %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/misc;
 tar xzf %{S:4};
 $bdftopcf -t Xlat9-10x20.bdf |gzip -9 >Xlat9-10x20-lat9.pcf.gz;
 $bdftopcf -t Xlat9-8x14.bdf |gzip -9 >Xlat9-8x14-lat9.pcf.gz;
 $bdftopcf -t Xlat9-9x16.bdf |gzip -9 >Xlat9-9x16-lat9.pcf.gz;
 rm *.bdf
 $mkfontdir .
)

# create at least an empty Compose dir for each locale; otherwise the
# keysysms of keyboard map files don't work
#
# also a dirty hack to make japanese, polish etc display correctly

chmod u+w %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/*/*

for i in \
        iso8859-1 iso8859-2 iso8859-3 iso8859-4 iso8859-5 iso8859-6 \
        iso8859-7 iso8859-8 iso8859-9 iso8859-10 iso8859-13 iso8859-14 \
	iso8859-15 armscii-8 georgian-academy georgian-ps ibm-cp1133 \
	koi8-r koi8-u mulelao-1 vi_VN.tcvn th_TH.TACTIS vi_VN.viscii \
	microsoft-cp1251 ja ja.SJIS ja.JIS ko zh zh_TW zh_TW.Big5 en_US.utf
do
	mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/$i
        touch %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/$i/Compose

	# is this still needed ?
	if [ -r %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/$i/XLC_LOCALE ]; then
		cp %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/$i/XLC_LOCALE %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/$i/aa
		cat %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/$i/aa | sed 's|^use_stdc_env|#use_stdc_env|' | \
			sed 's|^force_convert_to_mb|#force_convert_to_mb|' > \
			%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/$i/XLC_LOCALE
		rm %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/$i/aa
	fi
done

# some bitmap files seem to be misplaced
mv %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/bitmaps/* %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/bitmaps || :
rmdir %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/bitmaps ||:

gzip -9nf %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/*/* ||:
%{_rpmint_target}-strip %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:
%{_rpmint_target}-stack --fix=256k %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:

#
# Until now, all generated executables are for the target.
# Now generate some tools that are compiled for the host,
# but fetch the configuration files for the target.
# These are needed to cross-compile other packages later
#
%if "%{buildtype}" == "cross"
mkdir -p %{buildroot}%{_prefix}/bin

# imake.
cd config/imake
gcc -m32 -O2 -fomit-frame-pointer \
	-I../.. -I../../exports/include -I../../include -I../../exports/include/X11 \
	-D__MINT__ \
	-DDependCmd=\"%{_rpmint_target}-makedepend\" \
	-DImakeCmd=\"%{_rpmint_target}-imake\" \
	-DProjectRoot=\"%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6\" \
	-s -o imake imake.c
cp imake %{buildroot}%{_prefix}/bin/%{_rpmint_target}-imake

# xmkmf & gccmakedep are scripts
cd ../util
cpp -undef -traditional -DCONFIGDIRSPEC='"-I%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/config"' -Dimake=%{_rpmint_target}-imake ./xmkmf.cpp | sed -e /^\#/d | sed -e s/XCOMM/\#/ > xmkmf
chmod 755 xmkmf
cp xmkmf %{buildroot}%{_prefix}/bin/%{_rpmint_target}-xmkmf
cp gccmakedep %{buildroot}%{_prefix}/bin/%{_rpmint_target}-gccmakedep

# makedepend
cd ../makedepend
../../host-tools/imake -I../../config/cf -DTOPDIR=../.. -DCURDIR=config/makedepend \
	-DStdIncDir=\"%{_rpmint_sysroot}%{_rpmint_target_prefix}/include\"
make clean
make
cp makedepend %{buildroot}%{_prefix}/bin/%{_rpmint_target}-makedepend

%else

for tool in imake makedepend xmkmf gccmakedep; do
	ln -s $tool %{buildroot}/%{_rpmint_target_prefix}/X11R6/bin/%{_rpmint_target}-$tool
done

%endif


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%if "%{buildtype}" != "cross"
%pre xfs
#%{_rpmint_target_prefix}/sbin/useradd -c "X Font Server" \
#	-s /bin/false -r -d %{_isysconfdir}/X11/fs xfs 2>/dev/null || :

%post xfs
/sbin/chkconfig --add xfs

%preun xfs
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del xfs
# 	/usr/sbin/userdel xfs 2>/dev/null || :
#	/usr/sbin/groupdel xfs 2>/dev/null || :
#	service xfs stop >/dev/null 2>&1
fi

%postun xfs
if [ "$1" -ge "1" ]; then
	; #service xfs condrestart >/dev/null 2>&1
fi

%post 100dpi-fonts
/usr/sbin/chkfontpath -q -a %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/100dpi

%post 75dpi-fonts
/usr/sbin/chkfontpath -q -a %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/75dpi

%post cyrillic-fonts
/usr/sbin/chkfontpath -q -a %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/cyrillic

#%post ISO8859-2-100dpi-fonts
#/usr/sbin/chkfontpath -q -a %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/100dpi

#%post ISO8859-2-75dpi-fonts
#/usr/sbin/chkfontpath -q -a %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/75dpi

%postun 100dpi-fonts
if [ "$1" = "0" ]; then
  /usr/sbin/chkfontpath -q -r %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/100dpi
fi

%postun 75dpi-fonts
if [ "$1" = "0" ]; then
  /usr/sbin/chkfontpath -q -r %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/75dpi
fi

%postun cyrillic-fonts
if [ "$1" = "0" ]; then
  /usr/sbin/chkfontpath -q -r %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/cyrillic
fi

#%postun ISO8859-2-100dpi-fonts
#if [ "$1" = "0" ]; then
#  /usr/sbin/chkfontpath -q -r %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/100dpi
#fi

#%postun ISO8859-2-75dpi-fonts
#if [ "$1" = "0" ]; then
#  /usr/sbin/chkfontpath -q -r %{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/75dpi
#fi

%endif


%files
%defattr(-,root,root)

#%dir %%{_isysroot}%%{_isysconfdir}/X11/app-defaults
%dir %{_isysroot}%{_isysconfdir}/X11/lbxproxy
%dir %{_isysroot}%{_isysconfdir}/X11/proxymngr
%dir %{_isysroot}%{_isysconfdir}/X11/rstart
%dir %{_isysroot}%{_isysconfdir}/X11/xsm
%{_isysroot}%{_rpmint_localstatedir}/db/xkb

%config %{_isysroot}%{_isysconfdir}/X11/app-defaults/*
%config %{_isysroot}%{_isysconfdir}/X11/lbxproxy/AtomControl
%config %{_isysroot}%{_isysconfdir}/X11/proxymngr/pmconfig
%config %{_isysroot}%{_isysconfdir}/X11/rstart/*
%config %{_isysroot}%{_isysconfdir}/X11/xsm/system.xsm

#%dir %%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11
#%dir %%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/etc
#%dir %%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/CID
#%dir %%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/PEX
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Speedo
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Type1
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/encodings
#%dir %%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/local
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/misc
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/x11perfcomp

%{_isysroot}%{_rpmint_target_prefix}/X11
%{_isysroot}%{_rpmint_target_prefix}/bin/X11
%{_isysroot}%{_rpmint_target_prefix}/lib/X11
%{_isysroot}%{_rpmint_target_prefix}/man/X11

%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/app-defaults
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/lbxproxy
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/proxymngr
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/rstart
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/xsm

%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/Xmark
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/appres
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/atobm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/bdftopcf
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/bitmap
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/bmtoa
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/editres
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/iceauth
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/lbxproxy
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/lndir
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/makepsres
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/makestrs
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/mergelib
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/mkcfm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/mkdirhier
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/proxymngr
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/resize
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/revpath
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/rstart
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/rstartd
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/sessreg
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/setxkbmap
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/smproxy
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xauth
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xcmsdb
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xconsole
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xcutsel
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xdpyinfo
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xfindproxy
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xfwp
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/bin/xgamma		- XXX needs Xxf86vm extension
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xhost
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xkbbell
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xkbcomp
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xkbevd
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xkbprint
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xkbvleds
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xkbwatch
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xlsatoms
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xlsclients
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xlsfonts
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xmodmap
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xon
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xprop
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xrdb
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xrefresh
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xset
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xsetmode
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xsetpointer
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xsetroot
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xsm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xstdcmap
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xterm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xwd
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xwud
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/XErrorDB
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/XKeysymDB
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/etc/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/CID/*
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/PEX/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Speedo/*.spd
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Speedo/encodings.dir
%config(noreplace) %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Speedo/fonts.*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Type1/*.afm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Type1/*.pfa
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Type1/*.pfb
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Type1/encodings.dir
%config(noreplace) %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/Type1/fonts.*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/encodings/*
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/local/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/misc/*gz
%config(noreplace) %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/misc/fonts.*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/xkb/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/locale/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/x11perfcomp/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/appres.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/atobm.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/bdftopcf.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/bitmap.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/bmtoa.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/cxpm.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/editres.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/iceauth.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/lbxproxy.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/lndir.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/makedepend.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/makepsres.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/makestrs.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/mkcfm.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/mkdirhier.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/oclock.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/proxymngr.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/resize.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/revpath.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/rstart.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/rstartd.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/sessreg.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/setxkbmap.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/smproxy.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/sxpm.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xauth.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xcmsdb.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xconsole.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xcutsel.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xdpyinfo.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xfindproxy.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xfwp.1*
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/man/man1/xgamma.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xhost.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xkbcomp.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xkbevd.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xkbprint.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xkill.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xlogo.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xlsatoms.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xlsclients.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xlsfonts.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xmkmf.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xmodmap.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xon.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xprop.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xrdb.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xrefresh.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xset.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xsetmode.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xsetpointer.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xsetroot.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xsm.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xstdcmap.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xterm.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xwd.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xwud.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man7/*

%files tools
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/ico
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/listres
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/oclock
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/showfont
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/viewres
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/x11perf
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/x11perfcomp
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xbiff
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xcalc
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xclipboard
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xclock
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xditview
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xedit
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xev
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xeyes
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xfd
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xfontsel
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xgc
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xieperf
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xkill
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xload
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xlogo
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xmag
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xman
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xmessage
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xwininfo
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/xman.help
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/ico.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/listres.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/showfont.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/viewres.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/x11perf.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/x11perfcomp.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xbiff.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xcalc.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xclipboard.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xclock.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xditview.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xedit.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xev.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xeyes.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xfd.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xfontsel.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xgc.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xieperf.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xload.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xmag.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xman.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xmessage.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xwininfo.1*

%files xfs
%defattr(-,root,root)
#%dir %%{_isysroot}%%{_isysconfdir}/X11/fs
%config(noreplace) %{_isysroot}%{_isysconfdir}/X11/fs/config
%config %{_isysroot}%{_isysconfdir}/rc.d/init.d/xfs
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/fsinfo
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/fslsfonts
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/fstobdf
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/mkfontdir
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xfs
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fs
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/fsinfo.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/fslsfonts.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/fstobdf.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/mkfontdir.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xfs.1*

%files twm
%defattr(-,root,root)
%dir %{_isysroot}%{_isysconfdir}/X11/twm
%config %{_isysroot}%{_isysconfdir}/X11/twm/system.twmrc
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/twm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/twm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/twm.1*

%files devel
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/DPS
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/ICE
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/PEX5
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/PM
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/SM
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/Xaw
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/Xmu
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/bitmaps
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/extensions
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/fonts
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/config
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/cxpm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/gccmakedep
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/imake
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/makedepend
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/makeg
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/pswrap
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/bin/rman
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/sxpm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xmkmf
%if "%{buildtype}" == "cross"
%{_prefix}/bin/%{_rpmint_target}-imake
%{_prefix}/bin/%{_rpmint_target}-makedepend
%{_prefix}/bin/%{_rpmint_target}-xmkmf
%{_prefix}/bin/%{_rpmint_target}-gccmakedep
%else
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/%{_rpmint_target}-imake
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/%{_rpmint_target}-makedepend
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/%{_rpmint_target}-xmkmf
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/%{_rpmint_target}-gccmakedep
%endif
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/*.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/ICE/*.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/PEX5/*.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/PM/*.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/SM/*.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/Xaw/*.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/Xaw/*.c
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/Xmu/*.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/bitmaps/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/extensions/*.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/fonts/*.h
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/config/*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/makeg.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/pswrap.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/imake.1*
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/man/man1/rman.1*
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man3/*
%{_isysroot}%{_rpmint_target_prefix}/include/DPS
%{_isysroot}%{_rpmint_target_prefix}/include/X11

%files doc
%defattr(-,root,root)
%docdir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/doc
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/doc/*
%doc xc/doc/hardcopy/*

%files xdm
%defattr(-,root,root)
%dir %{_isysroot}%{_isysconfdir}/X11/xdm
%config %{_isysroot}%{_isysconfdir}/X11/xdm/GiveConsole
%config %{_isysroot}%{_isysconfdir}/X11/xdm/TakeConsole
%config %{_isysroot}%{_isysconfdir}/X11/xdm/Xaccess
%config %{_isysroot}%{_isysconfdir}/X11/xdm/Xresources
%config %{_isysroot}%{_isysconfdir}/X11/xdm/Xservers
%config %{_isysroot}%{_isysconfdir}/X11/xdm/Xsession
%config %{_isysroot}%{_isysconfdir}/X11/xdm/Xsetup_0
%config %{_isysroot}%{_isysconfdir}/X11/xdm/Xwilling
%{_isysroot}%{_isysconfdir}/X11/xdm/authdir
%config %{_isysroot}%{_isysconfdir}/X11/xdm/chooser
%{_isysroot}%{_isysconfdir}/X11/xdm/pixmaps
%config %{_isysroot}%{_isysconfdir}/X11/xdm/xdm-config
%dir %{_isysroot}%{_rpmint_localstatedir}/lib/xdm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xdm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/xdm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xdm.1*

%files 100dpi-fonts
%defattr(-,root,root)
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/100dpi
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/100dpi/*gz
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/100dpi/encodings.dir
%config(noreplace) %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/100dpi/fonts.*

%files 75dpi-fonts
%defattr(-,root,root)
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/75dpi
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/75dpi/*gz
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/75dpi/encodings.dir
%config(noreplace) %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/75dpi/fonts.*

%files cyrillic-fonts
%defattr(-,root,root)
%dir %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/cyrillic
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/cyrillic/*gz
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/cyrillic/encodings.dir
%config(noreplace) %{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/cyrillic/fonts.*

#%files ISO8859-2-100dpi-fonts
#%defattr(-,root,root)
#%dir %%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/100dpi
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/100dpi/*gz
#%config(noreplace) %%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/100dpi/fonts.*
#
#%files ISO8859-2-75dpi-fonts
#%defattr(-,root,root)
#%dir %%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/75dpi
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/75dpi/*gz
#%config(noreplace) %%{_isysroot}%%{_rpmint_target_prefix}/X11R6/lib/X11/fonts/latin2/75dpi/fonts.*
#
#%files Xnest
#%defattr(-,root,root)
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/bin/Xnest
#%%{_isysroot}%%{_rpmint_target_prefix}/X11R6/man/man1/Xnest.1*


%changelog
* Sun Mar 19 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Thu Dec 21 2000 Frank Naumann <fnaumann@freemint.de>
- first Sparemint release
