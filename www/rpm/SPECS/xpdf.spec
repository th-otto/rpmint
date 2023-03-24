%define pkgname xpdf

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

%rpmint_header

Summary       : A PDF file viewer for the X Window System.
%if "%{buildtype}" == "cross"
Name          : cross-mint-%{pkgname}
%else
Name          : %{pkgname}
%endif
Version       : 0.91
Release       : 1
License       : GPL-2.0-or-later
Group         : Applications/Publishing

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : http://www.foolabs.com/xpdf/

BuildRequires : autoconf
%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
#BuildRequires : cross-mint-freetype2-devel
Requires      : cross-mint-XFree86
Requires      : cross-mint-urw-fonts
%else
BuildRequires : XFree86-devel
#BuildRequires : freetype2-devel
Requires      : XFree86
Requires      : urw-fonts
%endif

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

%define t1libversion 1.0.1

Source0: ftp://ftp.foolabs.com/pub/xpdf/%{pkgname}-%{version}.tgz
Source1: ftp://ftp.foolabs.com/pub/xpdf/t1lib-%{t1libversion}.tar.gz
Source3: xpdf.desktop
Source4: xpdf-Xpdf.ad
Source5: mintelf-config.sub
Patch0:  xpdf-0.90-zapf.patch
Patch1:  xpdf-0.90-fefe-diff2.gz
Patch2:  xpdf-0.91-buildroot.patch
Patch3:  xpdf-0.90-resource.patch
Patch4:  xpdf-0.90-XOutputDev.patch
Patch5:  xpdf-0.91-rgb.patch
Patch6:  xpdf-0.91-xpmlib.patch
Patch7:  xpdf-0.91-configure.patch

%rpmint_build_arch


%description
Xpdf is an X Window System based viewer for Portable Document Format
(PDF) files.  PDF files are sometimes called Acrobat files, after
Adobe Acrobat (Adobe's PDF viewer).  Xpdf is a small and efficient
program which uses standard X fonts.

Install the xpdf package if you need a viewer for PDF files.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -a 1 -n %{pkgname}-%{version}
%patch0 -p1
#%%patch1 -p1
%patch2 -p1
%patch3 -p1
#%%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

cp %{S:5} config.sub

autoconf

cd T1-%{t1libversion}
rm -f ac-tools/aclocal.m4 ac-tools/ltconfig ac-tools/ltmain.sh
touch ac-tools/aclocal.m4
libtoolize -i
aclocal -I ac-tools -I m4

autoconf

rm -f ac-tools/config.sub
cp %{S:5} ac-tools/config.sub

cd ..

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}"

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 020
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	cd T1-%{t1libversion}
	CFLAGS="${COMMON_CFLAGS} ${CPU_CFLAGS}" \
	./configure \
		${CONFIGURE_FLAGS} \
		--disable-shared \
		--enable-static
	make without_doc
	
	cd ..
	CFLAGS="${COMMON_CFLAGS} ${CPU_CFLAGS}" \
	CXXFLAGS="${COMMON_CFLAGS} ${CPU_CFLAGS}" \
	./configure \
		${CONFIGURE_FLAGS} \
		--with-gzip \
		--enable-opi \
		--enable-japanese \
		--with-t1-library=`pwd`/T1-%{t1libversion}/lib/.libs \
		--with-t1-includes=`pwd`/T1-%{t1libversion}/lib
	make
done


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_isysroot}/etc/X11/applnk/Applications
mkdir -p %{buildroot}%{_isysroot}/etc/X11/app-defaults

make \
	bindir=%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin \
	mandir=%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man \
	install

install -m 0644 %{S:3} %{buildroot}%{_isysroot}/etc/X11/applnk/Applications/xpdf.desktop
install -m 0644 %{S:4} %{buildroot}%{_isysroot}/etc/X11/app-defaults/Xpdf


%{_rpmint_target}-strip %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:
%{_rpmint_target}-stack --fix=256k %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc CHANGES README
%config (missingok) %attr(0644,root,root) %{_isysroot}/etc/X11/applnk/Applications/xpdf.desktop
%config             %attr(0644,root,root) %{_isysroot}/etc/X11/app-defaults/Xpdf
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/*


%changelog
* Thu Mar 23 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri Dec 29 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
