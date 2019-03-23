Summary       : Free versions of the 35 standard PostScript fonts.
Name          : urw-fonts
Version       : 2.0
Release       : 2
Copyright     : GPL, URW holds copyright
Group         : User Interface/X

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.cs.wisc.edu/ghost/gnu/fonts/

Prereq        : chkfontpath

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root
BuildArchitectures: noarch

Source: ftp://ftp.cs.wisc.edu/ghost/gnu/fonts/gnu-gs-fonts-std-6.0.tar.gz
Patch0: urw-fonts-adobenames.patch


%description 
Free, good quality versions of the 35 standard PostScript(TM) fonts,
donated under the GPL by URW++ Design and Development GmbH.  The
fonts.dir file font names match the original Adobe names of the fonts
(e.g., Times, Helvetica, etc.).

Install the urw-fonts package if you need free versions of standard
PostScript fonts.


%prep
%setup -q -c
%patch0 -p1 -b .adobenames


%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/fonts/default/Type1
cd fonts
cp -f *.afm *.pfm *.pfb ${RPM_BUILD_ROOT}%{_prefix}/share/fonts/default/Type1
install -m 644 fonts.dir \
	${RPM_BUILD_ROOT}%{_prefix}/share/fonts/default/Type1/fonts.scale
{
    pushd ${RPM_BUILD_ROOT}%{_prefix}/share/fonts/default/Type1
    mkfontdir .
    popd
}


%post
/usr/sbin/chkfontpath -q -a %{_prefix}/share/fonts/default/Type1

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/chkfontpath -q -r %{_prefix}/share/fonts/default/Type1
fi


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(0644,root,root,0755)
%dir %{_prefix}/share/fonts/default/Type1
%config(noreplace) %{_prefix}/share/fonts/default/Type1/fonts.dir
%config(noreplace) %{_prefix}/share/fonts/default/Type1/fonts.scale
%{_prefix}/share/fonts/default/Type1/*.afm
%{_prefix}/share/fonts/default/Type1/*.pfm
%{_prefix}/share/fonts/default/Type1/*.pfb


%changelog
* Mon Dec 18 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
