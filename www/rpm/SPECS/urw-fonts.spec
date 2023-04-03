%define pkgname urw-fonts

%rpmint_header

Summary       : Free versions of the 35 standard PostScript fonts.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 2.0
Release       : 3
License       : GPL-2.0-or-later
# URW holds copyright
Group         : User Interface/X

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : ftp://ftp.cs.wisc.edu/ghost/gnu/fonts/

%if "%{buildtype}" != "cross"
Prereq        : chkfontpath
%endif

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root
BuildArch     : noarch
%global _arch noarch

Source: ftp://ftp.cs.wisc.edu/ghost/gnu/fonts/gnu-gs-fonts-std-6.0.tar.gz
Patch0: patches/urw-fonts/urw-fonts-adobenames.patch


%description 
Free, good quality versions of the 35 standard PostScript(TM) fonts,
donated under the GPL by URW++ Design and Development GmbH.  The
fonts.dir file font names match the original Adobe names of the fonts
(e.g., Times, Helvetica, etc.).

Install the urw-fonts package if you need free versions of standard
PostScript fonts.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -c -n %{pkgname}-%{version}
%patch0 -p1


%install

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1
cd fonts
cp -f *.afm *.pfm *.pfb %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1
install -m 644 fonts.dir \
	%{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1/fonts.scale
{
    pushd %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1
    mkfontdir .
    popd
}


%if "%{buildtype}" != "cross"
%post
/usr/sbin/chkfontpath -q -a %{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/chkfontpath -q -r %{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1
fi
%endif


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(0644,root,root,0755)
%dir %{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1
%config(noreplace) %{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1/fonts.dir
%config(noreplace) %{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1/fonts.scale
%{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1/*.afm
%{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1/*.pfm
%{_isysroot}%{_rpmint_target_prefix}/share/fonts/default/Type1/*.pfb


%changelog
* Thu Mar 23 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Mon Dec 18 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
