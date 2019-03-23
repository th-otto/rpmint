Summary       : Civilization clone (game)
Name          : freeciv
Version       : 1.11.4
Release       : 1
Copyright     : GPL
Group         : X11/Games

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.freeciv.org/

BuildRequires : XFree86-devel, Xaw3d, glib, gtk+, imlib-devel
Requires      : XFree86, glib, gtk+

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://freeciv.org/stable_version/%{name}-%{version}.tar.gz
Source1: freeciv-desktop.tar.gz
Patch0:  freeciv-gcc296.patch
Patch1:  freeciv-packaging.diff
Patch2:  freeciv-desktop.patch


%description
FreeCiv is an implementation of Civilization II for X Windows.


%prep
%setup -q -a 1
%patch -p1 -b .gcc296
%patch1 -p1 -b .destdir
%patch2 -p1 -b .desktop

# Rebuild makefiles after patching them...
find client -name Makefile.in |xargs rm -f
aclocal
autoheader
automake -a -i
autoconf


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--with-xaw3d \
	--with-zlib \
	--enable-debug=no
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	DESTDIR=${RPM_BUILD_ROOT} \
	localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale

chmod +x desktop/*wrapper
cp desktop/*wrapper ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}/etc/X11/applnk/Games ${RPM_BUILD_ROOT}%{_prefix}/share/pixmaps
cp desktop/*.desktop ${RPM_BUILD_ROOT}/etc/X11/applnk/Games
cp desktop/*.xpm ${RPM_BUILD_ROOT}%{_prefix}/share/pixmaps

pushd client
perl -p -i -e "s/CFLAGS = ${RPM_OPT_FLAGS}/CFLAGS = ${RPM_OPT_FLAGS} \`glib-config --cflags\`/" gui-gtk/Makefile
make clean
for i in 0 1 2 3 4 5 6 7 8 9 10; do
  perl -p -i -e "s/gui-xaw/gui-gtk/" Makefile
  perl -p -i -e "s|-I%{_prefix}/X11R6/include|\`glib-config --cflags\` \`gtk-config --cflags\` \`imlib-config --cflags-gdk\` -I%{_prefix}/X11R6/include|" Makefile 
  perl -p -i -e "s|-lXaw3d|\`glib-config --libs\` \`gtk-config --libs\` \`imlib-config --libs-gdk\`|" Makefile
done
make
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/civclient ${RPM_BUILD_ROOT}%{_prefix}/bin/civclient-xaw
cp civclient ${RPM_BUILD_ROOT}%{_prefix}/bin/civclient-gtk
ln -sf civclient-gtk ${RPM_BUILD_ROOT}%{_prefix}/bin/civclient
popd

%{_prefix}/bin/install -c civ  ${RPM_BUILD_ROOT}%{_prefix}/bin/civ

%{_prefix}/bin/install -d ${RPM_BUILD_ROOT}/etc/X11/app-defaults
mv ${RPM_BUILD_ROOT}%{_prefix}/share/freeciv/Freeciv ${RPM_BUILD_ROOT}/etc/X11/app-defaults/Freeciv

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%config /etc/X11/applnk/Games/*
%config /etc/X11/app-defaults/Freeciv
%{_prefix}/bin/*
%{_prefix}/share/freeciv
%{_prefix}/share/locale/*/*
%{_prefix}/share/pixmaps/*


%changelog
* Wed Jul 08 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
