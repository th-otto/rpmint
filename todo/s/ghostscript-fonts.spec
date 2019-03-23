Summary       : Fonts for the Ghostscript PostScript(TM) interpreter.
Name          : ghostscript-fonts
Version       : 6.0
Release       : 1
License       : GPL
Group         : Applications/Publishing

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.ghostscript.com/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root
BuildArchitectures: noarch

Source: ftp://ftp.cs.wisc.edu/pub/ghost/aladdin/fonts/ghostscript-fonts-other-%{version}.tar.gz


%description
Ghostscript-fonts contains a set of fonts that Ghostscript, a
PostScript interpreter, uses to render text. These fonts are in
addition to the fonts shared by Ghostscript and the X Window System.

You'll need to install ghostscript-fonts if you're installing
ghostscript.


%prep
%setup -q -c ghostscript-fonts-%{version}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/fonts/default/ghostscript
cp fonts/* ${RPM_BUILD_ROOT}%{_prefix}/share/fonts/default/ghostscript


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,-)
%{_prefix}/share/fonts/default/ghostscript


%changelog
* Mon Dec 18 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
