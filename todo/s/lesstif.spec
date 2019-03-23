Summary       : An OSF/Motif(R) clone.
Name          : lesstif
Version       : 0.92.6
Release       : 1
Copyright     : LGPL
Group         : System Environment/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.lesstif.org/

BuildRequires : XFree86-devel bison flex
Requires      : XFree86-devel

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.hungry.com/pub/hungry/lesstif/%{name}-%{version}.tar.gz


%description
Lesstif is an API compatible clone of the Motif toolkit.
Currently Lesstif is partially implemented with most of the API in place.
Having said this, some of the internal functionality is still missing.
Many Motif applications compile and run out-of-the-box with LessTif,
and we want to hear about those that don't.

%package mwm
Summary       : Lesstif Motif window manager clone based on fvwm.
Group         : User Interface/Desktops
Requires      : XFree86-devel
#, lesstif = %{PACKAGE_VERSION}

%description mwm
MWM is a window manager that adheres largely to the Motif mwm specification.

%package clients
Summary       : Lesstif clients.
Group         : Development/Tools
Requires      : XFree86-devel
#, lesstif = %{PACKAGE_VERSION}

%description clients
Uil and xmbind.

%package devel
Summary       : Static library and header files for LessTif/Motif development.
Group         : Development/Libraries
Requires      : XFree86-devel
#, lesstif = %{PACKAGE_VERSION}

%description devel
This package contains the lesstif static library and header files
required to develop Motif-based applications.
Package also contains development documentation in html (Lessdox), and
mxmkmf for Lesstif.


%prep
%setup -q -n lesstif-%{version}

LESSTIFTOP=$PWD


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}/X11R6 \
	--enable-static \
	--enable-build-12 \
	--disable-build-20 \
	--enable-build-21 \
	--disable-maintainer-mode \
	--disable-debug \
	--enable-build-Xlt \
	--enable-build-Xbae \
	--enable-default-21
make MAN2HTML=/usr/bin/man2html


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

chmod a-x [A-Z]*
make install MAN2HTML=/usr/bin/man2html DESTDIR=${RPM_BUILD_ROOT}

strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/mwm
strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/uil
strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/xmbind

strip --discard-locals ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/libXbae.a
strip --discard-locals ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/libXlt.a

strip --discard-locals ${RPM_BUILD_ROOT}%{_prefix}/X11R6/LessTif/Motif1.2/lib/libMrm.a
strip --discard-locals ${RPM_BUILD_ROOT}%{_prefix}/X11R6/LessTif/Motif1.2/lib/libUil.a
strip --discard-locals ${RPM_BUILD_ROOT}%{_prefix}/X11R6/LessTif/Motif1.2/lib/libXm.a

strip --discard-locals ${RPM_BUILD_ROOT}%{_prefix}/X11R6/LessTif/Motif2.1/lib/libDt.a
strip --discard-locals ${RPM_BUILD_ROOT}%{_prefix}/X11R6/LessTif/Motif2.1/lib/libMrm.a
strip --discard-locals ${RPM_BUILD_ROOT}%{_prefix}/X11R6/LessTif/Motif2.1/lib/libUil.a
strip --discard-locals ${RPM_BUILD_ROOT}%{_prefix}/X11R6/LessTif/Motif2.1/lib/libXm.a


install -d ${RPM_BUILD_ROOT}/etc/X11
mv ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/mwm ${RPM_BUILD_ROOT}/etc/X11
ln -sf /etc/X11/mwm ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/mwm

install -d ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man
install -d ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/man1
install -d ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/man5
install -c -m 644 doc/lessdox/clients/mwmrc.5   ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/man5
install -c -m 644 doc/lessdox/clients/mwm.1     ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/man1
install -c -m 644 doc/lessdox/clients/lesstif.1 ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/man1
install -c -m 644 doc/lessdox/clients/xmbind.1  ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/man1
install -c -m 644 doc/lessdox/*/*.html ${RPM_BUILD_ROOT}%{_prefix}/X11R6/LessTif/doc/Lessdox || :

# generate config files 
# cd ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/config;
# 
# mv Motif.rules Motif-lesstif.rules
# mv Motif.tmpl  Motif-lesstif.tmpl

# cleanup in a preparation for an installation - unify layout

( cd ${RPM_BUILD_ROOT}%{_prefix}/X11R6/LessTif ; \
  mv doc/man/man1/* ../man/man1 ; \
  mv doc/man/man3/* ../man/man3 ; \
  mv doc/man/man5/* ../man/man5 ; \
  rm -rf doc/man )

%{_prefix}/bin/install -d ${RPM_BUILD_ROOT}/etc/X11/app-defaults
mv ${RPM_BUILD_ROOT}%{_prefix}/X11R6/lib/X11/app-defaults/Mwm ${RPM_BUILD_ROOT}/etc/X11/app-defaults/Mwm

strip ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/X11R6/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files mwm
%doc clients/Motif-1.2/mwm/COPYING clients/Motif-1.2/mwm/README
%attr(755, root, root) %dir /etc/X11/mwm
%attr(644, root, root) %config /etc/X11/mwm/*
%attr(644, root, root) %config /etc/X11/app-defaults/Mwm
%attr(755, root, root) %{_prefix}/X11R6/bin/mwm
%attr(755, root, root) %{_prefix}/X11R6/lib/X11/mwm
%attr(644, root, root) %{_prefix}/X11R6/man/man1/mwm.1.gz
%attr(644, root, root) %{_prefix}/X11R6/man/man5/mwmrc.5.gz
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif2.1/bin/mwm

%files clients
%doc doc/UIL.txt
%attr(755, root, root) %{_prefix}/X11R6/bin/uil
%attr(755, root, root) %{_prefix}/X11R6/bin/xmbind
%attr(644, root, root) %{_prefix}/X11R6/man/man1/xmbind.1.gz
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif2.1/bin/uil
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif2.1/bin/xmbind

%files devel
# root package
%doc AUTHORS BUG-REPORTING COPYING COPYING.LIB CREDITS ChangeLog KNOWN_BUGS
%doc NEWS NOTES README RELEASE-POLICY doc/www.lesstif.org/FAQ
%attr(755, root, root) %dir %{_prefix}/X11R6/LessTif/Motif1.2/lib
%attr(755, root, root) %dir %{_prefix}/X11R6/LessTif/Motif2.1/lib
%attr(755, root, root) %{_prefix}/X11R6/LessTif/Motif1.2/lib/*.la
%attr(755, root, root) %{_prefix}/X11R6/LessTif/Motif2.1/lib/*.la
%attr(755, root, root) %{_prefix}/X11R6/lib/libDt.la
%attr(755, root, root) %{_prefix}/X11R6/lib/libMrm.la
%attr(755, root, root) %{_prefix}/X11R6/lib/libUil.la
%attr(755, root, root) %{_prefix}/X11R6/lib/libXbae.la
%attr(755, root, root) %{_prefix}/X11R6/lib/libXlt.la
%attr(755, root, root) %{_prefix}/X11R6/lib/libXm.la
%attr(755, root, root) %dir %{_prefix}/X11R6/LessTif/doc
%attr(-, root, root) %{_prefix}/X11R6/LessTif/doc/*
%attr(644, root, root) %{_prefix}/X11R6/man/man1/lesstif.1.gz

%doc doc/lessdox/*
%attr(755, root, root) %dir %{_prefix}/X11R6/include/Mrm
%attr(755, root, root) %dir %{_prefix}/X11R6/include/Xm
%attr(755, root, root) %dir %{_prefix}/X11R6/include/Xlt
%attr(755, root, root) %dir %{_prefix}/X11R6/include/Xbae
%attr(755, root, root) %dir %{_prefix}/X11R6/include/Dt
%attr(755, root, root) %dir %{_prefix}/X11R6/include/uil
%attr(755, root, root) %dir %{_prefix}/X11R6/LessTif/Motif2.1/include
%attr(755, root, root) %dir %{_prefix}/X11R6/LessTif/Motif1.2/include
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif1.2/include/Mrm/*
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif1.2/include/Xm/*
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif1.2/lib/*.a
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif2.1/include/Dt/*
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif2.1/include/Mrm/*
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif2.1/include/uil/*
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif2.1/include/Xm/*
%attr(644, root, root) %{_prefix}/X11R6/LessTif/Motif2.1/lib/*.a
%attr(755, root, root) %{_prefix}/X11R6/bin/mxmkmf
%attr(644, root, root) %{_prefix}/X11R6/include/Xlt/*
%attr(644, root, root) %{_prefix}/X11R6/include/Xbae/*
%attr(644, root, root) %{_prefix}/X11R6/lib/libMrm.a
%attr(644, root, root) %{_prefix}/X11R6/lib/libXm.a
%attr(644, root, root) %{_prefix}/X11R6/lib/libXlt.a
%attr(644, root, root) %{_prefix}/X11R6/lib/libXbae.a
%attr(644, root, root) %{_prefix}/X11R6/lib/libDt.a
%attr(644, root, root) %{_prefix}/X11R6/lib/libUil.a
%attr(644, root, root) %{_prefix}/X11R6/lib/X11/config/LessTif.*
%attr(644, root, root) %{_prefix}/X11R6/man/man3/*


%changelog
* Fri Dec 29 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
