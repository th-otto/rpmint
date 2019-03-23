Summary       : A GUI text editor for systems with X and Motif.
Name          : nedit
Version       : 5.4
Release       : 1
Copyright     : GPL
Group         : Applications/Editors

Packager      : Matthias Alles <alles@rhrk.uni-kl.de>
Vendor        : Sparemint
URL           : http://www.nedit.org


Source: http://nedit.org/ftp/v5_4/nedit-%{version}-source.tar.gz
Patch0: nedit-5.4-mint.patch

BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: lesstif-devel

%description
NEdit is a GUI text editor for the X Window System and Motif. NEdit is
very easy to use, especially if you are familiar with the
Macintosh(TM) or Microsoft(TM) Windows(TM) style of interface.
It features syntax highlighting with built-in patterns for C, C++, Java,
Ada, FORTRAN, Pascal, Yacc, Perl, Python, Tcl, Csh, Awk, HTML, LaTeX,
VHDL, Verilog, and more.

%prep
%setup -q
%patch0 -p1 -b .mint


%build
make mint

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/X11R6/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/X11R6/man/man1
strip source/nedit
strip source/nc
stack --fix=200k source/nedit
stack --fix=200k source/nc
install -m 755 source/nedit source/nc $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/
install -m 644 doc/nedit.man $RPM_BUILD_ROOT%{_prefix}/X11R6/man/man1/nedit.1x
install -m 644 doc/nc.man $RPM_BUILD_ROOT%{_prefix}/X11R6/man/man1/nc.1x


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/nedit.doc README ReleaseNotes
%{_prefix}/X11R6/man/*/*
%{_prefix}/X11R6/bin/*

%changelog
* Sun Jan 04 2004 Matthias Alles <alles@rhrk.uni-kl.de>
- updated from 5.3 to 5.4

* Wed Dec 03 2003 Matthias Alles <alles@rhrk.uni-kl.de>
- first Sparemint release
