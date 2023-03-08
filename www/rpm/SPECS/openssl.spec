%define pkgname openssl

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

%define _sonum  1_1
Summary:        Secure Sockets and Transport Layer Security
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.1.1p
Release:        1
License:        OpenSSL
Group:          Productivity/Networking/Security

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://www.openssl.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://www.openssl.org/source/%{pkgname}-%{version}.tar.gz
Patch0: patches/openssl/openssl-1.1.1p-mint.patch
Patch1: patches/openssl/openssl-zlib-static.patch
Patch1: patches/openssl/openssl-bn_div-asm.patch

%rpmint_essential
BuildRequires:  pkgconfig
%if "%{buildtype}" == "cross"
Provides:       pkgconfig(cross-mint-libssl) = %{version}
Provides:       pkgconfig(cross-mint-libcrypto) = %{version}
Provides:       pkgconfig(cross-mint-openssl) = %{version}
%else
Provides:       pkgconfig(libssl) = %{version}
Provides:       pkgconfig(libcrypto) = %{version}
Provides:       pkgconfig(openssl) = %{version}
%endif

%if "%{buildtype}" == "cross"
BuildArch:      noarch
%else
%define _target_platform %{_rpmint_target_platform}
%if "%{buildtype}" == "v4e"
%define _arch m5475
%else
%if "%{buildtype}" == "020"
%define _arch m68020
%else
%define _arch m68k
%endif
%endif
%endif

%define SSLETCDIR /etc/ssl

%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, full-featured, and open source toolkit implementing
the Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS
v1) protocols with full-strength cryptography. The project is managed
by a worldwide community of volunteers that use the Internet to
communicate, plan, and develop the OpenSSL toolkit and its related
documentation.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build

%rpmint_cflags

CONFIGURE_FLAGS="--prefix=%{_rpmint_target_prefix} --cross-compile-prefix=${TARGET}- ${CONFIGURE_FLAGS_AMIGAOS}
	 --openssldir=%{SSLETCDIR}
	zlib
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

targetconf_000=mint
targetconf_020=mint020
targetconf_v4e=mintv4e


for CPU in ${ALL_CPUS}; do
	eval targetconf=\${targetconf_$CPU}
	"./Configure" ${CONFIGURE_FLAGS} $targetconf

	make %{?_smp_mflags}
	make MANDIR=%{_rpmint_target_prefix}/share/man DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make distclean
done


%install

%rpmint_cflags

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
rm -rf %{buildroot}/etc
mv %{buildroot}%{_rpmint_sysroot}/etc %{buildroot}/etc
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}/*.pc
%{_rpmint_datadir}
%{_rpmint_sysroot}%{SSLETCDIR}
%else
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%{SSLETCDIR}
%endif




%changelog
* Sun Mar 5 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Upgraded to 1.1.1p

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
