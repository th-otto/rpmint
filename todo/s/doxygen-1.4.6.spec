Summary      : A documentation system for C/C++.
Name         : doxygen
Version      : 1.4.6
Release      : 1
Copyright    : GPL
Group        : Development/Tools

Packager     : Arnaud BERCEGEAY <arnaud.bercegeay@free.fr>
Vendor       : Sparemint
URL          : http://www.stack.nl/~dimitri/doxygen/index.html

Prefix       : %{_prefix}
Docdir       : %{_prefix}/doc
BuildRoot    : %{_tmppath}/%{name}-%{version}-root

Source: %{name}-%{version}.src.tar.gz

%description
Doxygen can generate an online class browser (in HTML) and/or a
reference manual (in LaTeX) from a set of documented source files. The
documentation is extracted directly from the sources. Doxygen can
also be configured to extract the code structure from undocumented
source files.

%prep
%setup -q

%build
./configure --prefix %{_prefix}
make all

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#export OLD_PO_FILE_INPUT=yes
make install INSTALL=$RPM_BUILD_ROOT%{_prefix}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc LANGUAGE.HOWTO README
%{_bindir}/doxygen
%{_bindir}/doxytag

%changelog
* Mon Jan 2 2006 Arnaud BERCEGEAY <bercegeay@atari.org>
- updated for release 1.4.6

* Tue Oct 4 2005 Arnaud BERCEGEAY <bercegeay@atari.org>
- updated for release 1.4.5

* Mon Jul 25 2005 Arnaud BERCEGEAY <bercegeay@atari.org>
- updated for release 1.4.4

* Mon May 16 2005 Arnaud BERCEGEAY <bercegeay@atari.org>
- updated for release 1.4.3

* Thu Dec 02 2004 Arnaud BERCEGEAY <bercegeay@atari.org>
- updated for release 1.3.9.1_20041129

* Thu Dec 02 2004 Arnaud BERCEGEAY <bercegeay@atari.org>
- Creation, based on spec file provided in doxygen sources.
