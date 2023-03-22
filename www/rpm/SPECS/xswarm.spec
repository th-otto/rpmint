%define pkgname xswarm

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

%rpmint_header

%if "%{buildtype}" == "cross"
%define _isysroot %{_rpmint_sysroot}
%else
%define _isysroot %{nil}
%endif

Summary       : A nice X11 demo or screensaver.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 2.3
Release       : 2
License       : MIT
Group         : Amusements/Graphics

BuildRequires : XFree86-devel
Requires      : XFree86

%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
Requires      : cross-mint-XFree86
%else
BuildRequires : XFree86-devel
Requires      : XFree86
%endif

Packager:       Thorsten Otto <admin@tho-otto.de>

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{pkgname}-%{version}.tar.gz
Patch0: patches/%{pkgname}/xswarm.patch

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


%description
The well known xswarm screensaver or X11 demo program. Similiar
to ATARI's lines.app that was shipped with MultiTOS.

Author:
--------
    Jeff Butterworth <butterwo@cs.unc.edu>


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# That package does not have an Imakefile in the top directory :(
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

	%{_rpmint_target}-xmkmf -DCpuOption="${CPU_CFLAGS}" -a
	make
done


%install
make DESTDIR=%{buildroot} install install.man

%if "%{buildtype}" != "cross"
cp -pr %{buildroot}%{_rpmint_sysroot}/. %{buildroot}
rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%{_rpmint_target}-strip %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:
%{_rpmint_target}-stack --fix=64k %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/* ||:

# compress manpages
gzip -9nf %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/*/*


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xswarm
%{_isysroot}%{_rpmint_target_prefix}/X11R6/man/man1/xswarm.1x*


%changelog
* Wed Mar 22 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
