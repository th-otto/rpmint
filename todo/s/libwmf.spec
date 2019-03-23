Summary       : library and utilities for displaying and converting metafile images
Name          : libwmf
Version       : 0.2.2
Release       : 1
Copyright     : LGPL
Group         : Development/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.wvware.com/

BuildRequires : libpng, zlib-devel, freetype-devel >= 2.0.4, libxml2-devel
Requires      : libpng, zlib-devel, freetype-devel >= 2.0.4, libxml2-devel

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://download.sourceforge.net/wvware/libwmf-%{version}.tar.gz


%description
This is a library for interpreting metafile images and either displaying them
using X or converting them to standard formats such as PNG, JPEG, PS, EPS,...


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--without-expat \
	--with-plot \
	--with-layers
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	DESTDIR=${RPM_BUILD_ROOT}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README COPYING ChangeLog
%doc %{_prefix}/share/doc/libwmf/

%{_prefix}/bin/libwmf-fontmap
%{_prefix}/bin/wmf2*
%{_prefix}/share/libwmf

%{_prefix}/bin/libwmf-config
%{_prefix}/include/libwmf
%{_prefix}/lib/lib*a


%changelog
* Tue Nov 06 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.2.2

* Tue Jul 10 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.2.0

* Sat Dec 23 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
