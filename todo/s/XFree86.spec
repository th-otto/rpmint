Summary       : The basic fonts, programs and docs for an X workstation.
Name          : XFree86
Version       : 4.0
Release       : 1
Copyright     : MIT
Group         : User Interface/X

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

BuildRequires : gdbm >= 1.8.0, mintlib-devel >= 0.56, zlib-devel, ncurses-devel
Prereq        : /bin/ln

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

%define baseversion 400

Source0: ftp://ftp.xfree86.org/pub/XFree86/snapshots/%{version}/X%{baseversion}src-1.tgz
Source1: ftp://ftp.xfree86.org/pub/XFree86/snapshots/%{version}/X%{baseversion}src-2.tgz
Source2: ftp://ftp.xfree86.org/pub/XFree86/snapshots/%{version}/X%{baseversion}src-3.tgz
Source3: Euro.xmod
Source4: eurofonts-X11.tar.gz
Source5: xfs.config
Source6: xfs.init
Patch1:  XFree86-4.0-startx_xauth.patch
Patch2:  XFree86-4.0-xfsredhat.patch
Patch5:  XFree86-3.3.6-fixemacs.patch
Patch7:  XFree86-4.0-xtermresources.patch
Patch15: Xaw-unaligned.patch
Patch18: XFree86-4.0-fhs.patch
Patch20: XFree86-4.0-xdmsecurity.patch
Patch21: XFree86-4.0-moresecurity.patch
Patch22: XFree86-xfs-fix.patch
Patch30: xdm-4.0-servonly.patch
Patch31: xlib-textmeasure.patch
Patch50: XFree86-4.0-mint.patch
Patch51: XFree86-4.0-mint-cf.patch
Patch52: XFree86-4.0-mint-config.patch


%package tools
Summary       : Various tools for XFree86
Group         : User Interface/X
Requires      : XFree86

%package xfs
Summary       : A font server for the X Window System.
Group         : System Environment/Daemons
Prereq        : /sbin/chkconfig fileutils sed
#Requires      : initscripts >= 5.20

%package twm
Summary       : A simple window manager
Group         : User Interface/X
Requires      : XFree86
Provides      : windowmanager

%package devel
Summary       : X11R6 static libraries, headers and programming man pages.
Group         : Development/Libraries
Requires      : XFree86 = %{version}

%package doc
Summary       : Documentation on various X11 programming interfaces.
Group         : Documentation

%package xdm
Summary       : X Display Manager
Requires      : XFree86 = %{version}
Group         : User Interface/X

%package 100dpi-fonts
Summary       : X Window System 100dpi fonts.
Group         : User Interface/X
Prereq        : chkfontpath

%package 75dpi-fonts
Summary       : A set of 75 dpi resolution fonts for the X Window System.
Group         : User Interface/X
Prereq        : chkfontpath

%package cyrillic-fonts
Summary       : Cyrillic fonts for X.
Group         : User Interface/X
Prereq        : chkfontpath

#%package ISO8859-2-100dpi-fonts
#Summary       : ISO 8859-2 fonts in 100 dpi resolution for the X Window System.
#Group         : User Interface/X
#Prereq        : chkfontpath
#
#%package ISO8859-2-75dpi-fonts
#Summary       : A set of 75 dpi Central European language fonts for X.
#Group         : User Interface/X
#Prereq        : chkfontpath
#
#%package Xnest
#Summary       : A nested XFree86 server.
#Group         : User Interface/X Hardware Support
#Requires      : XFree86 = %{version}



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
%setup -q -c -a 1 -a 2

%patch1  -p1 -b .startx_xauth
%patch2  -p1 -b .xfsredhat
%patch5  -p1 -b .fixemacs
%patch7  -p1 -b .xtermresources
%patch15 -p1 -b .Xaw-unaligned
%patch18 -p1 -b .fhs
%patch20 -p1 -b .xdmsecurity
%patch21 -p1 -b .moresecurity
%patch22 -p0 -b .xfs-fix
%patch30 -p1 -b .xdm-4.0-servonly
%patch31 -p0 -b .xlib-textmeasure

%patch50 -p1 -b .mint
%patch51 -p1 -b .mint
%patch52 -p1 -b .mint


%build
ln -s include xc/X11

make World -C xc \
	CDEBUGFLAGS="$RPM_OPT_FLAGS" \
	CXXDEBUGFLAGS="$RPM_OPT_FLAGS"
#make -C xc \
#	CDEBUGFLAGS="$RPM_OPT_FLAGS" \
#	CXXDEBUGFLAGS="$RPM_OPT_FLAGS"

echo PACKAGING DOCUMENTATION
# rezip these - they are in the old compress format
find xc/doc/hardcopy -name \*.PS.Z | xargs gzip -df
find xc/doc/hardcopy -name \*.PS | xargs gzip

# Generate docs
groff -Tascii -ms xc/doc/misc/RELNOTES.ms             > xc/doc/hardcopy/RELNOTES.txt
rm xc/doc/hardcopy/BDF/*
groff -Tascii -ms xc/doc/specs/BDF/bdf.ms             > xc/doc/hardcopy/BDF/bdf.txt
rm xc/doc/hardcopy/CTEXT/*
groff -Tascii -ms xc/doc/specs/CTEXT/ctext.tbl.ms     > xc/doc/hardcopy/CTEXT/ctext.tbl.txt
rm xc/doc/hardcopy/FSProtocol/*
groff -Tascii -ms xc/doc/specs/FSProtocol/protocol.ms > xc/doc/hardcopy/FSProtocol/protocol.txt
rm xc/doc/hardcopy/ICCCM/*
groff -Tascii -ms xc/doc/specs/ICCCM/icccm.ms         > xc/doc/hardcopy/ICCCM/icccm.txt
rm xc/doc/hardcopy/ICE/*
groff -Tascii -ms xc/doc/specs/ICE/ICElib.ms          > xc/doc/hardcopy/ICE/ICElib.txt
groff -Tascii -ms xc/doc/specs/ICE/ice.ms             > xc/doc/hardcopy/ICE/ice.txt
cp xc/doc/specs/PM/PM_spec xc/doc/hardcopy/ICE
rm xc/doc/hardcopy/SM/*
groff -Tascii -ms xc/doc/specs/SM/SMlib.ms            > xc/doc/hardcopy/SM/SMlib.txt
rm xc/doc/hardcopy/XDMCP/*
groff -Tascii -ms xc/doc/specs/XDMCP/xdmcp.ms         > xc/doc/hardcopy/XDMCP/xdmcp.txt
rm xc/doc/hardcopy/XIM/*
groff -Tascii -ms xc/doc/specs/XIM/xim.ms             > xc/doc/hardcopy/XIM/xim.txt
rm xc/doc/hardcopy/XLFD/*
groff -Tascii -ms xc/doc/specs/XLFD/xlfd.tbl.ms       > xc/doc/hardcopy/XLFD/xlfd.tbl.txt


%install
rm -rf ${RPM_BUILD_ROOT}

make DESTDIR=${RPM_BUILD_ROOT} install install.man -C xc

# we don't want the libz.a from XFree86 -- it's broken
rm -f ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/libz.a

# explicitly create X authdir
mkdir -p ${RPM_BUILD_ROOT}/var/lib/xdm/authdir
chmod 0700 ${RPM_BUILD_ROOT}/var/lib/xdm/authdir

# we install our own config files for the xfs package
mkdir -p ${RPM_BUILD_ROOT}/etc/X11/fs
install -m 644 ${RPM_SOURCE_DIR}/xfs.config \
	${RPM_BUILD_ROOT}/etc/X11/fs/config
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
install -m 755 ${RPM_SOURCE_DIR}/xfs.init \
	${RPM_BUILD_ROOT}/etc/rc.d/init.d/xfs

# Fix up symlinks
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/{bin,include,lib,man}
ln -sf X11R6			${RPM_BUILD_ROOT}%{_prefix}/X11
ln -sf ../X11R6/bin		${RPM_BUILD_ROOT}%{_prefix}/bin/X11
ln -sf ../X11R6/include/DPS	${RPM_BUILD_ROOT}%{_prefix}/include/DPS
ln -sf ../X11R6/include/X11	${RPM_BUILD_ROOT}%{_prefix}/include/X11
ln -sf ../X11R6/lib/X11		${RPM_BUILD_ROOT}%{_prefix}/lib/X11
ln -sf ../X11R6/man		${RPM_BUILD_ROOT}%{_prefix}/man/X11

# no need to be SUID
chmod 755 ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/xload
# need to be SUID
chmod 755 ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/xterm
chmod u+s ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/xterm

# EURO support
(cd ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/fonts/misc;
 tar xzf ${RPM_SOURCE_DIR}/eurofonts-X11.tar.gz;
 bdftopcf -t Xlat9-10x20.bdf |gzip -9 >Xlat9-10x20-lat9.pcf.gz;
 bdftopcf -t Xlat9-8x14.bdf |gzip -9 >Xlat9-8x14-lat9.pcf.gz;
 bdftopcf -t Xlat9-9x16.bdf |gzip -9 >Xlat9-9x16-lat9.pcf.gz;
 rm *.bdf
 mkfontdir ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/fonts/misc
)

# create at least an empty Compose dir for each locale; otherwise the
# keysysms of keyboard map files don't work
#
# also a dirty hack to make japanese, polish etc display correctly

chmod u+w ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/locale/*/*

for i in \
        iso8859-1 iso8859-2 iso8859-3 iso8859-4 iso8859-5 iso8859-6 \
        iso8859-7 iso8859-8 iso8859-9 iso8859-10 iso8859-13 iso8859-14 \
	iso8859-15 armscii-8 georgian-academy georgian-ps ibm-cp1133 \
	koi8-r koi8-u mulelao-1 vi_VN.tcvn th_TH.TACTIS vi_VN.viscii \
	microsoft-cp1251 ja ja.SJIS ja.JIS ko zh zh_TW zh_TW.Big5 en_US.utf
do
	mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/locale/$i
        touch ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/locale/$i/Compose

	# is this still needed ?
	if [ -r ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/locale/$i/XLC_LOCALE ]; then
		cp ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/locale/$i/XLC_LOCALE \
			${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/locale/$i/aa
		cat ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/locale/$i/aa | \
			sed 's|^use_stdc_env|#use_stdc_env|' | \
			sed 's|^force_convert_to_mb|#force_convert_to_mb|' > \
			${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/locale/$i/XLC_LOCALE
		rm ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/locale/$i/aa
	fi
done

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/*/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:


%clean
rm -rf ${RPM_BUILD_ROOT}


%pre xfs
#%{_prefix}/sbin/useradd -c "X Font Server" \
#	-s /bin/false -r -d /etc/X11/fs xfs 2>/dev/null || :

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
/usr/sbin/chkfontpath -q -a %{_prefix}/X11R6/lib/X11/fonts/100dpi

%post 75dpi-fonts
/usr/sbin/chkfontpath -q -a %{_prefix}/X11R6/lib/X11/fonts/75dpi

%post cyrillic-fonts
/usr/sbin/chkfontpath -q -a %{_prefix}/X11R6/lib/X11/fonts/cyrillic

#%post ISO8859-2-100dpi-fonts
#/usr/sbin/chkfontpath -q -a %{_prefix}/X11R6/lib/X11/fonts/latin2/100dpi

#%post ISO8859-2-75dpi-fonts
#/usr/sbin/chkfontpath -q -a %{_prefix}/X11R6/lib/X11/fonts/latin2/75dpi

%postun 100dpi-fonts
if [ "$1" = "0" ]; then
  /usr/sbin/chkfontpath -q -r %{_prefix}/X11R6/lib/X11/fonts/100dpi
fi

%postun 75dpi-fonts
if [ "$1" = "0" ]; then
  /usr/sbin/chkfontpath -q -r %{_prefix}/X11R6/lib/X11/fonts/75dpi
fi

%postun cyrillic-fonts
if [ "$1" = "0" ]; then
  /usr/sbin/chkfontpath -q -r %{_prefix}/X11R6/lib/X11/fonts/cyrillic
fi

#%postun ISO8859-2-100dpi-fonts
#if [ "$1" = "0" ]; then
#  /usr/sbin/chkfontpath -q -r %{_prefix}/X11R6/lib/X11/fonts/latin2/100dpi
#fi

#%postun ISO8859-2-75dpi-fonts
#if [ "$1" = "0" ]; then
#  /usr/sbin/chkfontpath -q -r %{_prefix}/X11R6/lib/X11/fonts/latin2/75dpi
#fi


%files
%defattr(-,root,root)

#%dir /etc/X11/app-defaults
#%dir /etc/X11/lbxproxy
%dir /etc/X11/proxymngr
%dir /etc/X11/rstart
%dir /etc/X11/xsm

%config /etc/X11/app-defaults/*
#%config /etc/X11/lbxproxy/AtomControl
%config /etc/X11/proxymngr/pmconfig
%config /etc/X11/rstart/*
%config /etc/X11/xsm/system.xsm

#%dir %{_prefix}/X11R6/lib/X11
#%dir %{_prefix}/X11R6/lib/X11/etc
#%dir %{_prefix}/X11R6/lib/X11/fonts
%dir %{_prefix}/X11R6/lib/X11/fonts/CID
#%dir %{_prefix}/X11R6/lib/X11/fonts/PEX
%dir %{_prefix}/X11R6/lib/X11/fonts/Speedo
%dir %{_prefix}/X11R6/lib/X11/fonts/Type1
%dir %{_prefix}/X11R6/lib/X11/fonts/encodings
#%dir %{_prefix}/X11R6/lib/X11/fonts/local
%dir %{_prefix}/X11R6/lib/X11/fonts/misc
%dir %{_prefix}/X11R6/lib/X11/locale
%dir %{_prefix}/X11R6/lib/X11/x11perfcomp

%{_prefix}/X11
%{_prefix}/bin/X11
%{_prefix}/lib/X11
%{_prefix}/man/X11

%{_prefix}/X11R6/lib/X11/app-defaults
#%{_prefix}/X11R6/lib/X11/lbxproxy
%{_prefix}/X11R6/lib/X11/proxymngr
%{_prefix}/X11R6/lib/X11/rstart
%{_prefix}/X11R6/lib/X11/xsm

%{_prefix}/X11R6/bin/Xmark
%{_prefix}/X11R6/bin/appres
%{_prefix}/X11R6/bin/atobm
%{_prefix}/X11R6/bin/bdftopcf
%{_prefix}/X11R6/bin/bitmap
%{_prefix}/X11R6/bin/bmtoa
%{_prefix}/X11R6/bin/editres
%{_prefix}/X11R6/bin/iceauth
#%{_prefix}/X11R6/bin/lbxproxy		- XXX illegal instruction
%{_prefix}/X11R6/bin/lndir
%{_prefix}/X11R6/bin/makepsres
%{_prefix}/X11R6/bin/makestrs
%{_prefix}/X11R6/bin/mergelib
%{_prefix}/X11R6/bin/mkcfm
%{_prefix}/X11R6/bin/mkdirhier
%{_prefix}/X11R6/bin/proxymngr
%{_prefix}/X11R6/bin/resize
%{_prefix}/X11R6/bin/revpath
%{_prefix}/X11R6/bin/rstart
%{_prefix}/X11R6/bin/rstartd
#%{_prefix}/X11R6/bin/sessreg		- XXX build problem
%{_prefix}/X11R6/bin/setxkbmap
%{_prefix}/X11R6/bin/smproxy
%{_prefix}/X11R6/bin/xauth
%{_prefix}/X11R6/bin/xcmsdb
%{_prefix}/X11R6/bin/xconsole
%{_prefix}/X11R6/bin/xcutsel
%{_prefix}/X11R6/bin/xdpyinfo
%{_prefix}/X11R6/bin/xfindproxy
#%{_prefix}/X11R6/bin/xfwp		- XXX build problem
#%{_prefix}/X11R6/bin/xgamma		- XXX build problem
%{_prefix}/X11R6/bin/xhost
%{_prefix}/X11R6/bin/xkbbell
%{_prefix}/X11R6/bin/xkbcomp
%{_prefix}/X11R6/bin/xkbevd
%{_prefix}/X11R6/bin/xkbprint
%{_prefix}/X11R6/bin/xkbvleds
%{_prefix}/X11R6/bin/xkbwatch
%{_prefix}/X11R6/bin/xlsatoms
%{_prefix}/X11R6/bin/xlsclients
%{_prefix}/X11R6/bin/xlsfonts
%{_prefix}/X11R6/bin/xmodmap
%{_prefix}/X11R6/bin/xon
%{_prefix}/X11R6/bin/xprop
%{_prefix}/X11R6/bin/xrdb
%{_prefix}/X11R6/bin/xrefresh
%{_prefix}/X11R6/bin/xset
%{_prefix}/X11R6/bin/xsetmode
%{_prefix}/X11R6/bin/xsetpointer
%{_prefix}/X11R6/bin/xsetroot
%{_prefix}/X11R6/bin/xsm
%{_prefix}/X11R6/bin/xstdcmap
%{_prefix}/X11R6/bin/xterm
%{_prefix}/X11R6/bin/xwd
%{_prefix}/X11R6/bin/xwud
%{_prefix}/X11R6/lib/X11/XErrorDB
%{_prefix}/X11R6/lib/X11/XKeysymDB
#%{_prefix}/X11R6/lib/X11/etc/*
%{_prefix}/X11R6/lib/X11/fonts/CID/*
#%{_prefix}/X11R6/lib/X11/fonts/PEX/*
%{_prefix}/X11R6/lib/X11/fonts/Speedo/*.spd
%{_prefix}/X11R6/lib/X11/fonts/Speedo/encodings.dir
%config(noreplace) %{_prefix}/X11R6/lib/X11/fonts/Speedo/fonts.*
%{_prefix}/X11R6/lib/X11/fonts/Type1/*.afm
%{_prefix}/X11R6/lib/X11/fonts/Type1/*.pfa
%{_prefix}/X11R6/lib/X11/fonts/Type1/*.pfb
%{_prefix}/X11R6/lib/X11/fonts/Type1/encodings.dir
%config(noreplace) %{_prefix}/X11R6/lib/X11/fonts/Type1/fonts.*
%{_prefix}/X11R6/lib/X11/fonts/encodings/*
#%{_prefix}/X11R6/lib/X11/fonts/local/*
%{_prefix}/X11R6/lib/X11/fonts/misc/*gz
%config(noreplace) %{_prefix}/X11R6/lib/X11/fonts/misc/fonts.*
%{_prefix}/X11R6/lib/X11/locale/*
%{_prefix}/X11R6/lib/X11/x11perfcomp/*
%{_prefix}/X11R6/man/man1/appres.1*
%{_prefix}/X11R6/man/man1/atobm.1*
%{_prefix}/X11R6/man/man1/bdftopcf.1*
%{_prefix}/X11R6/man/man1/bitmap.1*
%{_prefix}/X11R6/man/man1/bmtoa.1*
%{_prefix}/X11R6/man/man1/cxpm.1*
%{_prefix}/X11R6/man/man1/editres.1*
%{_prefix}/X11R6/man/man1/iceauth.1*
#%{_prefix}/X11R6/man/man1/lbxproxy.1*
%{_prefix}/X11R6/man/man1/lndir.1*
%{_prefix}/X11R6/man/man1/makedepend.1*
%{_prefix}/X11R6/man/man1/makepsres.1*
%{_prefix}/X11R6/man/man1/makestrs.1*
%{_prefix}/X11R6/man/man1/mkcfm.1*
%{_prefix}/X11R6/man/man1/mkdirhier.1*
%{_prefix}/X11R6/man/man1/oclock.1*
%{_prefix}/X11R6/man/man1/proxymngr.1*
%{_prefix}/X11R6/man/man1/resize.1*
%{_prefix}/X11R6/man/man1/revpath.1*
%{_prefix}/X11R6/man/man1/rstart.1*
%{_prefix}/X11R6/man/man1/rstartd.1*
%{_prefix}/X11R6/man/man1/sessreg.1*
%{_prefix}/X11R6/man/man1/setxkbmap.1*
%{_prefix}/X11R6/man/man1/smproxy.1*
%{_prefix}/X11R6/man/man1/sxpm.1*
%{_prefix}/X11R6/man/man1/xauth.1*
%{_prefix}/X11R6/man/man1/xcmsdb.1*
%{_prefix}/X11R6/man/man1/xconsole.1*
%{_prefix}/X11R6/man/man1/xcutsel.1*
%{_prefix}/X11R6/man/man1/xdpyinfo.1*
%{_prefix}/X11R6/man/man1/xfindproxy.1*
#%{_prefix}/X11R6/man/man1/xfwp.1*
#%{_prefix}/X11R6/man/man1/xgamma.1*
%{_prefix}/X11R6/man/man1/xhost.1*
%{_prefix}/X11R6/man/man1/xkbcomp.1*
%{_prefix}/X11R6/man/man1/xkbevd.1*
%{_prefix}/X11R6/man/man1/xkbprint.1*
%{_prefix}/X11R6/man/man1/xkill.1*
%{_prefix}/X11R6/man/man1/xlogo.1*
%{_prefix}/X11R6/man/man1/xlsatoms.1*
%{_prefix}/X11R6/man/man1/xlsclients.1*
%{_prefix}/X11R6/man/man1/xlsfonts.1*
%{_prefix}/X11R6/man/man1/xmkmf.1*
%{_prefix}/X11R6/man/man1/xmodmap.1*
%{_prefix}/X11R6/man/man1/xon.1*
%{_prefix}/X11R6/man/man1/xprop.1*
%{_prefix}/X11R6/man/man1/xrdb.1*
%{_prefix}/X11R6/man/man1/xrefresh.1*
%{_prefix}/X11R6/man/man1/xset.1*
%{_prefix}/X11R6/man/man1/xsetmode.1*
%{_prefix}/X11R6/man/man1/xsetpointer.1*
%{_prefix}/X11R6/man/man1/xsetroot.1*
%{_prefix}/X11R6/man/man1/xsm.1*
%{_prefix}/X11R6/man/man1/xstdcmap.1*
%{_prefix}/X11R6/man/man1/xterm.1*
%{_prefix}/X11R6/man/man1/xwd.1*
%{_prefix}/X11R6/man/man1/xwud.1*
%{_prefix}/X11R6/man/man7/*

%files tools
%defattr(-,root,root)
%{_prefix}/X11R6/bin/ico
%{_prefix}/X11R6/bin/listres
%{_prefix}/X11R6/bin/oclock
%{_prefix}/X11R6/bin/showfont
%{_prefix}/X11R6/bin/viewres
%{_prefix}/X11R6/bin/x11perf
%{_prefix}/X11R6/bin/x11perfcomp
%{_prefix}/X11R6/bin/xbiff
%{_prefix}/X11R6/bin/xcalc
%{_prefix}/X11R6/bin/xclipboard
%{_prefix}/X11R6/bin/xclock
%{_prefix}/X11R6/bin/xditview
%{_prefix}/X11R6/bin/xedit
%{_prefix}/X11R6/bin/xev
%{_prefix}/X11R6/bin/xeyes
%{_prefix}/X11R6/bin/xfd
%{_prefix}/X11R6/bin/xfontsel
%{_prefix}/X11R6/bin/xgc
%{_prefix}/X11R6/bin/xieperf
%{_prefix}/X11R6/bin/xkill
%{_prefix}/X11R6/bin/xload
%{_prefix}/X11R6/bin/xlogo
%{_prefix}/X11R6/bin/xmag
%{_prefix}/X11R6/bin/xman
%{_prefix}/X11R6/bin/xmessage
%{_prefix}/X11R6/bin/xwininfo
%{_prefix}/X11R6/lib/X11/xman.help
%{_prefix}/X11R6/man/man1/ico.1*
%{_prefix}/X11R6/man/man1/listres.1*
%{_prefix}/X11R6/man/man1/showfont.1*
%{_prefix}/X11R6/man/man1/viewres.1*
%{_prefix}/X11R6/man/man1/x11perf.1*
%{_prefix}/X11R6/man/man1/x11perfcomp.1*
%{_prefix}/X11R6/man/man1/xbiff.1*
%{_prefix}/X11R6/man/man1/xcalc.1*
%{_prefix}/X11R6/man/man1/xclipboard.1*
%{_prefix}/X11R6/man/man1/xclock.1*
%{_prefix}/X11R6/man/man1/xditview.1*
%{_prefix}/X11R6/man/man1/xedit.1*
%{_prefix}/X11R6/man/man1/xev.1*
%{_prefix}/X11R6/man/man1/xeyes.1*
%{_prefix}/X11R6/man/man1/xfd.1*
%{_prefix}/X11R6/man/man1/xfontsel.1*
%{_prefix}/X11R6/man/man1/xgc.1*
%{_prefix}/X11R6/man/man1/xieperf.1*
%{_prefix}/X11R6/man/man1/xload.1*
%{_prefix}/X11R6/man/man1/xmag.1*
%{_prefix}/X11R6/man/man1/xman.1*
%{_prefix}/X11R6/man/man1/xmessage.1*
%{_prefix}/X11R6/man/man1/xwininfo.1*

%files xfs
%defattr(-,root,root)
#%dir /etc/X11/fs
%config(noreplace) /etc/X11/fs/config
%config /etc/rc.d/init.d/xfs
%{_prefix}/X11R6/bin/fsinfo
%{_prefix}/X11R6/bin/fslsfonts
%{_prefix}/X11R6/bin/fstobdf
%{_prefix}/X11R6/bin/mkfontdir
%{_prefix}/X11R6/bin/xfs
%{_prefix}/X11R6/lib/X11/fs
%{_prefix}/X11R6/man/man1/fsinfo.1*
%{_prefix}/X11R6/man/man1/fslsfonts.1*
%{_prefix}/X11R6/man/man1/fstobdf.1*
%{_prefix}/X11R6/man/man1/mkfontdir.1*
%{_prefix}/X11R6/man/man1/xfs.1*

%files twm
%defattr(-,root,root)
%dir /etc/X11/twm
%config /etc/X11/twm/system.twmrc
%{_prefix}/X11R6/bin/twm
%{_prefix}/X11R6/lib/X11/twm
%{_prefix}/X11R6/man/man1/twm.1*

%files devel
%defattr(-,root,root)
%dir %{_prefix}/X11R6/include/DPS
%dir %{_prefix}/X11R6/include/X11
%dir %{_prefix}/X11R6/include/X11/ICE
%dir %{_prefix}/X11R6/include/X11/PEX5
%dir %{_prefix}/X11R6/include/X11/PM
%dir %{_prefix}/X11R6/include/X11/SM
%dir %{_prefix}/X11R6/include/X11/Xaw
%dir %{_prefix}/X11R6/include/X11/Xmu
%dir %{_prefix}/X11R6/include/X11/bitmaps
%dir %{_prefix}/X11R6/include/X11/extensions
%dir %{_prefix}/X11R6/include/X11/fonts
%dir %{_prefix}/X11R6/lib/X11/config
%{_prefix}/X11R6/bin/cxpm
%{_prefix}/X11R6/bin/gccmakedep
%{_prefix}/X11R6/bin/imake
%{_prefix}/X11R6/bin/makedepend
%{_prefix}/X11R6/bin/makeg
%{_prefix}/X11R6/bin/pswrap
#%{_prefix}/X11R6/bin/rman
%{_prefix}/X11R6/bin/sxpm
%{_prefix}/X11R6/bin/xmkmf
%{_prefix}/X11R6/include/X11/*.h
%{_prefix}/X11R6/include/X11/ICE/*.h
%{_prefix}/X11R6/include/X11/PEX5/*.h
%{_prefix}/X11R6/include/X11/PM/*.h
%{_prefix}/X11R6/include/X11/SM/*.h
%{_prefix}/X11R6/include/X11/Xaw/*.h
%{_prefix}/X11R6/include/X11/Xmu/*.h
%{_prefix}/X11R6/include/X11/bitmaps/*
%{_prefix}/X11R6/include/X11/extensions/*.h
%{_prefix}/X11R6/include/X11/fonts/*.h
%{_prefix}/X11R6/lib/*.a
%{_prefix}/X11R6/lib/X11/config/*
%{_prefix}/X11R6/man/man1/makeg.1*
%{_prefix}/X11R6/man/man1/pswrap.1*
#%{_prefix}/X11R6/man/man1/rman.1*
%{_prefix}/X11R6/man/man3/*
%{_prefix}/include/DPS
%{_prefix}/include/X11

%files doc
%defattr(-,root,root)
%docdir %{_prefix}/X11R6/lib/X11/doc
#%{_prefix}/X11R6/lib/X11/doc/*
%doc xc/doc/hardcopy/*

%files xdm
%defattr(-,root,root)
%dir /etc/X11/xdm
#%dir /etc/X11/xdm/pixmaps
#%config /etc/X11/xdm/Xservers
%dir %attr(0700,root,root) /etc/X11/xdm/authdir
%dir /var/lib/xdm
#%config /etc/X11/xdm/Xresources
#%config /etc/X11/xdm/Xwilling
#%config /etc/X11/xdm/chooser
#%config /etc/X11/xdm/xdm-config
#/etc/X11/xdm/pixmaps/*
%{_prefix}/X11R6/bin/xdm
%{_prefix}/X11R6/lib/X11/xdm
%{_prefix}/X11R6/man/man1/xdm.1*

%files 100dpi-fonts
%defattr(-,root,root)
%dir %{_prefix}/X11R6/lib/X11/fonts/100dpi
%{_prefix}/X11R6/lib/X11/fonts/100dpi/*gz
%{_prefix}/X11R6/lib/X11/fonts/100dpi/encodings.dir
%config(noreplace) %{_prefix}/X11R6/lib/X11/fonts/100dpi/fonts.*

%files 75dpi-fonts
%defattr(-,root,root)
%dir %{_prefix}/X11R6/lib/X11/fonts/75dpi
%{_prefix}/X11R6/lib/X11/fonts/75dpi/*gz
%{_prefix}/X11R6/lib/X11/fonts/75dpi/encodings.dir
%config(noreplace) %{_prefix}/X11R6/lib/X11/fonts/75dpi/fonts.*

%files cyrillic-fonts
%defattr(-,root,root)
%dir %{_prefix}/X11R6/lib/X11/fonts/cyrillic
%{_prefix}/X11R6/lib/X11/fonts/cyrillic/*gz
%{_prefix}/X11R6/lib/X11/fonts/cyrillic/encodings.dir
%config(noreplace) %{_prefix}/X11R6/lib/X11/fonts/cyrillic/fonts.*

#%files ISO8859-2-100dpi-fonts
#%defattr(-,root,root)
#%dir %{_prefix}/X11R6/lib/X11/fonts/latin2/100dpi
#%{_prefix}/X11R6/lib/X11/fonts/latin2/100dpi/*gz
#%config(noreplace) %{_prefix}/X11R6/lib/X11/fonts/latin2/100dpi/fonts.*
#
#%files ISO8859-2-75dpi-fonts
#%defattr(-,root,root)
#%dir %{_prefix}/X11R6/lib/X11/fonts/latin2/75dpi
#%{_prefix}/X11R6/lib/X11/fonts/latin2/75dpi/*gz
#%config(noreplace) %{_prefix}/X11R6/lib/X11/fonts/latin2/75dpi/fonts.*
#
#%files Xnest
#%defattr(-,root,root)
#%{_prefix}/X11R6/bin/Xnest
#%{_prefix}/X11R6/man/man1/Xnest.1*


%changelog
* Thu Dec 21 2000 Frank Naumann <fnaumann@freemint.de>
- first Sparemint release
