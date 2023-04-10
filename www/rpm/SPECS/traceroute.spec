%define pkgname traceroute

%rpmint_header

Summary:        Traces the route taken by packets over a TCP/IP network
Name:           %{crossmint}%{pkgname}
Version:        1.4a5
Release:        1
License:        BSD-3-Clause
Group:          Applications/Internet

Packager:       %{packager}
URL:            ftp://ftp.ee.lbl.gov/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: ftp://ftp.ee.lbl.gov/traceroute-1.4a5.tar.xz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/%{pkgname}/traceroute-mint.patch

%rpmint_essential
BuildRequires:  make

%rpmint_build_arch

%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.  Traceroute displays
the IP number and host name (if possible) of the machines along the
route taken by the packets.  Traceroute is used as a network debugging
tool.  If you're having network connectivity problems, traceroute will
show you where the trouble is coming from along the route.

Install traceroute if you need a tool for diagnosing network connectivity
problems.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%patch0 -p1

cp "%{S:1}" config.sub

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

	CC=${TARGET}-gcc \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	./configure
	
	make
	
	mkdir -p "%{buildroot}%{_rpmint_sysroot}/sbin"
	install -m 4755 traceroute "%{buildroot}%{_rpmint_sysroot}/sbin"
	mkdir -p "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man8"
	install -m 644 traceroute.8 "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man8"
	
	make clean

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
%doc CHANGES README
%{_isysroot}/sbin/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*


%changelog
* Mon Apr 10 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Tue Sep 25 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
