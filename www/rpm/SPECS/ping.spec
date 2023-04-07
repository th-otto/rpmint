%define pkgname ping

%rpmint_header

Summary:        The ping command
Name:           %{crossmint}%{pkgname}
Version:        20190714
Release:        1
License:        BSD-3-Clause
Group:          System/Base

Packager:       %{packager}
URL:            http://cvsweb.netbsd.org/bsdweb.cgi/basesrc/sbin/ping/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz

Patch0: patches/%{pkgname}/ping-20190714-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make

%rpmint_build_arch

%description
The ping command.
Ported from BSD sources.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%patch0 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


NO_STRIP=1

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 000
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s -o ping ping.c ping_hostops.c -lm || exit 1

	mkdir -p "%{buildroot}%{_rpmint_sysroot}/bin"
	install -m 4555 ping "%{buildroot}%{_rpmint_sysroot}/bin"
	mkdir -p "%{buildroot}%{_rpmint_mandir}/man8"
	install -m 444 ping.8 "%{buildroot}%{_rpmint_mandir}/man8"
	
	rm -f ping


	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_sysroot}/bin/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif
done


%install

%rpmint_cflags

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_isysroot}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*


%changelog
* Fri Apr 07 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 20190714

* Tue Oct 02 2001 Frank Naumann <fnaumann@freemint.de>
- corrected wrong mode bits for the ping tool

* Tue Sep 25 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
