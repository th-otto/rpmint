Summary        : A console based sudoku game with a curses interface
Name           : sudoku
Version        : 1.0.1
Release        : 1
License        : PD
Group          : Applications/Games

Vendor         : Sparemint
Packager       : Martin Tarenskeen <m.tarenskeen@zonnet.nl>
URL            : http://www.laurasia.com.au/sudoku

Prefix         : %{_prefix}
BuildRoot      : %{_tmppath}/%{name}-%{version}-buildroot

Source         : http://www.laurasia.com.au/downloads/%{name}-%{version}.tgz
Patch          : %{name}-%{version}.patch

%description
The Sudoku board game is played on a 9x9 grid, divided into rows,
columns, and 9 blocks of 3x3 squares. The objective is to fill the
empty  squares with the digits 1-9, so that each row, column, and block
contains each of the digits 1-9 (and hence, it is not possible for  any
digit to appear twice in the same row, column or block).

%prep
%setup -q
%patch -p1

%build
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 sudoku ${RPM_BUILD_ROOT}%{_bindir}/sudoku
strip ${RPM_BUILD_ROOT}%{_bindir}/sudoku
install -d ${RPM_BUILD_ROOT}/usr/lib/sudoku
install -m 644 template ${RPM_BUILD_ROOT}/usr/lib/sudoku/template
install -d ${RPM_BUILD_ROOT}%{_mandir}/man6
install -m 644 sudoku.6 ${RPM_BUILD_ROOT}%{_mandir}/man6/sudoku.6
gzip ${RPM_BUILD_ROOT}%{_mandir}/man6/sudoku.6
   
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc CHANGES README sudoku.html
%{_bindir}/*
/usr/lib/sudoku/template
%{_mandir}/man6/*

%changelog
* Wed Oct 19 2005 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- initial SpareMiNT RPM package release for sudoku-1.0.1
