Summary:        RPM macros for cross-compiling MiNT stuff
Name:           rpm-macros
Version:        1.0
Release:        1
License:        Public Domain
Group:          System/Packages

Packager:       Thorsten Otto <admin@tho-otto.de>
Source0:        rpm-macros.rpmint

Prefix:         %{_prefix}
BuildArch:      noarch
%global _arch noarch

%description
RPM macros for cross-compiling MiNT stuff.

%prep

%build

%install

mkdir -p %{buildroot}%{_prefix}/lib/rpm/macros.d
cp --preserve=mode,timestamps %{SOURCE0} %{buildroot}%{_prefix}/lib/rpm/macros.d/macros.rpmint

%files
%defattr(-,root,root)
%{_prefix}/lib/rpm/macros.d

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
