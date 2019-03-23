Summary       : A PDF file viewer for the X Window System.
Name          : xpdf
Version       : 0.91
Release       : 1
Copyright     : GPL
Group         : Applications/Publishing

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.foolabs.com/xpdf/

BuildRequires : XFree86-devel freetype-devel
Requires      : XFree86 urw-fonts

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

%define t1libversion 1.0.1

Source0: ftp://ftp.foolabs.com/pub/xpdf/%{name}-%{version}.tgz
Source1: ftp://ftp.foolabs.com/pub/xpdf/t1lib-%{t1libversion}.tar.gz
Source3: xpdf.desktop
Source4: Xpdf
Patch0:  xpdf-0.90-zapf.patch
Patch1:  xpdf-0.90-fefe-diff2.gz
Patch2:  xpdf-0.91-buildroot.patch
Patch3:  xpdf-0.90-resource.patch
Patch4:  xpdf-0.90-XOutputDev.patch
Patch5:  xpdf-0.91-rgb.patch
Patch6:  xpdf-0.91-xpmlib.patch


%description
Xpdf is an X Window System based viewer for Portable Document Format
(PDF) files.  PDF files are sometimes called Acrobat files, after
Adobe Acrobat (Adobe's PDF viewer).  Xpdf is a small and efficient
program which uses standard X fonts.

Install the xpdf package if you need a viewer for PDF files.


%prep
%setup -q -a 1
%patch0 -p1 -b .zapf
#%patch1 -p1 -b .fefe
%patch2 -p1 -b .buildroot
%patch3 -p1 -b .resource
#%patch4 -p1 -b .XOutputDev
%patch5 -p1 -b .rgb
%patch6 -p1 -b .xpmlib


%build
cd T1-%{t1libversion}
cp %{_prefix}/lib/rpm/config.{guess,sub} ac-tools/
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--disable-shared \
	--enable-static
make without_doc

cd ..
autoconf
CFLAGS="${RPM_OPT_FLAGS}" \
CXXFLAGS="${RPM_OPT_FLAGS} -O" \
./configure \
	--prefix=%{_prefix} \
	--with-gzip \
	--enable-opi \
	--enable-japanese \
	--with-t1-library=`pwd`/T1-%{t1libversion}/lib/.libs \
	--with-t1-includes=`pwd`/T1-%{t1libversion}/lib \
	--with-freetype-library=/usr/lib \
	--with-freetype-includes=/usr/include
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc/X11/applnk/Applications
mkdir -p ${RPM_BUILD_ROOT}/etc/X11/app-defaults

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	bindir=${RPM_BUILD_ROOT}%{_prefix}/bin \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man 

install -m 0644 %{SOURCE3} ${RPM_BUILD_ROOT}/etc/X11/applnk/Applications/
install -m 0644 %{SOURCE4} ${RPM_BUILD_ROOT}/etc/X11/app-defaults/


strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc CHANGES README
%config (missingok) %attr(0644,root,root) /etc/X11/applnk/Applications/xpdf.desktop
%config             %attr(0644,root,root) /etc/X11/app-defaults/Xpdf
%{_prefix}/bin/*
%{_prefix}/share/man/man1/*


%changelog
* Fri Dec 29 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
