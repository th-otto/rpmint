%define pkgname chkfontpath

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary       : Simple interface for editing the font path for the X font server.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 1.7
Release       : 3
License       : GPL
Group         : System Environment/Base

Requires      : XFree86-xfs

Prefix        : %{_prefix}
Docdir        : %{_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{pkgname}-%{version}.tar.gz

%rpmint_build_arch

%description 
This is a simple terminal mode program for configuring the directories
in the X font server's path. It is mostly intended to be used
`internally' by RPM when packages with fonts are added or removed, but
it may be useful as a stand-alone utility in some instances.


%prep
%setup -q -n %{pkgname}-%{version}

# remove strip flag from install target; it would invoke the host strip, not ours.
# we strip the binaries ourselve below
sed -i 's/755 -s/755/' Makefile

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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

	make CC="%{_rpmint_target}-gcc $CPU_CFLAGS" CFLAGS="-O2 -fomit-frame-pointer"

	make INSTROOT=%{buildroot}%{_isysroot} install
	mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share
	mv %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/man %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share
	# compress manpages
	%rpmint_gzip_docs
done


%install

%{_rpmint_target_strip}-strip %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/sbin/* ||:


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/sbin/chkfontpath
%{_isysroot}%{_rpmint_target_prefix}/share/man/man8/*


%changelog
* Tue Mar 21 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Mon Dec 18 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
