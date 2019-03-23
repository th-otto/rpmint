Summary       : MSWord Document to HTML converter
Name          : wv
Version       : 0.7.0
Release       : 1
License       : GPL
Group         : Applications/Text

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.wvWare.com/

BuildRequires : XFree86-devel, ImageMagick-devel >= 5.3.6
BuildRequires : freetype-devel, libwmf, libxml2-devel, libiconv, glib

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: http://download.sourceforge.net/wvware/%{name}-%{version}.tar.gz
Patch0:  wv-DESTDIR.patch
Patch1:  wv-0.7.0-config.patch
Patch2:  wv-0.6.5-types.patch


%description
MSWordView is a program that understands the Microsoft Word 8 binary
file format (Office97, Office2000) and is able to convert Word
documents into HTML, which can then be read with a browser.

wv is a suite of programs to help convert Word Documents to HTML.

%package devel
Summary       : Include files needed to compile
Group         : Development/Libraries
Requires      : %{name} = %{version}

%description devel
Contains the header files.


%prep
%setup -q
%patch0 -p1 -b .destdir
%patch1 -p1 -b .config
%patch2 -p1 -b .types

# Checking for CVS specific files and removing them.
find . -type d -name 'CVS'| xargs rm -rf

autoconf


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--with-zlib \
	--with-png \
	--with-libwmf \
	--with-libiconv \
	--with-Magick
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc CHANGELOG CREDITS D_CREDITS D_README KNOWN-BUGS README TESTING TODO.TXT
%{_prefix}/bin/*
%{_prefix}/share/wv
%{_prefix}/share/man/man*/*

%files devel
%defattr(-,root,root)
%{_prefix}/include/*.h
%{_prefix}/lib/libwv.a


%changelog
* Tue Nov 06 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.7.0

* Wed Jul 11 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
