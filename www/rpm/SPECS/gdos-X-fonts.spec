%define pkgname gdos-X-fonts

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Required fonts for Atari X environment
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        03
Release:        1
License:        Public Domain
Group:          System/X11/Fonts

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://freemint.de/X11/

Prefix:         %{_prefix}
%if "%{buildtype}" != "cross"
Docdir:         %{_rpmint_target_prefix}/share/doc
%else
Docdir:         %{_rpmint_docdir}
%endif
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://freemint.de/X11/gdos-X-fonts-03.tgz

%rpmint_essential

BuildArch:      noarch
%if "%{buildtype}" != "cross"
Requires:       XServer
%define _arch noarch
%endif

%description
Required fonts for Atari X environment

%prep
%setup -q -n X-fonts

%build

%install

%if "%{buildtype}" == "cross"
%define gemsys_dir %{_rpmint_sysroot}/gemsys
%else
%define gemsys_dir /c/GEMSYS
%endif

mkdir -p "%{buildroot}%{gemsys_dir}"
cp -a GEMSYS/*.fnt "%{buildroot}%{gemsys_dir}"

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README
%{gemsys_dir}/*.fnt


%changelog
* Fri Mar 17 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
