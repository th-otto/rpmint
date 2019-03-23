%define libmaj 1
%define libmin 0
%define librel 0
%define librev c
%define openssldir /var/ssl
%define version 1.0.0c
%define is_sparemint %(test -e /etc/sparemint-release && echo 1 || echo 0)
%undefine __os_install_post

Version: 	%{version}
Release: 	1
Summary: 	Secure Sockets Layer and cryptography libraries and tools
Name: 		openssl
Source0: 	ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz
Patch0: 	openssl-1.0.0-mint.patch
License: 	Freely distributable
Group: 		System Environment/Libraries
Provides: 	SSL
URL: 		http://www.openssl.org/
Packager: 	Keith Scroggins <kws@radix.net>
Vendor: 	Sparemint
BuildRoot:  	/var/tmp/%{name}-%{version}-root
%if %is_sparemint
Buildrequires: 	mintbin perl gzip fileutils
%else
AutoReqProv:	no
%endif

%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its related
documentation. 

OpenSSL is based on the excellent SSLeay library developed from Eric A.
Young and Tim J. Hudson.  The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get and
use it for commercial and non-commercial purposes. 

This package contains the base OpenSSL cryptography and SSL/TLS tools.

%package devel
Summary: Secure Sockets Layer and cryptography static libraries and headers
Group: Development/Libraries
Requires: openssl mintlib-devel >= 0.55
%description devel
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its related
documentation. 

OpenSSL is based on the excellent SSLeay library developed from Eric A.
Young and Tim J. Hudson.  The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get and
use it for commercial and non-commercial purposes. 

This package contains the the OpenSSL cryptography and SSL/TLS 
static libraries and header files required when developing applications.

%prep

%setup -q
%patch0 -p1

%build 

%define CONFIG_FLAGS --prefix=/usr

perl util/perlpath.pl /usr/bin/perl

./Configure %{CONFIG_FLAGS} --openssldir=%{openssldir} cf-mint
%if !%is_sparemint
sed -i "s/^CC=.*/CC= m68k-atari-mint-gcc/" Makefile
sed -i "s/^AR=.*/AR= m68k-atari-mint-ar $(ARFLAGS) r/" Makefile
sed -i "s/^RANLIB=.*/RANLIB= m68k-atari-mint-ranlib/" Makefile
%endif
make
make rehash

mkdir savlibs
mv libcrypto.a savlibs/libcryptoCF.a
mv libssl.a savlibs/libsslCF.a
make clean
./Configure %{CONFIG_FLAGS} --openssldir=%{openssldir} m680x0-mint
%if !%is_sparemint
sed -i "s/^CC=.*/CC= m68k-atari-mint-gcc/" Makefile
sed -i "s/^AR=.*/AR= m68k-atari-mint-ar $(ARFLAGS) r/" Makefile
sed -i "s/^RANLIB=.*/RANLIB= m68k-atari-mint-ranlib/" Makefile
%endif
make
make rehash

mv libcrypto.a savlibs/libcrypto020-60.a
mv libssl.a savlibs/libssl020-60.a
make clean
./Configure %{CONFIG_FLAGS} --openssldir=%{openssldir} m68k-mint
%if !%is_sparemint
sed -i "s/^CC=.*/CC= m68k-atari-mint-gcc/" Makefile
sed -i "s/^AR=.*/AR= m68k-atari-mint-ar $(ARFLAGS) r/" Makefile
sed -i "s/^RANLIB=.*/RANLIB= m68k-atari-mint-ranlib/" Makefile
%endif
make
make rehash

#make test - already passed successfully

%install
rm -rf $RPM_BUILD_ROOT
make install MANDIR=/usr/share/man INSTALL_PREFIX="$RPM_BUILD_ROOT"

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475

install -m644 savlibs/libsslCF.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libssl.a
install -m644 savlibs/libcryptoCF.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libcrypto.a

install -m644 savlibs/libssl020-60.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libssl.a
install -m644 savlibs/libcrypto020-60.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libcrypto.a

%if %is_sparemint
strip $RPM_BUILD_ROOT/usr/bin/openssl
%else
m68k-atari-mint-strip $RPM_BUILD_ROOT/usr/bin/openssl
%endif

# Clean up symlinks....
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/md2.1
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/md4.1
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/md5.1
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/mdc2.1
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/ripemd160.1
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/sha.1
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/sha1.1
# Too many symlinks, remove, for now
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man3

# Conflicts with shadow-utils package
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/passwd.1

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5/*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man7/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
%post devel

%files 
%defattr(0644,root,root,0755)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README
%attr(0755,root,root) /usr/bin/openssl
%attr(0755,root,root) /usr/bin/c_rehash
%attr(0755,root,root) %{openssldir}/misc/*
%attr(0644,root,root) /usr/share/man/man[157]/*
%config %attr(0644,root,root) %{openssldir}/openssl.cnf 
%dir %attr(0755,root,root) %{openssldir}/certs
%dir %attr(0755,root,root) %{openssldir}/misc
%dir %attr(0750,root,root) %{openssldir}/private

%files devel
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README
%defattr(0644,root,root,0755)
%attr(0644,root,root) /usr/lib/lib*.a
%attr(0644,root,root) /usr/lib/m5475/lib*.a
%attr(0644,root,root) /usr/lib/m68020-60/lib*.a
%attr(0644,root,root) /usr/lib/pkgconfig/*.pc
%attr(0644,root,root) /usr/include/openssl/*
#Too many symlinks, disable for now
#%attr(0644,root,root) /usr/share/man/man[3]/*

%changelog
* Thu Dec 09 2010 Keith Scroggins <kws@radix.net>
- Upgraded to 1.0.0c

* Mon Dec 06 2010 Keith Scroggins <kws@radix.net>
- Upgraded to 1.0.0b

* Wed Jun 09 2010 Keith Scroggins <kws@radix.net>
- Upgraded to 1.0.0a and added the ability to Cross Compile the RPM

* Sun May 23 2010 Keith Scroggins <kws@radix.net>
- Upgraded to 1.0.0 and incorporated assembly code from Howard Chu for 68020+
- target.

* Tue Jan 19 2010 Keith Scroggins <kws@radix.net>
- Modified to build libraries for 68000 / 68020-60 / 5475

* Sat Jan 16 2010 Keith Scroggins <kws@radix.net>
- Updated to the latest version of OpenSSL.

* Wed May 6 2009 Keith Scroggins <kws@radix.net>
- Updated to the latest version of OpenSSL.

* Sun Mar 1 2009 Keith Scroggins <kws@radix.net>
- Updated to the latest version of OpenSSL.

* Fri Mar 19 2004 Keith Scroggins <kws@radix.net>
- Updated package to the latest security fixed version

* Mon Feb 9 2004 Keith Scroggins <kws@radix.net>
- Updated packaged to the latest version (had a security fix) and compiled
- against the newest MiNTLib release.

* Tue Oct 14 2003 Keith Scroggins <kws@radix.net>
- Updated package to the latest secure version of OpenSSL and fixed the patches
- to apply to this version.  Otherwise, patches are the same as the original
- packagers.

* Thu Dec 05 2000 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- recompiled with correct gcc optimizations

* Sun Nov 26 2000 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- initial release for Sparemint, based on original .spec-file found
  in openssl-0.9.6.tar.gz
