Summary		: Neon is an HTTP and WebDAV client library
Name		: neon
Version		: 0.28.4
Release		: 1
License		: LGPL
Group		: System/Libraries

Packager	: Keith Scroggins <kws@radix.net>
Vendor		: Sparemint
URL		: http://www.webdav.org/neon/

Prefix		: %{_prefix}
Docdir		: %{_prefix}/doc
BuildRoot	: %{_tmppath}/%{name}-root

Source0: %{name}-%{version}.tar.gz

%description
Neon is an HTTP and WebDAV client library, with a C interface. Featuring: 
- High-level interface to HTTP and WebDAV methods (PUT, GET, HEAD etc)
- Low-level interface to HTTP request handling, to allow implementing new
  methods easily. 
- persistent connections 
- RFC2617 basic and digest authentication (including auth-int, md5-sess) 
- Proxy support (including basic/digest authentication) 
- SSL/TLS support using OpenSSL (including client certificate support) 
- Generic WebDAV 207 XML response handling mechanism 
- XML parsing using the expat or libxml parsers 
- Easy generation of error messages from 207 error responses 
- WebDAV resource manipulation: MOVE, COPY, DELETE, MKCOL. 
- WebDAV metadata support: set and remove properties, query any set of
  properties (PROPPATCH/PROPFIND). 
- autoconf macros supplied for easily embedding neon directly inside an
  application source tree. 

%prep
%setup -q

%build
CFLAGS="-O -fomit-frame-pointer" \
./configure \
	--with-ssl=openssl --prefix=%{_prefix}

make

%install
[ "${RPM_BLUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:

%clean
[ "${RPM_BLUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*
%{_prefix}/share/man/man1/*
%{_prefix}/share/man/man3/*
%{_libdir}/pkgconfig/*
/usr/share/doc/%name-%version/*

%changelog
* Wed Mar 11 2009 Keith Scroggins <kws@radix.net>
- Updated to latest version, linking against latest OpenSSL

* Tue Jan 08 2008 Keith Scroggins <kws@radix.net>
- Initial build for MiNT

