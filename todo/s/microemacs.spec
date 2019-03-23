Summary       : microemacs -- a small, although powerful emacs clone.
Name          : microemacs
Version       : 5.03
Release       : 1
Copyright     : GPL
Group         : Applications/Editors

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.ac-grenoble.fr/ge/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.ac-grenoble.fr/ge/Office/microemacs-%{version}.tgz
Patch0: microemacs-5.03-mint.patch


%description
MicroEMACS has been developped by Daniel M. Lawrence
since the mid 80's and the 3.12 version appeared in 1993.
MicroEMACS is a small, although quick and efficient
emacs clone. The initialization file emacs.rc file is 
highly configurable. The included emacs.rc is designed
to work in a TeX or LaTeX environment. The microemacs
archive is a relatively minor modification of Lawrence's 
uemacs-3.12 distribution, with suitable changes in the
source code to make it compile under Linux. It further adds
a justification procedure taken from par-1.50


%prep
%setup -q
%patch0 -p1 -b .mint


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/microemacs

install -m 755 microemacs ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m 644 lib/*      ${RPM_BUILD_ROOT}%{_prefix}/lib/microemacs/

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=80k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README TODO
%{_prefix}/bin/*
%{_prefix}/lib/microemacs


%changelog
* Tue Apr 23 2002 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
